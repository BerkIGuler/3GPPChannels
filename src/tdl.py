from NeoRadium.neoradium import TdlChannel, random, Carrier
import numpy as np
from tqdm import tqdm


def generate_tdl_channels(
    num_channels: int = 10000,
    *,
    random_seed: int = 123,
    start_rb: int = 0,
    num_rbs: int = 10,
    spacing: int = 15,
    tx_antenna_count: int = 1,
    rx_antenna_count: int = 1,
    carrier_freq: float = 3.5e9,
    doppler_shift: float = 100,
    delay_spread: int = 500,
    profile: str = "A",
    show_progress: bool = True,
    normalize_mean_power: bool = True,
    slots_per_channel: int = 1,
    sos_type: str = "Xiao",
    sos_num_sins: int = 32,
    **channel_kwargs,
) -> np.ndarray:
    """Generate TDL channel matrices over multiple slots.

    NeoRadium advances time by one **slot** per `goNext()`. Slot duration is determined
    by **spacing** (subcarrier spacing): 15 kHz → 1 slot = 1 ms; 30 kHz → 0.5 ms; etc.
    For low Doppler, use spacing=15 and optionally slots_per_channel > 1 so consecutive
    channel matrices are further apart in time (less variation).

    Within-slot correlation (across OFDM symbols): NeoRadium uses a Sum-of-Sinusoids (SOS)
    method for Doppler. Use sos_type='GMEDS1' (default) for smooth, deterministic
    evolution; avoid 'Xiao' which can give less smooth transitions. Increasing
    sos_num_sins (default 64) improves correlation at short lags (consecutive symbols).

    slots_per_channel: advance this many slots between each captured channel matrix
        (default 1). E.g. slots_per_channel=5 with spacing=15 gives one channel every 5 ms.

    sos_type: passed to NeoRadium as sosType ('GMEDS1' or 'Xiao').
    sos_num_sins: passed to NeoRadium as sosNumSins (number of sinusoids; default 64 for
        better within-slot correlation than NeoRadium's default 32).

    With NeoRadium defaults, mean power E[|H|^2] is typically ~1–2 depending on profile
    (path powers are normalized; combined channel power varies with number of paths and tap overlap).

    Returns an array of shape (num_channels, L, K, Nr, Nt) of complex channel matrices.
    """
    random.setSeed(random_seed)
    carrier = Carrier(startRb=start_rb, numRbs=num_rbs, spacing=spacing)
    bwp = carrier.curBwp
    channel = TdlChannel(
        bwp,
        profile,
        carrierFreq=carrier_freq,
        dopplerShift=doppler_shift,
        delaySpread=delay_spread,
        txAntennaCount=tx_antenna_count,
        rxAntennaCount=rx_antenna_count,
        seed=random_seed,
        sosType=sos_type,
        sosNumSins=sos_num_sins,
        **channel_kwargs,
    )

    channel_matrices = []
    iterator = tqdm(range(num_channels), desc="TDL channels") if show_progress else range(num_channels)
    for _ in iterator:
        channel_matrices.append(channel.getChannelMatrix())
        for _ in range(slots_per_channel):
            channel.goNext()


    out = np.array(channel_matrices)
    if normalize_mean_power:
        scale = np.sqrt(np.mean(np.abs(out) ** 2))
        if scale > 0:
            out = out / scale
    return out