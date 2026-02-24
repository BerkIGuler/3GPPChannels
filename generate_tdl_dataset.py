#!/usr/bin/env python3
"""
Generate TDL channel datasets from a YAML config.

For each (delay_spread, max_doppler_shift) pair, generates num_channels_per_config
channel matrices, saves them as .npy with a descriptive filename, and writes
metadata.yaml in the output folder.
"""
import argparse
from pathlib import Path
import numpy as np

from src.tdl import generate_tdl_channels
from src.utils import load_config, save_config


def run(config_path: Path, output_dir: Path) -> None:
    config = load_config(config_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    delay_spreads = config["delay_spreads"]
    max_doppler_shifts = config["max_doppler_shifts"]
    num_channels_per_config = config["num_channels_per_config"]

    base_kwargs = {
        "num_channels": num_channels_per_config,
        "random_seed": config.get("random_seed", 123),
        "start_rb": config.get("start_rb", 0),
        "num_rbs": config.get("num_rbs", 10),
        "spacing": config.get("spacing", 15),
        "tx_antenna_count": config.get("tx_antenna_count", 1),
        "rx_antenna_count": config.get("rx_antenna_count", 1),
        "carrier_freq": config.get("carrier_freq", 3.5e9),
        "profile": config.get("delay_profile", "A"),
        "show_progress": config.get("show_progress", True),
    }

    generated = []
    for delay_spread in delay_spreads:
        for doppler_shift in max_doppler_shifts:
            name = f"delay_spread_{delay_spread}_doppler_{doppler_shift}.npy"
            out_path = output_dir / name
            channels = generate_tdl_channels(
                **base_kwargs,
                delay_spread=delay_spread,
                doppler_shift=doppler_shift,
            )
            np.save(out_path, channels)
            generated.append({
                "file": name,
                "delay_spread_ns": delay_spread,
                "doppler_shift_hz": doppler_shift,
            })

    metadata = {
        "config_path": str(Path(config_path).resolve()),
        "config": config,
        "generated": generated,
    }
    save_config(output_dir / "metadata.yaml", metadata)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate TDL channel datasets from a YAML config."
    )
    parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        default=Path("configs/tdl_dataset.yaml"),
        help="Path to the YAML config file (default: configs/tdl_dataset.yaml)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output/tdl_dataset"),
        help="Output directory for .npy files and metadata.yaml (default: output/tdl_dataset)",
    )
    args = parser.parse_args()
    run(args.config, args.output)


if __name__ == "__main__":
    main()