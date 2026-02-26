from matplotlib import pyplot as plt
import numpy as np
import yaml
from pathlib import Path


def load_config(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def save_config(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def plot_channel_distribution(channel_matrices: np.ndarray) -> None:
    _, (ax_real, ax_imag) = plt.subplots(1, 2, figsize=(10, 4))

    ax_real.hist(channel_matrices.real.flatten(), bins=100, color='purple', edgecolor='black', alpha=0.7)
    ax_real.set_title('Real Part')
    ax_real.set_xlabel('Value')
    ax_real.set_ylabel('Frequency')

    ax_imag.hist(channel_matrices.imag.flatten(), bins=100, color='orange', edgecolor='black', alpha=0.7)
    ax_imag.set_title('Imaginary Part')
    ax_imag.set_xlabel('Value')
    ax_imag.set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()

def plot_power_distribution(channel_matrices: np.ndarray) -> None:
    power_distribution = np.abs(channel_matrices)**2
    plt.hist(power_distribution.flatten(), bins=100, color='orange', edgecolor='black', alpha=0.7)
    plt.title('Power Distribution')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()

def plot_angle_magnitude_distribution(channel_matrices: np.ndarray) -> None:
    angle_distribution = np.angle(channel_matrices)
    magnitude_distribution = np.abs(channel_matrices)

    _, (ax_angle, ax_mag) = plt.subplots(1, 2, figsize=(10, 4))

    ax_angle.hist(angle_distribution.flatten(), bins=100, color='purple', edgecolor='black', alpha=0.7)
    ax_angle.set_title('Angle Distribution')
    ax_angle.set_xlabel('Angle (radians)')
    ax_angle.set_ylabel('Frequency')

    ax_mag.hist(magnitude_distribution.flatten(), bins=100, color='orange', edgecolor='black', alpha=0.7)
    ax_mag.set_title('Magnitude Distribution')
    ax_mag.set_xlabel('Magnitude')
    ax_mag.set_ylabel('Frequency')

    plt.tight_layout()
    plt.show()


def plot_power_distribution_and_cdf(
    channel_matrices: np.ndarray, log_scale: bool = False
) -> None:
    """Plot channel power distribution (histogram) and CDF side by side."""
    power = np.abs(channel_matrices) ** 2
    power_flat = power.flatten()

    if log_scale:
        # Plot 10*log10(power) in dB; clip zeros to avoid -inf
        power_flat = 10 * np.log10(np.maximum(power_flat, 1e-20))

    _, (ax_hist, ax_cdf) = plt.subplots(1, 2, figsize=(10, 4))

    ax_hist.hist(power_flat, bins=100, color="orange", edgecolor="black", alpha=0.7)
    ax_hist.set_title("Power Distribution")
    ax_hist.set_xlabel("Power (dB)" if log_scale else "Power")
    ax_hist.set_ylabel("Frequency")

    sorted_power = np.sort(power_flat)
    cdf = np.arange(1, len(sorted_power) + 1) / len(sorted_power)
    ax_cdf.plot(sorted_power, cdf, color="purple", linewidth=1.5)
    ax_cdf.set_title("Power CDF")
    ax_cdf.set_xlabel("Power (dB)" if log_scale else "Power")
    ax_cdf.set_ylabel("CDF")
    ax_cdf.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# Default colors for profile comparison (one per profile, cycled if needed)
_PROFILE_COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]


def _profile_plot_defaults(channels_by_profile, colors):
    """Return (ordered list of (name, array), color list) for profile comparison plots."""
    items = list(channels_by_profile.items())
    n = len(items)
    if colors is None:
        colors = [_PROFILE_COLORS[i % len(_PROFILE_COLORS)] for i in range(n)]
    return items, colors


def plot_profiles_channel_distribution(
    channels_by_profile: dict[str, np.ndarray],
    colors: list[str] | None = None,
) -> None:
    """Plot real/imag channel distribution in a 2 x N grid (one column per profile)."""
    items, colors = _profile_plot_defaults(channels_by_profile, colors)
    n = len(items)
    fig, axes = plt.subplots(2, n, figsize=(2.8 * max(n, 1), 5), squeeze=False)
    for j, (profile, H) in enumerate(items):
        c = colors[j]
        axes[0, j].hist(H.real.flatten(), bins=100, color=c, edgecolor="black", alpha=0.8, density=True)
        axes[0, j].set_title(f"Profile {profile} – Real")
        axes[0, j].set_xlabel("Value")
        axes[0, j].set_ylabel("Density")
        axes[1, j].hist(H.imag.flatten(), bins=100, color=c, edgecolor="black", alpha=0.8, density=True)
        axes[1, j].set_title(f"Profile {profile} – Imag")
        axes[1, j].set_xlabel("Value")
        axes[1, j].set_ylabel("Density")
    plt.suptitle("Channel distribution (real / imaginary)")
    plt.tight_layout()
    plt.show()


def plot_profiles_power_distribution(
    channels_by_profile: dict[str, np.ndarray],
    colors: list[str] | None = None,
) -> None:
    """Plot power distribution in a 1 x N grid (one subplot per profile)."""
    items, colors = _profile_plot_defaults(channels_by_profile, colors)
    n = len(items)
    fig, axes = plt.subplots(1, n, figsize=(2.8 * max(n, 1), 3.5), squeeze=False)
    for j, (profile, H) in enumerate(items):
        power = np.abs(H) ** 2
        axes[0, j].hist(power.flatten(), bins=100, color=colors[j], edgecolor="black", alpha=0.8, density=True)
        axes[0, j].set_title(f"Profile {profile}")
        axes[0, j].set_xlabel("Power")
        axes[0, j].set_ylabel("Density")
    plt.suptitle("Power distribution")
    plt.tight_layout()
    plt.show()


def plot_profiles_angle_magnitude_distribution(
    channels_by_profile: dict[str, np.ndarray],
    colors: list[str] | None = None,
) -> None:
    """Plot angle/magnitude distribution in a 2 x N grid (one column per profile)."""
    items, colors = _profile_plot_defaults(channels_by_profile, colors)
    n = len(items)
    fig, axes = plt.subplots(2, n, figsize=(2.8 * max(n, 1), 5), squeeze=False)
    for j, (profile, H) in enumerate(items):
        c = colors[j]
        axes[0, j].hist(np.angle(H).flatten(), bins=100, color=c, edgecolor="black", alpha=0.8, density=True)
        axes[0, j].set_title(f"Profile {profile} – Angle")
        axes[0, j].set_xlabel("Angle (rad)")
        axes[0, j].set_ylabel("Density")
        axes[1, j].hist(np.abs(H).flatten(), bins=100, color=c, edgecolor="black", alpha=0.8, density=True)
        axes[1, j].set_title(f"Profile {profile} – Magnitude")
        axes[1, j].set_xlabel("Magnitude")
        axes[1, j].set_ylabel("Density")
    plt.suptitle("Angle / magnitude distribution")
    plt.tight_layout()
    plt.show()


def plot_profiles_power_distribution_and_cdf(
    channels_by_profile: dict[str, np.ndarray],
    colors: list[str] | None = None,
    log_scale: bool = True,
) -> None:
    """Plot power (dB) distribution and CDF in a 2 x N grid (one column per profile)."""
    items, colors = _profile_plot_defaults(channels_by_profile, colors)
    n = len(items)
    fig, axes = plt.subplots(2, n, figsize=(2.8 * max(n, 1), 5), squeeze=False)
    for j, (profile, H) in enumerate(items):
        power = np.abs(H) ** 2
        power_flat = power.flatten()
        if log_scale:
            power_flat = 10 * np.log10(np.maximum(power_flat, 1e-20))
        axes[0, j].hist(power_flat, bins=100, color=colors[j], edgecolor="black", alpha=0.8, density=True)
        axes[0, j].set_title(f"Profile {profile} – Power")
        axes[0, j].set_xlabel("Power (dB)" if log_scale else "Power")
        axes[0, j].set_ylabel("Density")
        sorted_power = np.sort(power_flat)
        cdf = np.arange(1, len(sorted_power) + 1) / len(sorted_power)
        axes[1, j].plot(sorted_power, cdf, color=colors[j], linewidth=1.5)
        axes[1, j].set_title(f"Profile {profile} – CDF")
        axes[1, j].set_xlabel("Power (dB)" if log_scale else "Power")
        axes[1, j].set_ylabel("CDF")
        axes[1, j].grid(True, alpha=0.3)
    plt.suptitle("Power (dB) distribution and CDF")
    plt.tight_layout()
    plt.show()