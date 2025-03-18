#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:49:30 2023

@author: bharadwaj
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import logging
import os
import platform
import threading
import astropy.io.fits as fits
import matplotlib.pyplot as plt
        

class PreprocessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JCBT PIPELINE")

        # Changes
        font_small = ('clean', 10, 'bold')
        font_med = ('clean', 12, 'bold')
        font_large = ('clean', 14, 'bold')
        self.root.configure(bg="black")
        #self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.resizable(True,True)
        

        
        #Input folder
        self.input_label = tk.Label(root, text="INPUT FOLDER:", font=font_med, bg="black", fg="white")
        self.input_entry = tk.Entry(root, width=25, font=font_small, bg="black", fg="white")
        self.input_button = tk.Button(root, text="BROWSE", font=font_med, relief=tk.RAISED, command=self.select_input_folder, bg="black", fg="lime", activebackground="green", activeforeground="white")

        #Output folder
        self.output_label = tk.Label(root, text="OUTPUT FOLDER:", font=font_med, bg="black", fg="white")
        self.output_entry = tk.Entry(root, width=25, font=font_small, bg="black", fg="white")
        self.output_button = tk.Button(root, text="BROWSE", font=font_med, relief=tk.RAISED, command=self.select_output_folder, bg="black", fg="lime", activebackground="green", activeforeground="white")

        self.run_button = tk.Button(root, text="RUN PREPROCESSING", font=font_large, relief=tk.RAISED, command=self.run_preprocessing, bg="red",fg="white", activebackground="green", activeforeground="white")


        # Create a progress bar
        self.style = ttk.Style()
        self.style.configure("Custom.Horizontal.TProgressbar", troughcolor="black", background="green")
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress_bar.grid(row=3, columnspan=3, padx=10, pady=10)

        # Create a label for the percentage indicator
        self.percentage_label = tk.Label(root, text="", font=font_small, bg="black", fg="lime")
        self.percentage_label.grid(row=3, columnspan=3)


        # Set up layout using grid
        self.input_label.grid(row=0, column=0, padx=10, pady=10)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)
        self.input_button.grid(row=0, column=2, padx=10, pady=10)

        self.output_label.grid(row=1, column=0, padx=10, pady=10)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10)
        self.output_button.grid(row=1, column=2, padx=10, pady=10)

        self.run_button.grid(row=2, columnspan=3, padx=10, pady=10)

        # Configure column and row weights for resizing
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(20):
            self.root.grid_rowconfigure(i, weight=1)

        # Add a horizontal line after the preprocessing section
        ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=4, columnspan=3, sticky="ew", padx=10, pady=10)


        # Initialize variables
        self.input_dir = ""
        self.output_dir = ""  



    def select_input_folder(self):
        self.input_dir = filedialog.askdirectory()
        if self.input_dir:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.input_dir)

    def select_output_folder(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, self.output_dir)
            

    def run_preprocessing(self):
        if not self.input_dir or not self.output_dir:
            messagebox.showerror("Error", "Please select input and output directories.")
            return
        
        try:
            # Your preprocessing logic here
            self.perform_preprocessing()

            messagebox.showinfo("Success", "Preprocessing completed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")



        """
        Sorting and Listing
        
        """
    

    def perform_preprocessing(self):
        
        import os
        import fnmatch
        import numpy as np
        from astropy.io import fits
        from pyraf import iraf
        import logging


        # Change to required working directory
        print("Current working directory: {0}".format(os.getcwd()))
        os.chdir(self.input_dir)
        print("Changed to this directory: {0}".format(os.getcwd()))
        print()


        # Directory containing fits files
        #directory = "./"
        # Get all the files in the directory
        files = os.listdir()

        # Iterate over the files
        for file_name in files:
            if file_name.endswith("_t.fits"):
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if file_name.endswith("_tb.fits"):
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if file_name.endswith("_tbf.fits"):
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if ".coo" in file_name:
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if ".pst" in file_name:
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if ".mag" in file_name:
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if ".psg" in file_name:
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if ".psf" in file_name:
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if ".sub" in file_name:
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if ".arj" in file_name:
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
            if ".als" in file_name:
                file_path = os.path.join(self.input_dir,file_name)
                os.remove(file_path)
                
            


        # Create and configure logger
        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("task_logs.log")):
                os.remove("task_logs.log")
            if (os.path.exists("logfile")):
                os.remove("logfile")

        logging.basicConfig(level=logging.DEBUG,
                            filename="task_logs.log",
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            filemode='w')

        # Creating an object
        logger = logging.getLogger('task_logger')

        # Create a file handler and set its level to DEBUG
        file_handler = logging.FileHandler('task_logs.log')
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter and add it to the file handler
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)


        # Remove existing lists
        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("biaslist")):
                os.remove("biaslist")
            if (os.path.exists("flatlist")):
                os.remove("flatlist")
            if (os.path.exists("objectlist")):
                os.remove("objectlist")
            if (os.path.exists("obj_B")):
                os.remove("obj_B")
            if (os.path.exists("obj_V")):
                os.remove("obj_V")
            if (os.path.exists("obj_R")):
                os.remove("obj_R")
            if (os.path.exists("obj_I")):
                os.remove("obj_I")
            if (os.path.exists("obj_ha")):
                os.remove("obj_ha")
            if (os.path.exists("obj_hb")):
                os.remove("obj_hb")
            if (os.path.exists("obj_U")):
                os.remove("obj_U")
            if (os.path.exists("obj_O")):
                os.remove("obj_O")
            if (os.path.exists("obj_6724")):
                os.remove("obj_6724")
            if (os.path.exists("flat_B")):
                os.remove("flat_B")
            if (os.path.exists("flat_V")):
                os.remove("flat_V")
            if (os.path.exists("flat_R")):
                os.remove("flat_R")
            if (os.path.exists("flat_I")):
                os.remove("flat_I")
            if (os.path.exists("flat_ha")):
                os.remove("flat_ha")
            if (os.path.exists("flat_hb")):
                os.remove("flat_hb")
            if (os.path.exists("flat_U")):
                os.remove("flat_U")
            if (os.path.exists("flat_O")):
                os.remove("flat_O")
            if (os.path.exists("flat_6724")):
                os.remove("flat_6724")
        

        total_tasks = 6  # The total number of tasks in your script
        # Create batch lists
        bias_list = []
        flats_list = []
        objects_list = []
        obj_B_list = []
        obj_V_list = []
        obj_R_list = []
        obj_I_list = []
        obj_ha_list = []
        obj_hb_list = []
        obj_U_list = []
        obj_O_list = []
        obj_6724_list = []
        flat_B_list = []
        flat_V_list = []
        flat_R_list = []
        flat_I_list = []
        flat_ha_list = []
        flat_hb_list = []
        flat_U_list = []
        flat_O_list = []
        flat_6724_list = []
        all_files_list = []



        # Iterate over files in the directory
        for filename in sorted(os.listdir(self.input_dir)):
            if filename.endswith(".fits"):
                filepath = os.path.join(filename)
                all_files_list.append(filename)
                
                # Read FITS header
                with fits.open(filepath) as hdul:
                    header = hdul[0].header
                    
                    # Get IMAGETYP and FILTER values
                    imagetyp = header.get('IMAGETYP', '').lower()
                    filter_value = header.get('FILTER', '').upper()
                    
                    # Add file to the appropriate batch list
                    if imagetyp == 'zero':
                        bias_list.append(filename)
                        
                    elif imagetyp == 'flat':
                        flats_list.append(filename)
                        if filter_value == 'B':
                            flat_B_list.append(filename)
                        elif filter_value == 'V':
                            flat_V_list.append(filename)
                        elif filter_value == 'R':
                            flat_R_list.append(filename)
                        elif filter_value == 'I':
                            flat_I_list.append(filename)
                        elif filter_value == 'U':
                            flat_U_list.append(filename)    
                        elif filter_value in ['6563/50A', '6563/50', '6563','6563/100A','6563/100']:
                            flat_ha_list.append(filename)
                        elif filter_value in ['5120/100A','5120/100','5120']:
                            flat_hb_list.append(filename)
                        elif filter_value in ['5007/80A','5007/80', '5007']:
                            flat_O_list.append(filename)
                        elif filter_value in ['6724/70A','6724/70','6724']:
                            flat_6724_list.append(filename)
                        
                        
                    elif imagetyp == 'object':
                        objects_list.append(filename) 
                        if filter_value == 'B':
                            obj_B_list.append(filename)
                        elif filter_value == 'V':
                            obj_V_list.append(filename)
                        elif filter_value == 'R':
                            obj_R_list.append(filename)
                        elif filter_value == 'I':
                            obj_I_list.append(filename)
                        elif filter_value == 'U':
                            obj_U_list.append(filename)    
                        elif filter_value in ['6563/50A', '6563/50', '6563','6563/100A','6563/100']:
                            obj_ha_list.append(filename)
                        elif filter_value in ['5120/100A','5120/100','5120']:
                            obj_hb_list.append(filename)
                        elif filter_value in ['5007/80A','5007/80', '5007']:
                            obj_O_list.append(filename)
                        elif filter_value in ['6724/70A','6724/70','6724']:
                            obj_6724_list.append(filename)
                        
                            
                            
        # Write batch lists to text files only if files are present
        if bias_list:
            with open("biaslist", "w") as bias_file:
                bias_file.write("\n".join(bias_list))

        if flats_list:
            with open("flatlist", "w") as flats_file:
                flats_file.write("\n".join(flats_list))

        if objects_list:
            with open("objectlist", "w") as objects_file:
                objects_file.write("\n".join(objects_list))

        if obj_B_list:
            with open("obj_B", "w") as obj_B_file:
                obj_B_file.write("\n".join(obj_B_list))

        if obj_V_list:
            with open("obj_V", "w") as obj_V_file:
                obj_V_file.write("\n".join(obj_V_list))

        if obj_R_list:
            with open("obj_R", "w") as obj_R_file:
                obj_R_file.write("\n".join(obj_R_list))

        if obj_I_list:
            with open("obj_I", "w") as obj_I_file:
                obj_I_file.write("\n".join(obj_I_list))
                
        if obj_U_list:
            with open("obj_U", "w") as obj_U_file:
                obj_U_file.write("\n".join(obj_U_list))        
                
        if obj_ha_list:
            with open("obj_ha", "w") as obj_ha_file:
                obj_ha_file.write("\n".join(obj_ha_list))
                
        if obj_hb_list:
            with open("obj_hb", "w") as obj_hb_file:
                obj_hb_file.write("\n".join(obj_hb_list))
                
        if obj_O_list:
            with open("obj_O", "w") as obj_O_file:
                obj_O_file.write("\n".join(obj_O_list))
                
        if obj_6724_list:
            with open("obj_6724", "w") as obj_6724_file:
                obj_6724_file.write("\n".join(obj_6724_list))

        if flat_B_list:
            with open("flat_B", "w") as flat_B_file:
                flat_B_file.write("\n".join(flat_B_list))

        if flat_V_list:
            with open("flat_V", "w") as flat_V_file:
                flat_V_file.write("\n".join(flat_V_list))
                
        if flat_R_list:
            with open("flat_R", "w") as flat_R_file:
                flat_R_file.write("\n".join(flat_R_list))
                
        if flat_I_list:
            with open("flat_I", "w") as flat_I_file:
                flat_I_file.write("\n".join(flat_I_list))
                
        if flat_U_list:
            with open("flat_U", "w") as flat_U_file:
                flat_U_file.write("\n".join(flat_U_list))        
                
        if flat_ha_list:
            with open("flat_ha", "w") as flat_ha_file:
                flat_ha_file.write("\n".join(flat_ha_list))
                
        if flat_hb_list:
            with open("flat_hb", "w") as flat_hb_file:
                flat_hb_file.write("\n".join(flat_hb_list))
                
        if flat_O_list:
            with open("flat_O", "w") as flat_O_file:
                flat_O_file.write("\n".join(flat_O_list))
                
        if flat_6724_list:
            with open("flat_6724", "w") as flat_6724_file:
                flat_6724_file.write("\n".join(flat_6724_list))
                
                
        # Write all files to a text file
        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("op_list")):
                os.remove("op_list")
        with open("op_list", "w") as all_files_file:
            all_files_file.write("\n".join(all_files_list))

                
        # To check the existence of flat frames in the directory 
        if (os.path.exists("flat_B")):
            print('flat frames in B filter are found')
            logger.info('flat frames in B filter are found')
        else:
            print('no flat frames in B filter found')
            logger.warning('no flat frames in B filter found')
                   
        if (os.path.exists("flat_V")):
            print('flat frames in V filter are found')
            logger.info('flat frames in V filter are found')
        else:
            print('no flat frames in V filter found')
            logger.warning('no flat frames in V filter found')
                
        if (os.path.exists("flat_R")):
            print('flat frames in R filter are found')
            logger.info('flat frames in R filter are found')
        else:
            print('no flat frames in R filter found')
            logger.warning('no flat frames in R filter found')

        if (os.path.exists("flat_I")):
            print('flat frames in I filter are found')
            logger.info('flat frames in I filter are found')
        else:
            print('no flat frames in I filter found')
            logger.warning('no flat frames in I filter found')
            
        if (os.path.exists("flat_U")):
            print('flat frames in U filter are found')
            logger.info('flat frames in U filter are found')
        else:
            print('no flat frames in U filter found')
            logger.warning('no flat frames in U filter found')    

        if (os.path.exists("flat_ha")):
            print('flat frames in Ha filter are found')
            logger.info('flat frames in Ha filter are found')
        else:
            print('no flat frames in Ha filter found')
            logger.warning('no flat frames in Ha filter found')

        if (os.path.exists("flat_hb")):
            print('flat frames in Hb filter are found')
            logger.info('flat frames in Hb filter are found')
        else:
            print('no flat frames in Hb filter found')
            logger.warning('no flat frames in Hb filter found')
            
        if (os.path.exists("flat_O")):
            print('flat frames in O filter are found')
            logger.info('flat frames in O filter are found')
        else:
            print('no flat frames in O filter found')
            logger.warning('no flat frames in O filter found')
            
        if (os.path.exists("flat_6724")):
            print('flat frames in 6724 filter are found')
            logger.info('flat frames in 6724 filter are found')
        else:
            print('no flat frames in 6724 filter found')
            logger.warning('no flat frames in 6724 filter found')

        print()

        # To check the existence of object frames in the directory
        if (os.path.exists("obj_B")):
            print('object frames in B filter are found')
            logger.info('object frames in B filter are found')
        else:
            print('no object frames in B filter found')
            logger.warning('no object frames in B filter found')
                   
        if (os.path.exists("obj_V")):
            print('object frames in V filter are found')
            logger.info('object frames in V filter are found')
        else:
            print('no object frames in V filter found')
            logger.warning('no object frames in V filter found')
                
        if (os.path.exists("obj_R")):
            print('object frames in R filter are found')
            logger.info('object frames in R filter are found')
        else:
            print('no object frames in R filter found')
            logger.warning('no object frames in R filter found')

        if (os.path.exists("obj_I")):
            print('object frames in I filter are found')
            logger.info('object frames in I filter are found')
        else:
            print('no object frames in I filter found')
            logger.warning('no object frames in I filter found')
            
        if (os.path.exists("obj_U")):
            print('object frames in U filter are found')
            logger.info('object frames in U filter are found')
        else:
            print('no object frames in U filter found')
            logger.warning('no object frames in U filter found')    

        if (os.path.exists("obj_ha")):
            print('object frames in Ha filter are found')
            logger.info('object frames in Ha filter are found')
        else:
            print('no object frames in Ha filter found')
            logger.warning('no object frames in Ha filter found')

        if (os.path.exists("obj_hb")):
            print('object frames in Hb filter are found')
            logger.info('object frames in Hb filter are found')
        else:
            print('no object frames in Hb filter found')
            logger.warning('no object frames in Hb filter found')
            
        if (os.path.exists("obj_O")):
            print('object frames in O filter are found')
            logger.info('object frames in O filter are found')
        else:
            print('no object frames in O filter found')
            logger.warning('no object frames in O filter found')
            
        if (os.path.exists("obj_6724")):
            print('object frames in 6724 filter are found')
            logger.info('object frames in 6724 filter are found')
        else:
            print('no object frames in 6724 filter found')
            logger.warning('no object frames in 6724 filter found')
        
        print()
         



        """ Removing bad bias frames """


        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("biaslist_filtered")):
                os.remove("biaslist_filtered")

        def calculate_stats(fits_file):
            hdulist = fits.open(fits_file)
            data = hdulist[0].data
            stddev = np.std(data)
            mean = np.mean(data)
            hdulist.close()
            return stddev,mean

        # Read the text file containing the list of FITS files
        input_file = 'biaslist'
        output_list = 'biaslist_filtered'

        # Check if the filtered batch list file already exists
        if os.path.exists(output_list):
            with open(output_list, 'r') as file:
                batch_list = file.read().splitlines()
        else:
            with open(input_file, 'r') as file:
                batch_list = file.read().splitlines()
            
        stddev_values = []
        mean_values = []
        file_paths = []

        # Loop over the files in the list
        for fits_file in batch_list:
            # Calculate the standard deviation and mean
            stddev, mean = calculate_stats(fits_file)
            print(f"{fits_file}: Stddev = {stddev}, Mean = {mean}")
            #logger.debug(f"{fits_file}: Stddev = {stddev}, Mean = {mean}")

            stddev_values.append(stddev)
            mean_values.append(mean)
            file_paths.append(fits_file)
        print()    
                    
        # Calculate the median of the standard deviation values
        stddev_median = np.median(stddev_values)
        print("Median of Standard Deviations:", stddev_median)
        #logger.debug("Median of Standard Deviations:", stddev_median)

        # Calculate the standard deviation of the mean values
        mean_values_stddev = np.std(mean_values)
        print("Standard Deviation of Mean Values:", mean_values_stddev)
        #logger.debug("Standard Deviation of Mean Values:", mean_values_stddev)

        print()

        # Calculate the difference between median of stddev values and stddev of individual fits files
        differences = np.abs(stddev_median - stddev_values)

        # Set the threshold for excluding files based on the difference
        threshold = 2  # Adjust this value as desired

        # Find the indices of the FITS files exceeding the threshold difference
        excluded_indices = [i for i, diff in enumerate(differences) if diff > threshold]

        # Create a new batch list with FITS files that are not excluded
        biaslist_filtered = [fits_file for i, fits_file in enumerate(batch_list) if i not in excluded_indices]

        # Store the filtered batch list in a text file
        with open(output_list, 'w') as file:
            for fits_file in biaslist_filtered:
                file.write(fits_file + '\n')

        # Print the excluded files
        print("Excluded files:")
        for excluded_index in sorted(excluded_indices, reverse=True):
            print(file_paths[excluded_index])

        print()    
        print(f"Filtered batch list saved to '{output_list}'.")
        logger.info(f"Filtered batch list saved to '{output_list}'.")

        #input('Press Enter to Continue...')
        print()

        # Recalculate the standard deviation of mean values and the median of the standard deviation of the remaining FITS files
        mean_values = [mean_values[i] for i in range(len(mean_values)) if i not in excluded_indices]
        stddev_values_remaining = [stddev_values[i] for i in range(len(stddev_values)) if i not in excluded_indices]
        #mean_values_stddev_remaining = np.std(mean_values)
        stddev_median_remaining = np.median(stddev_values_remaining)

        #print("Standard Deviation of Mean Values (After Exclusion):", mean_values_stddev_remaining)
        #logger.debug("Standard Deviation of Mean Values (After Exclusion):", mean_values_stddev_remaining)
        print("Median of Standard Deviation (After Exclusion):", stddev_median_remaining)
        #logger.debug("Median of Standard Deviation (After Exclusion):", stddev_median_remaining)
        print()
        
        self.update_progress(1, total_tasks)



                
        """
        Start of Pre-processing

        """

        # Packages required
        iraf.noao(_doprint=0)
        iraf.imred(_doprint=0)
        iraf.ccdred(_doprint=0)
        iraf.echelle(_doprint=0)


        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("op_t")):
                os.remove("op_t")
                
        with open ('op_list','r') as i:
            op = i.read()
            op = op.replace('.fits','_t.fits')
        with open ('op_t', 'w') as k:
            k.write(op)
            k.close()
            


        """ Task 1 - Trimming """



        # Set parameters for ccdproc task to perform trimming
        try:
            logger.info("Started trimming task")
            iraf.ccdproc.setParam('images','@op_list')
            iraf.ccdproc.setParam('output','@op_t')
            iraf.ccdproc.setParam('trim','yes')
            iraf.ccdproc.setParam('trimsec','[50:2100,5:4090]')
            iraf.ccdproc.setParam('zerocor','no')
            iraf.ccdproc.setParam('flatcor','no')
            iraf.ccdproc.setParam('zero','')
            iraf.ccdproc.setParam('flat','')
            #iraf.ccdproc.eParam()
            iraf.ccdproc()
            logger.debug("op_list is trimmed and listed in op_t")
            print("op_list is trimmed and listed in op_t")
            self.update_progress(2, total_tasks)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        print()



        """Task 2 - Making Masterbias """
        

        # Creating a list with only trimmed bias frames 
        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("bias_t")):
                os.remove("bias_t")
                
        for file in sorted(os.listdir(self.input_dir)):
            if (fnmatch.fnmatch(file,'*_bias_*_t.fits')):
                with open("bias_t",mode='a+') as a:
                    b = os.path.join(file)
                    a.write (str(b) + os.linesep)
                    a.close()

        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("masterbias_t.fits")):
                os.remove("masterbias_t.fits")


        # Set parameters for zerocombine task to combine bias frames
        try:
            logger.info("Started combining the bias frames")
            iraf.zerocombine.setParam('input','@bias_t')
            iraf.zerocombine.setParam('output','masterbias_t.fits')
            iraf.zerocombine.setParam('combine','average')
            iraf.zerocombine.setParam('rdnoise','4.1')
            iraf.zerocombine.setParam('gain','0.75')
            #iraf.zerocombine.eParam()
            iraf.zerocombine()
            logger.debug("bias frames are combined to create masterbias_t.fits")
            print("bias frames are combined to create masterbias_t.fits")
            self.update_progress(3, total_tasks)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        print()
        print()

        #statistics of combined masterbias frame
        iraf.imstat.setParam('images','masterbias_t.fits')
        #iraf.imstat.eParam()
        iraf.imstat()
        print()



        """Task 3 - Bias Correction """


        # Creating a list with only the trimmed object and flat frames
        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("op1_t")):
                os.remove("op1_t")

        # Read FITS header
        # with fits.open(filepath) as hdul:
        #     header = hdul[0].header
    

        for file in sorted(os.listdir(self.input_dir)):
            if file.endswith('_t.fits'):
                filepath = os.path.join(self.input_dir, file)
                with fits.open(filepath) as hdul:
                    header = hdul[0].header
                    imagetyp = header.get('IMAGETYP', '').lower()
                    if imagetyp in ['object', 'flat']:
                        with open("op1_t",mode='a+') as a:
                            b = os.path.join(file)
                            a.write (str(b) + os.linesep)
                            a.close()
         
        # Editing the list to populate the bias-corrected frames
        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("op1_tb")):
                os.remove("op1_tb")    

        with open ('op1_t','r') as p:
            q = p.read()
            q = q.replace('_t.fits','_tb.fits')

        with open ('op1_tb', 'a+') as r:
            r.write(q)
            r.close()   




        # Set parameters for ccdproc task to perform bias correction of objects and flat frames
        try:
            logger.info("Started bias correction task")
            iraf.ccdproc.setParam('images','@op1_t')
            iraf.ccdproc.setParam('output','@op1_tb')
            iraf.ccdproc.setParam('trim','no')
            iraf.ccdproc.setParam('zerocor','yes')
            iraf.ccdproc.setParam('flatcor','no')
            iraf.ccdproc.setParam('zero','masterbias_t.fits')
            iraf.ccdproc.setParam('flat','')
            #iraf.ccdproc.eParam()
            iraf.ccdproc()
            logger.debug("list op1_t is bias corrected and listed in op1_tb")
            print("list op1_t is bias corrected and listed in op1_tb")
            self.update_progress(4, total_tasks)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        print() 
        print()




        """Task 4 - Creating Masterflat """


        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("flat_B_tb")):
                os.remove("flat_B_tb")
            if (os.path.exists("flat_V_tb")):
                os.remove("flat_V_tb")
            if (os.path.exists("flat_R_tb")):
                os.remove("flat_R_tb")
            if (os.path.exists("flat_I_tb")):
                os.remove("flat_I_tb")
            if (os.path.exists("flat_U_tb")):
                os.remove("flat_U_tb")    
            if (os.path.exists("flat_ha_tb")):
                os.remove("flat_ha_tb")
            if (os.path.exists("flat_hb_tb")):
                os.remove("flat_hb_tb")
            if (os.path.exists("flat_O_tb")):
                os.remove("flat_O_tb")
            if (os.path.exists("flat_6724_tb")):
                os.remove("flat_6724_tb")

        if (os.path.exists("flat_B")):
            with open ('flat_B','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_B_tb', 'a+') as r:
                r.write(q)
                r.close()
            
        if (os.path.exists("flat_V")):
            with open ('flat_V','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_V_tb', 'a+') as r:
                r.write(q)
                r.close() 

        if (os.path.exists("flat_R")):
            with open ('flat_R','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_R_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("flat_I")):
            with open ('flat_I','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_I_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("flat_U")):
            with open ('flat_U','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_U_tb', 'a+') as r:
                r.write(q)
                r.close()        
                
        if (os.path.exists("flat_ha")):
            with open ('flat_ha','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_ha_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("flat_hb")):
            with open ('flat_hb','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_hb_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("flat_O")):
            with open ('flat_O','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_O_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("flat_6724")):
            with open ('flat_6724','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('flat_6724_tb', 'a+') as r:
                r.write(q)
                r.close()


        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("masterflat_B_tb.fits")):
                os.remove("masterflat_B_tb.fits")
            if (os.path.exists("masterflat_V_tb.fits")):
                os.remove("masterflat_V_tb.fits")
            if (os.path.exists("masterflat_R_tb.fits")):
                os.remove("masterflat_R_tb.fits")
            if (os.path.exists("masterflat_I_tb.fits")):
                os.remove("masterflat_I_tb.fits")
            if (os.path.exists("masterflat_U_tb.fits")):
                os.remove("masterflat_U_tb.fits")    
            if (os.path.exists("masterflat_ha_tb.fits")):
                os.remove("masterflat_ha_tb.fits")
            if (os.path.exists("masterflat_hb_tb.fits")):
                os.remove("masterflat_hb_tb.fits")
            if (os.path.exists("masterflat_O_tb.fits")):
                os.remove("masterflat_O_tb.fits")
            if (os.path.exists("masterflat_6724_tb.fits")):
                os.remove("masterflat_6724_tb.fits")


        # Set parameters for flatcombine task to combine flat frames according to their filters
        logger.info("Started combining flat frames according to filters")
        try:
            if (os.path.exists('flat_B_tb')):
                iraf.flatcombine.setParam('input','@flat_B_tb')
                iraf.flatcombine.setParam('output','masterflat_B_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in B filter are combined to create masterflat_B_tb.fits")
                print("flat frames in B filter are combined to create masterflat_B_tb.fits")
                print()
            
            if (os.path.exists('flat_V_tb')):
                iraf.flatcombine.setParam('input','@flat_V_tb')
                iraf.flatcombine.setParam('output','masterflat_V_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in V filter are combined to create masterflat_V_tb.fits")
                print("flat frames in V filter are combined to create masterflat_V_tb.fits")
                print()
            
            if (os.path.exists('flat_R_tb')):
                iraf.flatcombine.setParam('input','@flat_R_tb')
                iraf.flatcombine.setParam('output','masterflat_R_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in R filter are combined to create masterflat_R_tb.fits")
                print("flat frames in R filter are combined to create masterflat_R_tb.fits")
                print()
            
            if (os.path.exists('flat_I_tb')):
                iraf.flatcombine.setParam('input','@flat_I_tb')
                iraf.flatcombine.setParam('output','masterflat_I_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in I filter are combined to create masterflat_I_tb.fits")
                print("flat frames in I filter are combined to create masterflat_I_tb.fits")
                print()
                
            if (os.path.exists('flat_U_tb')):
                iraf.flatcombine.setParam('input','@flat_U_tb')
                iraf.flatcombine.setParam('output','masterflat_U_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in U filter are combined to create masterflat_U_tb.fits")
                print("flat frames in U filter are combined to create masterflat_U_tb.fits")
                print()    
            
            if (os.path.exists('flat_ha_tb')):
                iraf.flatcombine.setParam('input','@flat_ha_tb')
                iraf.flatcombine.setParam('output','masterflat_ha_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in Ha filter are combined to create masterflat_ha_tb.fits")
                print("flat frames in Ha filter are combined to create masterflat_Ha_tb.fits")
                print()
            
            if (os.path.exists('flat_hb_tb')):
                iraf.flatcombine.setParam('input','@flat_hb_tb')
                iraf.flatcombine.setParam('output','masterflat_hb_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in Hb filter are combined to create masterflat_hb_tb.fits")
                print("flat frames in Hb filter are combined to create masterflat_Hb_tb.fits")
                print()
                
            if (os.path.exists('flat_O_tb')):
                iraf.flatcombine.setParam('input','@flat_O_tb')
                iraf.flatcombine.setParam('output','masterflat_O_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in O filter are combined to create masterflat_O_tb.fits")
                print("flat frames in O filter are combined to create masterflat_O_tb.fits")
                print()
                
            if (os.path.exists('flat_6724_tb')):
                iraf.flatcombine.setParam('input','@flat_6724_tb')
                iraf.flatcombine.setParam('output','masterflat_6724_tb.fits')
                iraf.flatcombine.setParam('combine','median')
                iraf.flatcombine.setParam('reject','crreject')
                iraf.flatcombine.setParam('rdnoise','4.1')
                iraf.flatcombine.setParam('gain','0.75')
                #iraf.flatcombine.eParam()
                iraf.flatcombine()
                logger.debug("flat frames in 6724 filter are combined to create masterflat_6724_tb.fits")
                print("flat frames in 6724 filter are combined to create masterflat_6724_tb.fits")
                print()
                
            self.update_progress(5, total_tasks)        
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        print()


        # Statistics of combined masterflat frames
        if (os.path.exists('masterflat_B_tb.fits')):
            iraf.imstat.setParam('images','masterflat_B_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()

        if (os.path.exists('masterflat_V_tb.fits')):
            iraf.imstat.setParam('images','masterflat_V_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()

        if (os.path.exists('masterflat_R_tb.fits')):
            iraf.imstat.setParam('images','masterflat_R_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()

        if (os.path.exists('masterflat_I_tb.fits')):
            iraf.imstat.setParam('images','masterflat_I_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()
            
        if (os.path.exists('masterflat_U_tb.fits')):
            iraf.imstat.setParam('images','masterflat_U_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()    

        if (os.path.exists('masterflat_ha_tb.fits')):
            iraf.imstat.setParam('images','masterflat_ha_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()

        if (os.path.exists('masterflat_hb_tb.fits')):
            iraf.imstat.setParam('images','masterflat_hb_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()
            
        if (os.path.exists('masterflat_O_tb.fits')):
            iraf.imstat.setParam('images','masterflat_O_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()
        
        if (os.path.exists('masterflat_6724_tb.fits')):
            iraf.imstat.setParam('images','masterflat_6724_tb.fits')
            #iraf.imstat.eParam()
            iraf.imstat()

        print()
        
        

        """ Task 6 - Flat Correction """

        # Editing the object list to populate the bias-corrected frames
        for file in sorted(os.listdir(self.input_dir)):
            if (os.path.exists("obj_B_tb")):
                os.remove("obj_B_tb")
            if (os.path.exists("obj_V_tb")):
                os.remove("obj_V_tb")
            if (os.path.exists("obj_R_tb")):
                os.remove("obj_R_tb")
            if (os.path.exists("obj_I_tb")):
                os.remove("obj_I_tb")
            if (os.path.exists("obj_U_tb")):
                os.remove("obj_U_tb")    
            if (os.path.exists("obj_ha_tb")):
                os.remove("obj_ha_tb")
            if (os.path.exists("obj_hb_tb")):
                os.remove("obj_hb_tb")
            if (os.path.exists("obj_O_tb")):
                os.remove("obj_O_tb")
            if (os.path.exists("obj_6724_tb")):
                os.remove("obj_6724_tb")
            
               
            if (os.path.exists("obj_B_tbf")):
                os.remove("obj_B_tbf")
            if (os.path.exists("obj_V_tbf")):
                os.remove("obj_V_tbf")
            if (os.path.exists("obj_R_tbf")):
                os.remove("obj_R_tbf")
            if (os.path.exists("obj_I_tbf")):
                os.remove("obj_I_tbf")
            if (os.path.exists("obj_U_tbf")):
                os.remove("obj_U_tbf")    
            if (os.path.exists("obj_ha_tbf")):
                os.remove("obj_ha_tbf")
            if (os.path.exists("obj_hb_tbf")):
                os.remove("obj_hb_tbf")
            if (os.path.exists("obj_O_tbf")):
                os.remove("obj_O_tbf")
            if (os.path.exists("obj_6724_tbf")):
                os.remove("obj_6724_tbf")
            


        if (os.path.exists("obj_B")):
            with open ('obj_B','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_B_tb', 'a+') as r:
                r.write(q)
                r.close()
            
        if (os.path.exists("obj_V")):
            with open ('obj_V','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_V_tb', 'a+') as r:
                r.write(q)
                r.close() 

        if (os.path.exists("obj_R")):
            with open ('obj_R','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_R_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_I")):
            with open ('obj_I','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_I_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_U")):
            with open ('obj_U','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_U_tb', 'a+') as r:
                r.write(q)
                r.close()        
                
        if (os.path.exists("obj_ha")):
            with open ('obj_ha','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_ha_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_hb")):
            with open ('obj_hb','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_hb_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_O")):
            with open ('obj_O','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_O_tb', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_6724")):
            with open ('obj_6724','r') as p:
                q = p.read()
                q = q.replace('.fits','_tb.fits')
            with open ('obj_6724_tb', 'a+') as r:
                r.write(q)
                r.close()



        # Editing the object list to populate the flat-corrected frames
        if (os.path.exists("obj_B_tb")):
            with open ('obj_B_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_B_tbf', 'a+') as r:
                r.write(q)
                r.close()
            
        if (os.path.exists("obj_V_tb")):
            with open ('obj_V_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_V_tbf', 'a+') as r:
                r.write(q)
                r.close() 

        if (os.path.exists("obj_R_tb")):
            with open ('obj_R_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_R_tbf', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_I_tb")):
            with open ('obj_I_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_I_tbf', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_U_tb")):
            with open ('obj_U_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_U_tbf', 'a+') as r:
                r.write(q)
                r.close()        
                
        if (os.path.exists("obj_ha_tb")):
            with open ('obj_ha_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_ha_tbf', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_hb_tb")):
            with open ('obj_hb_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_hb_tbf', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_O_tb")):
            with open ('obj_O_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_O_tbf', 'a+') as r:
                r.write(q)
                r.close()
                
        if (os.path.exists("obj_6724_tb")):
            with open ('obj_6724_tb','r') as p:
                q = p.read()
                q = q.replace('_tb.fits','_tbf.fits')
            with open ('obj_6724_tbf', 'a+') as r:
                r.write(q)
                r.close()




        # Set parameters for ccdproc task to perform flat correction of object frames
        logger.info("Started flat correction task")
        try:
            if os.path.exists('obj_B_tb') and os.path.exists('masterflat_B_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_B_tb')
                iraf.ccdproc.setParam('output','@obj_B_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_B_tb.fits')
                #iraf.ccdproc.setParam('trimsec','[1:2051,1:4086]')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_B_tb is flat corrected and listed in obj_B_tbf")
                print("list obj_B_tb is flat corrected and listed in obj_B_tbf")
                print()
            
            if os.path.exists('obj_V_tb') and os.path.exists('masterflat_V_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_V_tb')
                iraf.ccdproc.setParam('output','@obj_V_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_V_tb.fits')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_V_tb is flat corrected and listed in obj_V_tbf")
                print("list obj_V_tb is flat corrected and listed in obj_V_tbf")
                print()
            
            if os.path.exists('obj_R_tb') and os.path.exists('masterflat_R_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_R_tb')
                iraf.ccdproc.setParam('output','@obj_R_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_R_tb.fits')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_R_tb is flat corrected and listed in obj_R_tbf")
                print("list obj_R_tb is flat corrected and listed in obj_R_tbf")
                print()
            
            if os.path.exists('obj_I_tb') and os.path.exists('masterflat_I_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_I_tb')
                iraf.ccdproc.setParam('output','@obj_I_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_I_tb.fits')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_I_tb is flat corrected and listed in obj_I_tbf")
                print("list obj_I_tb is flat corrected and listed in obj_I_tbf")
                print()
                
            if os.path.exists('obj_U_tb') and os.path.exists('masterflat_U_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_U_tb')
                iraf.ccdproc.setParam('output','@obj_U_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_U_tb.fits')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_U_tb is flat corrected and listed in obj_U_tbf")
                print("list obj_U_tb is flat corrected and listed in obj_U_tbf")
                print()    
                
            if os.path.exists('obj_ha_tb') and os.path.exists('masterflat_ha_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_ha_tb')
                iraf.ccdproc.setParam('output','@obj_ha_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_ha_tb.fits')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_ha_tb is flat corrected and listed in obj_ha_tbf")
                print("list obj_ha_tb is flat corrected and listed in obj_ha_tbf")
                print()
            
            if os.path.exists('obj_hb_tb') and os.path.exists('masterflat_hb_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_hb_tb')
                iraf.ccdproc.setParam('output','@obj_hb_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_hb_tb.fits')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_hb_tb is flat corrected and listed in obj_hb_tbf")
                print("list obj_hb_tb is flat corrected and listed in obj_hb_tbf")
                print()
                
            if os.path.exists('obj_O_tb') and os.path.exists('masterflat_O_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_O_tb')
                iraf.ccdproc.setParam('output','@obj_O_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_O_tb.fits')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_O_tb is flat corrected and listed in obj_O_tbf")
                print("list obj_O_tb is flat corrected and listed in obj_O_tbf")
                print()
                
            if os.path.exists('obj_6724_tb') and os.path.exists('masterflat_6724_tb.fits'):
                iraf.ccdproc.setParam('images','@obj_6724_tb')
                iraf.ccdproc.setParam('output','@obj_6724_tbf')
                iraf.ccdproc.setParam('trim','no')
                iraf.ccdproc.setParam('zerocor','no')
                iraf.ccdproc.setParam('flatcor','yes')
                iraf.ccdproc.setParam('zero','')
                iraf.ccdproc.setParam('flat','masterflat_6724_tb.fits')
                #iraf.ccdproc.eParam()
                iraf.ccdproc()
                logger.debug("list obj_6724_tb is flat corrected and listed in obj_6724_tbf")
                print("list obj_6724_tb is flat corrected and listed in obj_6724_tbf")
                print()
                
                
            self.update_progress(6, total_tasks)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        print()
        logger.debug("End of Pre-processing")
        print("End of Pre-processing")

        # Update progress to full when all tasks are completed successfully
        self.update_progress(total_tasks, total_tasks)

    def update_progress(self, completed_tasks, total_tasks):
        progress_percentage = (completed_tasks / total_tasks) * 100
        self.progress_bar["value"] = progress_percentage
        self.percentage_label.config(text=f"{progress_percentage:.1f}%")
        self.root.update_idletasks()

    def handle_error(self, error):
        messagebox.showerror("Error", f"An error occurred: {str(error)}")
        self.progress_bar["value"] = 0


   
    
 
     
    
"""Start of the Photometry"""



class PhotometricReductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JCBT PIPELINE")
        
        # Changes
        font_small = ('clean', 10, 'bold')
        font_med = ('clean', 12, 'bold')
        font_large = ('clean', 14, 'bold')
        self.root.configure(bg="black")
        #self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.resizable(True,True)

        #Input file
        self.input_label = tk.Label(root, text="INPUT FILE:", font=font_med, bg="black", fg="white")
        self.input_entry = tk.Entry(root, width=25, font=font_small, bg="black", fg="white")
        self.input_button = tk.Button(root, text="BROWSE", font=font_med, relief=tk.RAISED, command=self.select_input_file, bg="black", fg="lime", activebackground="green", activeforeground="white")

        self.run_button = tk.Button(root, text="RUN PHOTOMETRY", font=font_large, relief=tk.RAISED, command=self.perform_photometry, bg="red",fg="white", activebackground="green", activeforeground="white")

        #Output folder
        self.output_label = tk.Label(root, text="OUTPUT FOLDER:", font=font_med, bg="black", fg="white")
        self.output_entry = tk.Entry(root, width=25, font=font_small, bg="black", fg="white")
        self.output_button = tk.Button(root, text="BROWSE", font=font_med, relief=tk.RAISED, command=self.phot_output_folder, bg="black", fg="lime", activebackground="green", activeforeground="white")

        # Create a progress bar
        self.style = ttk.Style()
        self.style.configure("Custom.Horizontal.TProgressbar", troughcolor="black", background="green")
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress_bar.grid(row=8, columnspan=3, padx=10, pady=10)

        # Create a label for the percentage indicator
        self.percentage_label = tk.Label(root, text="", font=font_small, bg="black", fg="lime")
        self.percentage_label.grid(row=8, columnspan=3)


        # Set up layout using grid
        self.input_label.grid(row=5, column=0, padx=10, pady=10)
        self.input_entry.grid(row=5, column=1, padx=10, pady=10)
        self.input_button.grid(row=5, column=2, padx=10, pady=10)
      

        self.output_label.grid(row=6, column=0, padx=10, pady=10)
        self.output_entry.grid(row=6, column=1, padx=10, pady=10)
        self.output_button.grid(row=6, column=2, padx=10, pady=10) 
        
        self.run_button.grid(row=7, columnspan=3, padx=10, pady=10) 
        
        # Create a "Show Map" button for preprocessing
        self.show_map_button = tk.Button(root, text="SHOW MAP", font=font_med, command=self.show_map, bg="black", fg="lime", activebackground="green", activeforeground="white")
        self.show_map_button.grid(row=9, columnspan=3, padx=10, pady=10)
 
        # Configure column and row weights for resizing
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(20):
            self.root.grid_rowconfigure(i, weight=1)        

        # Add a horizontal line after the preprocessing section
        ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=10, columnspan=3, sticky="ew", padx=10, pady=10)

        self.phot_output_dir = ""

        # Initialize logger
        self.logger = logging.getLogger("PhotometricReductionApp")
        self.logger.setLevel(logging.DEBUG)


    def select_input_file(self):
        input_file = filedialog.askopenfilename(filetypes=[("TBF Files", "*_tbf.fits"), ("TB Files", "*_tb.fits")])
        if input_file:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_file)

    def phot_output_folder(self):
        self.phot_output_dir = filedialog.askdirectory()
        if self.phot_output_dir:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, self.phot_output_dir)

    def perform_photometry(self):
        input_file = self.input_entry.get()

        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return

        try:
            
            import os
            import fnmatch
            import numpy as np
            from astropy.io import fits
            from pyraf import iraf
            from photutils.detection import IRAFStarFinder
            import glob
            import logging
            import pandas as pd
            import re
            import matplotlib.pyplot as plt
            from photutils import background
            from photutils.background import MedianBackground
            from astropy.stats import sigma_clipped_stats
            
            #directory = "./"
            # Change to required working directory
            print("Current working directory: {0}".format(os.getcwd()))
            os.chdir(self.phot_output_dir)
            print("Changed to this directory: {0}".format(os.getcwd()))
            print()
            
            files = os.listdir()
            logging.basicConfig(level=logging.DEBUG,
                                filename="task_logs.log",
                                format='%(asctime)s | %(levelname)s | %(message)s',
                                filemode='w')

            # Creating an object
            logger = logging.getLogger('task_logger')

            # Create a file handler and set its level to DEBUG
            file_handler = logging.FileHandler('task_logs.log')
            file_handler.setLevel(logging.DEBUG)

            # Create a formatter and add it to the file handler
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            file_handler.setFormatter(formatter)

            # Add the file handler to the logger
            logger.addHandler(file_handler)
            
            self.logger.info('Started to process selected fits file')
            total_tasks = 5  # The total number of tasks in your script

            for file in sorted(os.listdir(self.phot_output_dir)):
                if (os.path.exists("median_fwhm")):
                    os.remove("median_fwhm")

            # Open the selected FITS file
            hdul = fits.open(input_file)
            image = hdul[0].data

            # Check image dimensions and reshape if necessary    
            if len(image.shape) > 2:
                image = np.mean(image, axis=0)

            # Perform source extraction using IRAFStarFinder    
            fwhm = 10
            threshold = np.median(image.flatten())
            star = IRAFStarFinder(threshold, fwhm, sigma_radius=1.5, minsep_fwhm=2.5, sharplo=0.2, sharphi=1.0, roundlo=-1.0, roundhi=1.0, sky=None, exclude_border=True, brightest=None, peakmax=None, xycoords=None)
            sources = star.find_stars(image)

            # Calculate median FWHM        
            median_fwhm = np.median(sources['fwhm'])
            output_file = open('median_fwhm', 'a+')
            output_file.write(f"Median FWHM in {input_file}: {median_fwhm}\n")
            output_file.close()
            hdul.close()
            logger.debug("median FWHM calculated from the selected fits file")
            print()            
            hdul.close()
            
            #Calculate Sigma above background
            mean, median, std = sigma_clipped_stats(image, sigma=3.0)
            #print(std)
            
            
            """ Task 2 - Setting Parameter files """


            # Packages required
            iraf.digiphot(_doprint=0)
            iraf.daophot(_doprint=0)

            # Set data parameter file
            iraf.datapars.setParam('scale','1.0')
            #iraf.datapars.setParam('fwhmpsf','fwhm')
            iraf.datapars.fwhmpsf = median_fwhm
            #iraf.datapars.setParam('sigma','10')
            iraf.datapars.sigma = std
            iraf.datapars.setParam('datamin','INDEF')
            iraf.datapars.setParam('datamax','INDEF')
            iraf.datapars.setParam('ccdread','RDNOISE')
            iraf.datapars.setParam('gain','GAIN')
            iraf.datapars.setParam('readnoise','4.2')
            iraf.datapars.setParam('epadu','0.75')
            iraf.datapars.setParam('exposure','EXPTIME')
            iraf.datapars.setParam('airmass','AIRMASS')
            iraf.datapars.setParam('filter','FILTER')
            iraf.datapars.setParam('obstime','UT')
            #iraf.datapars.eParam()
            #iraf.datapars()


            # Setting the find parameter file
            iraf.findpars.setParam('threshold','4')
            #iraf.findpars.eParam()
            #iraf.findpars()

            # Setting the center parameter file
            #iraf.centerpars.setParam('cbox','5')
            iraf.centerpars.cbox = 2*median_fwhm
            iraf.centerpars.setParam('cthreshold','5')
            #iraf.centerpars.eParam()
            #iraf.centerpars()

            #Setting the daophot parameter file
            iraf.daopars.setParam('function','auto')
            iraf.daopars.setParam('varorder','-1')
            #iraf.daopars.setParam('psfrad','3*fwhm')
            iraf.daopars.psfrad = 4*median_fwhm+1
            #iraf.daopars.setParam('fitrad','3')
            iraf.daopars.fitrad = median_fwhm
            iraf.daopars.setParam('recenter','Yes')
            iraf.daopars.setParam('fitsky','No')
            iraf.daopars.setParam('groupsky','Yes')
            #iraf.daopars.setParam('sannulus','35.0')
            iraf.daopars.sannulus = 5*median_fwhm
            #iraf.daopars.setParam('wsannulus','20.0')
            iraf.daopars.wsannulus = 3*median_fwhm
            iraf.daopars.setParam('maxiter','50')
            iraf.daopars.setParam('maxgroup','60')
            #iraf.daopars.eParam()
            #iraf.daopars()

            # Setting the fitsky parameter file
            iraf.fitskypars.setParam('salgorithm','mode')
            #iraf.fitskypars.setParam('annulus','35.0')
            iraf.fitskypars.annulus = 5*median_fwhm
            #iraf.fitskypars.setParam('dannulus','20.0')
            iraf.fitskypars.dannulus = 3*median_fwhm
            iraf.fitskypars.setParam('smaxiter','10')
            #iraf.fitskypars.eParam()
            #iraf.fitskypars()

            # Setting the photometric parameter file
            #iraf.photpars.setParam('apertures','5:30:5')
            iraf.photpars.apertures = 4*median_fwhm
            iraf.photpars.setParam('zmag','25')
            #iraf.photpars.eParam()
            #iraf.photpars()
            
            print("Parameters are found")
            print()



            """ Task 3 - Running Daofind """


            # Set parameters for daofind task to detect sources and estimate is position
            try:
                #logger.info("Started Daofind task")
                #iraf.daofind.setParam('image','')
                iraf.daofind.image = input_file
                iraf.daofind.setParam('output','default')
                iraf.daofind.setParam('interactive','No')
                iraf.daofind.setParam('cache','No')
                iraf.daofind.setParam('verify','No')
                iraf.daofind.setParam('update','Yes')
                iraf.daofind.setParam('verbose','No')
                #iraf.daofind.eParam()
                iraf.daofind()
                logger.debug("Sources detected using Daofind task")
                print("Sources detected using Daofind task")
                self.update_progress(1, total_tasks)
            except Exception as e:
                logger.error(f"Error executing trimming task: {str(e)}")
            print()
            print()



            """ Task 4 - Running Phot """


            # Set parameters for phot task to estimate instrumental magnitude of detected sources
            try:
                logger.info("Started Phot task")
                iraf.phot.image = input_file
                iraf.phot.setParam('coords', 'default')
                iraf.phot.setParam('output', 'default')
                iraf.phot.setParam('interactive', 'No')
                iraf.phot.setParam('radplots', 'No')
                iraf.phot.setParam('cache','No')
                iraf.phot.setParam('verify','No')
                iraf.phot.setParam('update','Yes')
                iraf.phot.setParam('verbose','No')
                #iraf.phot.eParam()
                iraf.phot()
                logger.debug("Estimated the instrumental magnitudes using Phot task")
                print("Estimated the instrumental magnitudes using Phot task")
                self.update_progress(2, total_tasks)
            except Exception as e:
                logger.error(f"Error executing trimming task: {str(e)}")
            print()
            print()



            """ Task 5 - Running Pstselect """


            # Set parameters for pstselect task to select suitable sources for PSF model
            try:
                logger.info("Started pstselect task")
                iraf.pstselect.image = input_file
                iraf.pstselect.setParam('photfile', 'default')
                iraf.pstselect.setParam('pstfile', 'default')
                iraf.pstselect.setParam('maxnpsf', '25')
                iraf.pstselect.setParam('mkstars', 'No')
                iraf.pstselect.setParam('interactive', 'No')
                iraf.pstselect.setParam('cache','No')
                iraf.pstselect.setParam('verify','No')
                iraf.pstselect.setParam('update','Yes')
                iraf.pstselect.setParam('verbose','No')
                #iraf.pstselect.eParam()
                iraf.pstselect()
                logger.debug("Sources selected for PSF modeling using Pstselect task")
                print("Sources selected for PSF modeling using Pstselect task")
                self.update_progress(3, total_tasks)
            except Exception as e:
                logger.error(f"Error executing trimming task: {str(e)}")
            print()
            print()




            """ Task 6 - Running Psf """


            # Set parameters for psf task to model PSF for selected sources
            try:
                logger.info("Started Psf task")
                iraf.psf.image = input_file
                iraf.psf.setParam('photfile', 'default')
                iraf.psf.setParam('pstfile', 'default')
                iraf.psf.setParam('psfimage', 'default')
                iraf.psf.setParam('opstfile', 'default')
                iraf.psf.setParam('groupfile', 'default')
                iraf.psf.setParam('matchbyid', 'Yes')
                iraf.psf.setParam('interactive', 'No')
                iraf.psf.setParam('mkstars', 'No')
                iraf.psf.setParam('cache','No')
                iraf.psf.setParam('verify','No')
                iraf.psf.setParam('update','Yes')
                iraf.psf.setParam('verbose','No')
                #iraf.psf.eParam()
                iraf.psf()
                logger.debug("PSF model generated using Psf task")
                print("PSF model generated using Psf task")
                self.update_progress(4, total_tasks)
            except Exception as e:
                logger.error(f"Error: {str(e)}")
            print()
            print()




            """ Task 7 - Running Allstar """


            # Set parameters for allstar task to estimate the final magnitudes of sources
            try:
                logger.info("Started Allstar task")
                iraf.allstar.image = input_file
                iraf.allstar.setParam('photfile', 'default')
                iraf.allstar.setParam('psfimage', 'default')
                iraf.allstar.setParam('allstarfile', 'default')
                iraf.allstar.setParam('rejfile', 'default')
                iraf.allstar.setParam('subimage', 'default')
                iraf.allstar.setParam('cache','No')
                iraf.allstar.setParam('verify','No')
                iraf.allstar.setParam('update','Yes')
                iraf.allstar.setParam('verbose','No')
                #iraf.allstar.eParam()
                iraf.allstar()
                logger.debug("Final magnitudes estimated using Allstar task")
                print("Final magnitudes estimated using Allstar task")
                print()
                logger.info("End of the pipeline")
                print()
                print()
                print("End of the pipeline")
                self.update_progress(5, total_tasks)
            except Exception as e:
                logger.error(f"Error: {str(e)}")

            """ End of the pipeline """
            
            messagebox.showinfo("Success", "Photometric reduction completed.")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


            self.update_progress(total_tasks, total_tasks)


    def update_progress(self, completed_tasks, total_tasks):
        progress_percentage = (completed_tasks / total_tasks) * 100
        self.progress_bar["value"] = progress_percentage
        self.percentage_label.config(text=f"{progress_percentage:.1f}%")
        self.root.update_idletasks()

    def handle_error(self, error):
        messagebox.showerror("Error", f"An error occurred: {str(error)}")
        self.progress_bar["value"] = 0

    def show_map(self):
        import re
        import pandas as pd
        input_file = self.input_entry.get()
        if input_file:
            input_text_file = input_file.replace('.fits', '.fits.als.1')

            def skip_lines(file, n):
                for _ in range(n):
                    next(file)
            with open(input_text_file) as file:
                skip_lines(file, 44)
                data_lines = file.readlines()

            data = []
            for line in data_lines:
                match = re.match(r'\s*(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*', line)
                if match:
                    id, xcenter, ycenter, magnitude = match.groups()
                    data.append([int(id), float(xcenter), float(ycenter), float(magnitude)])

            data = pd.DataFrame(data, columns=['ID', 'XCENTER', 'YCENTER', 'Magnitude'])


            fits_image_data = fits.open(input_file)[0].data[0]  # Extract 2D data
            fig, ax = plt.subplots(constrained_layout=True, figsize=(8,6))
            im = ax.imshow(fits_image_data, cmap='gray', origin='lower', vmin=150, vmax=250)
            scatter = ax.scatter(data['XCENTER'], data['YCENTER'], marker='x', c='red', s=5, picker=True)
            ax.set_xlabel('XCENTER')
            ax.set_ylabel('YCENTER')
            ax.set_title('Interactive Plot of Sources in FITS Image')

            annotations = []
            def onpick(event):
                ind = event.ind[0]
                x = data['XCENTER'][ind]
                y = data['YCENTER'][ind]
                id = data['ID'][ind]
                mag = data['Magnitude'][ind]
                text = f"ID: {id}\nXCENTER: {x:.2f}\nYCENTER: {y:.2f}\nMagnitude: {mag:.2f}"
                
                for ann in annotations:
                    ann.remove()
                annotations.clear()

                annotation = ax.annotate(text, (x, y), xytext=(-50, 10), textcoords='offset points', fontsize=10,
                            bbox=dict(boxstyle='round,pad=0.3', edgecolor='red', facecolor='white'))
                annotations.append(annotation)
                fig.canvas.draw()

            fig.canvas.mpl_connect('pick_event', onpick)
            plt.show()





"""Start of the Run Photometry for all"""



class AllPhotometricReductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JCBT PIPELINE")
        
        # Changes
        font_small = ('clean', 10, 'bold')
        font_med = ('clean', 12, 'bold')
        font_large = ('clean', 14, 'bold')
        self.root.configure(bg="black")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.resizable(True,True)

        #Input folder
        self.input_label = tk.Label(root, text="INPUT FOLDER:", font=font_med, bg="black", fg="white")
        self.input_entry = tk.Entry(root, width=25, font=font_small, bg="black", fg="white")
        self.input_button = tk.Button(root, text="BROWSE", font=font_med, relief=tk.RAISED, command=self.allphot_input_folder, bg="black", fg="lime", activebackground="green", activeforeground="white")

        self.run_button = tk.Button(root, text="RUN PHOTOMETRY FOR ALL", font=font_large, relief=tk.RAISED, command=self.perform_all_photometry, bg="red",fg="white", activebackground="green", activeforeground="white")

        #Output folder
        self.output_label = tk.Label(root, text="OUTPUT FOLDER:", font=font_med, bg="black", fg="white")
        self.output_entry = tk.Entry(root, width=25, font=font_small, bg="black", fg="white")
        self.output_button = tk.Button(root, text="BROWSE", font=font_med, relief=tk.RAISED, command=self.allphot_output_folder, bg="black", fg="lime", activebackground="green", activeforeground="white")

        # Create a progress bar
        self.style = ttk.Style()
        self.style.configure("Custom.Horizontal.TProgressbar", troughcolor="black", background="green")
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress_bar.grid(row=14, columnspan=3, padx=10, pady=10)

        # Create a label for the percentage indicator
        self.percentage_label = tk.Label(root, text="", font=font_small, bg="black", fg="lime")
        self.percentage_label.grid(row=14, columnspan=3)


        # Set up layout using grid
        self.input_label.grid(row=11, column=0, padx=10, pady=10)
        self.input_entry.grid(row=11, column=1, padx=10, pady=10)
        self.input_button.grid(row=11, column=2, padx=10, pady=10)
      

        self.output_label.grid(row=12, column=0, padx=10, pady=10)
        self.output_entry.grid(row=12, column=1, padx=10, pady=10)
        self.output_button.grid(row=12, column=2, padx=10, pady=10) 
        
        self.run_button.grid(row=13, columnspan=3, padx=10, pady=10) 
 
        # Configure column and row weights for resizing
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(20):
            self.root.grid_rowconfigure(i, weight=1)        

        # Create the 'Show files' button
        self.show_files_button = tk.Button(root, text="SHOW FILES", font=font_med, relief=tk.RAISED, command=self.show_files, bg="black", fg="lime", activebackground="green", activeforeground="white")
        self.show_files_button.grid(row=15, column=0, padx=10, pady=10)

        # Create a "Help" button
        self.help_button = tk.Button(root, text="HELP MENU", font=font_med, command=self.show_help, bg="black", fg="lime", activebackground="green", activeforeground="white")
        self.help_button.grid(row=15, column=1, padx=10, pady=10)

        # Create a "Show Plots" button for preprocessing
        self.show_plots_button = tk.Button(root, text="SHOW PLOT", font=font_med, command=self.show_plots, bg="black", fg="lime", activebackground="green", activeforeground="white")
        self.show_plots_button.grid(row=15, column=2, padx=10, pady=10)


        self.allphot_input_dir = ""
        self.allphot_output_dir = ""

        self.help_window = None

        # Initialize logger
        self.logger = logging.getLogger("AllPhotometricReductionApp")
        self.logger.setLevel(logging.DEBUG)


    def allphot_input_folder(self):
        self.allphot_input_dir = filedialog.askdirectory()
        if self.allphot_input_dir:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.allphot_input_dir)

    def allphot_output_folder(self):
        self.allphot_output_dir = filedialog.askdirectory()
        if self.allphot_output_dir:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, self.allphot_output_dir)

    def perform_all_photometry(self):
        try:
            import os
            import fnmatch
            import numpy as np
            from astropy.io import fits
            from pyraf import iraf
            from photutils.detection import IRAFStarFinder
            import glob
            import logging
            from photutils import background
            from photutils.background import MedianBackground
            from astropy.stats import sigma_clipped_stats
            
            #directory = "./"
            print("Current working directory: {0}".format(os.getcwd()))
            os.chdir(self.allphot_input_dir)
            print("Changed to this directory: {0}".format(os.getcwd()))
            print()
            logging.basicConfig(level=logging.DEBUG,
                                filename="task_logs.log",
                                format='%(asctime)s | %(levelname)s | %(message)s',
                                filemode='w')

            # Creating an object
            logger = logging.getLogger('task_logger')

            # Create a file handler and set its level to DEBUG
            file_handler = logging.FileHandler('task_logs.log')
            file_handler.setLevel(logging.DEBUG)

            # Create a formatter and add it to the file handler
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            file_handler.setFormatter(formatter)

            # Add the file handler to the logger
            logger.addHandler(file_handler)
            
            self.logger.info('Started to process selected fits file')
            total_tasks = 5  # The total number of tasks in your script

            for file in sorted(os.listdir(self.allphot_input_dir)):
                if (os.path.exists("median_fwhm")):
                    os.remove("median_fwhm")

            # Get a list of all files in the directory with the "_tbf.fits" extension
            fits_files = [f for f in sorted(os.listdir(self.allphot_input_dir)) if f.endswith("_tbf.fits")]
            
            # Iterate through each FITS file
            for input_file in fits_files:
                # Open the FITS file
                hdul = fits.open(os.path.join(input_file))
                image = hdul[0].data

                # Check image dimensions and reshape if necessary    
                if len(image.shape) > 2:
                    image = np.mean(image, axis=0)

                # Perform source extraction using IRAFStarFinder    
                fwhm = 10
                threshold = np.median(image.flatten())
                star = IRAFStarFinder(threshold, fwhm, sigma_radius=1.5, minsep_fwhm=2.5, sharplo=0.2, sharphi=1.0, roundlo=-1.0, roundhi=1, sky=None, exclude_border=True, brightest=None, peakmax=None, xycoords=None)
                sources = star.find_stars(image)
        
                # Calculate median FWHM        
                median_fwhm = np.median(sources['fwhm'])
                output_file = open('median_fwhm', 'a+')
                output_file.write(f"Median FWHM in {input_file}: {median_fwhm}\n")
                output_file.close()
                hdul.close()
                logger.debug("median FWHM calculated from the selected fits file")

                #Calculate Sigma above background
                mean, median, std = sigma_clipped_stats(image, sigma=3.0)
                #print(std)
            
            
                """ Task 2 - Setting Parameter files """
    
    
                # Packages required
                iraf.digiphot(_doprint=0)
                iraf.daophot(_doprint=0)
    
                # Set data parameter file
                iraf.datapars.setParam('scale','1.0')
                #iraf.datapars.setParam('fwhmpsf','fwhm')
                iraf.datapars.fwhmpsf = median_fwhm
                #iraf.datapars.setParam('sigma','30')
                iraf.datapars.sigma = std
                iraf.datapars.setParam('datamin','INDEF')
                iraf.datapars.setParam('datamax','INDEF')
                iraf.datapars.setParam('ccdread','RDNOISE')
                iraf.datapars.setParam('gain','GAIN')
                iraf.datapars.setParam('readnoise','4.2')
                iraf.datapars.setParam('epadu','0.75')
                iraf.datapars.setParam('exposure','EXPTIME')
                iraf.datapars.setParam('airmass','AIRMASS')
                iraf.datapars.setParam('filter','FILTER')
                iraf.datapars.setParam('obstime','UT')
                #iraf.datapars.eParam()
                #iraf.datapars()
    
    
                # Setting the find parameter file
                iraf.findpars.setParam('threshold','5')
                #iraf.findpars.eParam()
                #iraf.findpars()
    
                # Setting the center parameter file
                #iraf.centerpars.setParam('cbox','5')
                iraf.centerpars.cbox = 2*median_fwhm
                iraf.centerpars.setParam('cthreshold','5')
                #iraf.centerpars.eParam()
                #iraf.centerpars()
    
                #Setting the daophot parameter file
                iraf.daopars.setParam('function','auto')
                iraf.daopars.setParam('varorder','-1')
                #iraf.daopars.setParam('psfrad','3*fwhm')
                iraf.daopars.psfrad = 4*median_fwhm+1
                #iraf.daopars.setParam('fitrad','3')
                iraf.daopars.fitrad = median_fwhm
                iraf.daopars.setParam('recenter','Yes')
                iraf.daopars.setParam('fitsky','No')
                iraf.daopars.setParam('groupsky','Yes')
                #iraf.daopars.setParam('sannulus','35.0')
                iraf.daopars.sannulus = 5*median_fwhm
                #iraf.daopars.setParam('wsannulus','20.0')
                iraf.daopars.wsannulus = 3*median_fwhm
                iraf.daopars.setParam('maxiter','50')
                iraf.daopars.setParam('maxgroup','60')
                #iraf.daopars.eParam()
                #iraf.daopars()
    
                # Setting the fitsky parameter file
                iraf.fitskypars.setParam('salgorithm','mode')
                #iraf.fitskypars.setParam('annulus','35.0')
                iraf.fitskypars.annulus = 5*median_fwhm
                #iraf.fitskypars.setParam('dannulus','20.0')
                iraf.fitskypars.dannulus = 3*median_fwhm
                iraf.fitskypars.setParam('smaxiter','10')
                #iraf.fitskypars.eParam()
                #iraf.fitskypars()
    
                # Setting the photometric parameter file
                #iraf.photpars.setParam('apertures','5:30:5')
                iraf.photpars.apertures = 4*median_fwhm
                iraf.photpars.setParam('zmag','25.0')
                #iraf.photpars.eParam()
                #iraf.photpars()
                
                print()
                print("Parameters are found")
                print()
    
    
    
                """ Task 3 - Running Daofind """
    
    
                # Set parameters for daofind task to detect sources and estimate is position
                try:
                    #logger.info("Started Daofind task")
                    #iraf.daofind.setParam('image','')
                    iraf.daofind.setParam('image', os.path.join(input_file))
                    iraf.daofind.setParam('output','default')
                    iraf.daofind.setParam('interactive','No')
                    iraf.daofind.setParam('cache','No')
                    iraf.daofind.setParam('verify','No')
                    iraf.daofind.setParam('update','Yes')
                    iraf.daofind.setParam('verbose','No')
                    #iraf.daofind.eParam()
                    iraf.daofind()
                    logger.debug("Sources detected using Daofind task")
                    print("Sources detected using Daofind task")
                    self.update_progress(1, total_tasks)
                except Exception as e:
                    logger.error(f"Error executing trimming task: {str(e)}")
                print()
                print()
    
    
    
                """ Task 4 - Running Phot """
    
    
                # Set parameters for phot task to estimate instrumental magnitude of detected sources
                try:
                    logger.info("Started Phot task")
                    iraf.phot.setParam('image', os.path.join(input_file))
                    iraf.phot.setParam('coords', 'default')
                    iraf.phot.setParam('output', 'default')
                    iraf.phot.setParam('interactive', 'No')
                    iraf.phot.setParam('radplots', 'No')
                    iraf.phot.setParam('cache','No')
                    iraf.phot.setParam('verify','No')
                    iraf.phot.setParam('update','Yes')
                    iraf.phot.setParam('verbose','No')
                    #iraf.phot.eParam()
                    iraf.phot()
                    logger.debug("Estimated the instrumental magnitudes using Phot task")
                    print("Estimated the instrumental magnitudes using Phot task")
                    self.update_progress(2, total_tasks)
                except Exception as e:
                    logger.error(f"Error executing trimming task: {str(e)}")
                print()
                print()
    
    
    
                """ Task 5 - Running Pstselect """
    
    
                # Set parameters for pstselect task to select suitable sources for PSF model
                try:
                    logger.info("Started pstselect task")
                    iraf.pstselect.setParam('image', os.path.join(input_file))
                    iraf.pstselect.setParam('photfile', 'default')
                    iraf.pstselect.setParam('pstfile', 'default')
                    iraf.pstselect.setParam('maxnpsf', '25')
                    iraf.pstselect.setParam('mkstars', 'No')
                    iraf.pstselect.setParam('interactive', 'No')
                    iraf.pstselect.setParam('cache','No')
                    iraf.pstselect.setParam('verify','No')
                    iraf.pstselect.setParam('update','Yes')
                    iraf.pstselect.setParam('verbose','No')
                    #iraf.pstselect.eParam()
                    iraf.pstselect()
                    logger.debug("Sources selected for PSF modeling using Pstselect task")
                    print("Sources selected for PSF modeling using Pstselect task")
                    self.update_progress(3, total_tasks)
                except Exception as e:
                    logger.error(f"Error executing trimming task: {str(e)}")
                print()
                print()
    
    
    
    
                """ Task 6 - Running Psf """
    
    
                # Set parameters for psf task to model PSF for selected sources
                try:
                    logger.info("Started Psf task")
                    iraf.psf.setParam('image', os.path.join(input_file))
                    iraf.psf.setParam('photfile', 'default')
                    iraf.psf.setParam('pstfile', 'default')
                    iraf.psf.setParam('psfimage', 'default')
                    iraf.psf.setParam('opstfile', 'default')
                    iraf.psf.setParam('groupfile', 'default')
                    iraf.psf.setParam('matchbyid', 'Yes')
                    iraf.psf.setParam('interactive', 'No')
                    iraf.psf.setParam('mkstars', 'No')
                    iraf.psf.setParam('cache','No')
                    iraf.psf.setParam('verify','No')
                    iraf.psf.setParam('update','Yes')
                    iraf.psf.setParam('verbose','No')
                    #iraf.psf.eParam()
                    iraf.psf()
                    logger.debug("PSF model generated using Psf task")
                    print("PSF model generated using Psf task")
                    self.update_progress(4, total_tasks)
                except Exception as e:
                    logger.error(f"Error: {str(e)}")
                print()
                print()
    
    
    
    
                """ Task 7 - Running Allstar """
    
    
                # Set parameters for allstar task to estimate the final magnitudes of sources
                try:
                    logger.info("Started Allstar task")
                    iraf.allstar.setParam('image', os.path.join(input_file))
                    iraf.allstar.setParam('photfile', 'default')
                    iraf.allstar.setParam('psfimage', 'default')
                    iraf.allstar.setParam('allstarfile', 'default')
                    iraf.allstar.setParam('rejfile', 'default')
                    iraf.allstar.setParam('subimage', 'default')
                    iraf.allstar.setParam('cache','No')
                    iraf.allstar.setParam('verify','No')
                    iraf.allstar.setParam('update','Yes')
                    iraf.allstar.setParam('verbose','No')
                    #iraf.allstar.eParam()
                    iraf.allstar()
                    logger.debug("Final magnitudes estimated using Allstar task")
                    print("Final magnitudes estimated using Allstar task")
                    print()
                    logger.info("End of the pipeline")
                    # Close the FITS file
                    hdul.close()
                    print()
                    print()
                    #print("End of the pipeline")
                    self.update_progress(5, total_tasks)
                except Exception as e:
                    logger.error(f"Error: {str(e)}")


            """ End of the pipeline """
            
            messagebox.showinfo("Success", "Photometric reduction completed.")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


            self.update_progress(total_tasks, total_tasks)


    def update_progress(self, completed_tasks, total_tasks):
        progress_percentage = (completed_tasks / total_tasks) * 100
        self.progress_bar["value"] = progress_percentage
        self.percentage_label.config(text=f"{progress_percentage:.1f}%")
        self.root.update_idletasks()

    def handle_error(self, error):
        messagebox.showerror("Error", f"An error occurred: {str(error)}")
        self.progress_bar["value"] = 0


    def show_files(self):
        # Check if the output directory has been selected
        if not self.allphot_output_dir:
            messagebox.showerror("Error", "Select Output folder")
            return

        # Determine the appropriate file explorer based on the user's OS
        system = platform.system()
        if system == "Windows":
            os.startfile(self.allphot_output_dir)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", self.allphot_output_dir])
        elif system == "Linux":
            subprocess.Popen(["xdg-open", self.allphot_output_dir])
        else:
            messagebox.showerror("Error", "Unsupported operating system.")

    def show_help(self):
        if self.help_window is not None and self.help_window.winfo_exists():
            self.help_window.lift()
        else:
            self.help_window = tk.Toplevel(self.root)
            self.help_window.title("Help")

            # Add a scrollbar for the help text
            scrollbar = tk.Scrollbar(self.help_window)
            scrollbar.pack(side="right", fill="y")
      	
            help_text = """
Photometric reduction UI:
          
The code aims to perform the photometric data reduction process for the data obtained from the 1.3 meter JCBT telescope at VBO, kavalur. The code automatically performs all the steps involved in photometric reduction of the calibrated data including the Aperture and PSF photometry. The text file task_logs.log contains the logger information for debugging.
          
Usage: pipeline
          
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
Email  : adiphysik@gmail.com
Date   : 14/03/2024
version: 2.0
"""
            
            # Create a text widget for the help text
            text_widget = tk.Text(self.help_window, wrap="word", yscrollcommand=scrollbar.set, font=('Helvetica', 12))
            text_widget.insert("1.0", help_text)
            text_widget.pack(expand=True, fill="both")

            # Configure the scrollbar
            scrollbar.config(command=text_widget.yview)


    def show_plots(self):
        # Initialize empty lists to store UT and FWHM values
        # Initialize empty lists to store UT and FWHM values
        ut_values = []
        fwhm_values_pixels = []
        fwhm_values_arcseconds = []
        pixel_scale = 0.5

        # Step 1: Read the text file and extract FWHM values and filenames
        with open('median_fwhm', 'r') as file:
            for line in file:
                if line.startswith("Median FWHM"):
                    parts = line.split(': ')
                    filename = parts[0].split(' in ')[1].strip()
                    fwhm_pixels = float(parts[1])
                    
                    # Step 2: Open the FITS file and extract the UT from the header
                    try:
                        with fits.open(filename) as hdul:
                            ut = hdul[0].header['UT']
                        
                        # Append UT and FWHM to the respective lists
                        ut_values.append(ut)
                        fwhm_values_pixels.append(fwhm_pixels)
                        fwhm_arcseconds = fwhm_pixels * pixel_scale
                        fwhm_values_arcseconds.append(fwhm_arcseconds)                
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")

        # Step 3: Sort the UT and FWHM values based on UT
        sorted_indices = sorted(range(len(ut_values)), key=lambda i: ut_values[i])
        ut_values = [ut_values[i] for i in sorted_indices]
        fwhm_values_pixels = [fwhm_values_pixels[i] for i in sorted_indices]
        fwhm_values_arcseconds = [fwhm_values_arcseconds[i] for i in sorted_indices]


        # Step 4: Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(ut_values, fwhm_values_arcseconds, marker='o', linestyle='-', color='b', label='FWHM vs UT')
        plt.xlabel('UT')
        plt.ylabel('FWHM (arcs)')
        plt.title('FWHM vs UT')
        plt.legend()
        plt.grid(True)

        # Step 4: Show the plot or save it to a file
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
	


        
    def on_closing(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    preprocessing_app = PreprocessingApp(root)
    photometry_app = PhotometricReductionApp(root)
    allphotometry_app = AllPhotometricReductionApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()

