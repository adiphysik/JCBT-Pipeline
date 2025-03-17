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

