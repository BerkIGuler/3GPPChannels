from src.utils import plot_channel_distribution, plot_power_distribution, plot_angle_magnitude_distribution, plot_power_distribution_and_cdf
from src.tdl import generate_tdl_channels


RANDOM_SEED = 123
START_RB = 0
NUM_RBS = 10
SPACING = 15
TX_ANTENNA_COUNT = 1
RX_ANTENNA_COUNT = 1
CARRIER_FREQ = 3.5e9
DOPPLER_SHIFT = 100
DELAY_SPREAD = 500
PROFILE = 'B'
NUM_CHANNELS = 10000
SHOW_PROGRESS = True

channel_matrices = generate_tdl_channels(
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
    profile=PROFILE,
    show_progress=SHOW_PROGRESS,
)

print("Channel matrices shape:", channel_matrices.shape)

plot_channel_distribution(channel_matrices)
plot_power_distribution(channel_matrices)
plot_angle_magnitude_distribution(channel_matrices)
plot_power_distribution_and_cdf(channel_matrices, log_scale=True)