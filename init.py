"""
__init__.py

This file initializes the photometry pipeline package and ensures that all required 
dependencies are available. The package is designed for automated photometric 
data reduction from the 1.3m JCB Telescope.

Modules include:
- GUI (Tkinter-based interface)
- Data Loading (FITS file handling)
- Image Calibration (Bias, Dark, Flat correction)
- Photometry (Aperture/PSF photometry)
- Reduction & Analysis
- Plotting & Visualization
"""

# GUI-related imports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# System and process management
import os
import platform
import subprocess
import threading
import logging
import glob
import fnmatch
import re

# Scientific and numerical computing
import numpy as np
import pandas as pd

# Astropy and FITS file handling
import astropy.io.fits as fits
from astropy.io import fits
from astropy.stats import sigma_clipped_stats

# IRAF and photometry tools
from pyraf import iraf
from photutils.detection import IRAFStarFinder
from photutils import background
from photutils.background import MedianBackground

# Plotting and visualization
import matplotlib.pyplot as plt