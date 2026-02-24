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
    **channel_kwargs,
) -> np.ndarray:
    """Generate TDL channel matrices over multiple slots.

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
        **channel_kwargs,
    )

    channel_matrices = []
    iterator = tqdm(range(num_channels), desc="TDL channels") if show_progress else range(num_channels)
    for _ in iterator:
        channel_matrices.append(channel.getChannelMatrix())
        channel.goNext()

    return np.array(channel_matrices)