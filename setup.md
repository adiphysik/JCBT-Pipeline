# Setup and Installation Guide

## Introduction
This document provides step-by-step instructions to set up and install all dependencies required for running the **Photometric Reduction UI** pipeline. The pipeline is designed for automated photometric data reduction for data obtained from the 1.3m JCB Telescope at VBO, Kavalur.

## Prerequisites
Ensure you have the following installed on your system:
- **Operating System:** Linux/macOS (recommended)
- **Python Version:** Python 3.9 or later (recommended)
- **Package Manager:** `pip` (for installing dependencies)

## Installation Steps

### 1. Install Python
Ensure Python 3.9+ is installed. You can check your version using:
```bash
python3 --version
```
If Python is not installed, download it from [Python's official website](https://www.python.org/) and install it.

### 2. Install Required Python Packages
Install all required dependencies using `pip`:
```bash
pip install numpy pandas astropy photutils matplotlib
```
Some additional system-level dependencies may be required:
```bash
sudo apt-get install python3-tk  # For Tkinter GUI (Linux)
```

### 3. Install IRAF and PyRAF
The pipeline depends on **IRAF** and **PyRAF** for photometry tasks.

#### a) Install IRAF (Linux/macOS)
```bash
sudo apt-get install iraf
```
#### b) Install PyRAF
```bash
pip install pyraf
```
For Linux, a manual IRAF installation may be required. Follow the [IRAF installation guide](https://iraf-community.github.io/install.html).

### 4. Verify Installation
Run the following command to check if all required packages are installed correctly:
```bash
python3 -c "import tkinter, os, platform, subprocess, threading, logging, glob, fnmatch, re, numpy, pandas, astropy.io.fits, astropy.stats, pyraf.iraf, photutils.detection, photutils.background, matplotlib.pyplot; print('All packages installed successfully!')"
```
If no errors appear, the setup is complete.

## Running the Pipeline
Once installed, navigate to the directory containing the pipeline and run:
```bash
python3 main.py
```
This will launch the **Photometric Reduction UI**.

## Troubleshooting
- **IRAF-related errors:** Ensure IRAF is properly installed and accessible in your system path.
- **GUI not opening:** Install Tkinter (`sudo apt-get install python3-tk`).
- **Missing dependencies:** Run `pip install -r requirements.txt`.
