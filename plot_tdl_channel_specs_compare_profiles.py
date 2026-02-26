import numpy as np

from src.tdl import generate_tdl_channels
from src.utils import (
    plot_profiles_angle_magnitude_distribution,
    plot_profiles_channel_distribution,
    plot_profiles_power_distribution,
    plot_profiles_power_distribution_and_cdf,
)

PROFILES = ["A", "B", "C", "D", "E"]
COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]

RANDOM_SEED = 123
START_RB = 0
NUM_RBS = 10
SPACING = 15
TX_ANTENNA_COUNT = 1
RX_ANTENNA_COUNT = 1
CARRIER_FREQ = 3.5e9
DOPPLER_SHIFT = 100
DELAY_SPREAD = 500
NUM_CHANNELS = 2000
SHOW_PROGRESS = True


def main():
    channels_by_profile = {}
    for profile in PROFILES:
        print(f"Generating channels for profile {profile}...")
        channels_by_profile[profile] = generate_tdl_channels(
            num_channels=NUM_CHANNELS,
            random_seed=RANDOM_SEED,
            start_rb=START_RB,
            num_rbs=NUM_RBS,
            spacing=SPACING,
            tx_antenna_count=TX_ANTENNA_COUNT,
            rx_antenna_count=RX_ANTENNA_COUNT,
            carrier_freq=CARRIER_FREQ,
            doppler_shift=DOPPLER_SHIFT,
            delay_spread=DELAY_SPREAD,
            profile=profile,
            show_progress=SHOW_PROGRESS,
        )
    print("Channel matrices shapes:", {p: c.shape for p, c in channels_by_profile.items()})

    mean_power = {p: np.mean(np.abs(H) ** 2) for p, H in channels_by_profile.items()}
    print("Mean power per profile:")
    for profile in PROFILES:
        print(f"  Profile {profile}: {mean_power[profile]:.6g}")

    plot_profiles_channel_distribution(channels_by_profile, colors=COLORS)
    plot_profiles_power_distribution(channels_by_profile, colors=COLORS)
    plot_profiles_angle_magnitude_distribution(channels_by_profile, colors=COLORS)
    plot_profiles_power_distribution_and_cdf(channels_by_profile, colors=COLORS, log_scale=True)


if __name__ == "__main__":
    main()
