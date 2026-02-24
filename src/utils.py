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
