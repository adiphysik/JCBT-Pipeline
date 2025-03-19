"""
main.py

This script serves as the entry point for the photometric data reduction pipeline.
It integrates different modules for calibration, photometry, and batch processing.
"""

# Importing necessary modules from the pipeline
import pipeline

def main():
    """Main function to execute the photometry pipeline."""
    
    print("Starting the photometry pipeline...")

    # Step 1: Perform Calibration
    print("Performing image calibration...")
    pipeline()

    print("Pipeline execution complete!")

if __name__ == "__main__":
    main()
