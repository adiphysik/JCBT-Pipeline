# Calibration Workflow

The reduction pipeline performs calibration of RAW astronomical images obtained from the 1.3m JCBT Telescope.
The overall workflow of the calibration process is as shown below,



## 1) RAW Frame Selection

The acquired data from the telescope is in RAW format, stored as .fits files. 
The pipeline scans the data directory and selects only those files with the .fits extension for processing.


## 2) Trimming Overscan Regions

Raw CCD images contain overscan regions that introduce unwanted noise. 
The pipeline utilizes the ccdproc task from IRAF software to remove these overscan regions based on the appropriate trim sections for the specific CCD type.


## 3) Masterbias Frame

To minimize electronic noise and accurately determine the overall detector bias, multiple bias frames are combined into a master bias frame. 
The pipeline implements a statistical filtering method to remove bad bias frames and combines the good ones using the zerocombine task in IRAF.


## 4) Bias Correction

The underlying bias level is removed from all RAW frames by subtracting the master bias frame using the ccdproc task. 
This step ensures a uniform baseline across all images.


## 5) Masterflat Frame

For each filter used during observations, all flat field frames are combined to create a master flat frame. 
This is performed using the flatcombine task in IRAF.


## 6) Flat Field Correction

To correct for pixel-to-pixel variations in detector sensitivity, each image is divided by its corresponding normalized master flat frame using ccdproc task. 
This correction ensures that the brightness and intensity in the images accurately reflect the true signal from the astronomical object.


## Final Output

After performing all these calibration steps, the resulting calibrated frames are ready for photometric analysis.
