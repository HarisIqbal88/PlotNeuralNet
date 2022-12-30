#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from setuptools import setup, find_packages
    from pathlib import Path
    layerFiles = [str(f) for f in (Path(__file__).parent / "layers").glob("*")]

    setup(
	packages=find_packages(),
	data_files=[("layers", layerFiles)]
	)
