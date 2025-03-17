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

