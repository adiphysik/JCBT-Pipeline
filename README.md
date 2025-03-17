Photometric reduction UI:

The code aims to perform the photometric data reduction process for the data obtained from the 1.3 meter JCBT telescope at VBO, Kavalur.
The code automatically performs all the steps involved in photometric reduction of the calibrated data including the Aperture and PSF photometry.
The text file task_logs.log contains the logger information for debugging.

Usage: python pipeline.py

Dependencies: astropy, numpy, pyraf, photutils, IRAFStarFinder, logging, glob  
Install astropy, numpy, photutils --> pip3 install astropy, numpy, photutils  
Install matplotlib --> sudo apt-get install python3-matplotlib  
IRAFStarFinder --> extraction algorithm to detect point-like sources  

UI elements: The UI elements and their functions are given below,

INPUT FILE - It represents the desired calibrated input file to be selected.  
OUTPUT FOLDER - It represents the desired output folder to store the output files.  
ENTRY BAR - It shows the location of the desired input/output folder in the system.  
BROWSE - This button is used to browse the system for desired input/output folders.  
RUN PHOTOMETRY - This button runs the Photometric reduction script.  
SHOW FILES - This button is used to display and access the contents of the folder.  
HELP - This button is to access the Help Menu.  

 
Author : Aditya Bharadwaj  
Email : adiphysik@gmail.com  
Date : 14 / 03 / 2025  
version : 2.0
