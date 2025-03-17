"""
main.py

This script serves as the entry point for the photometric data reduction pipeline.
It integrates different modules for calibration, photometry, and batch processing.
"""

# Importing necessary modules from the pipeline
from pipeline.calibration import calibrate_images
from pipeline.photometry import perform_photometry
from pipeline.photometry_for_all import batch_photometry

def main():
    """Main function to execute the photometry pipeline."""
    
    print("Starting the photometry pipeline...")

    # Step 1: Perform Calibration
    print("Performing image calibration...")
    calibrate_images()

    # Step 2: Perform Photometry on a single image
    print("Performing photometry on a single image...")
    perform_photometry()

    # Step 3: Perform batch photometry on multiple images
    print("Performing photometry on all images...")
    batch_photometry()

    print("Pipeline execution complete!")

if __name__ == "__main__":
    main()
