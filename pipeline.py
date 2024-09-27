import pandas as pd
import pytest
import os
import sqlite3
import logging
from discount_calculator import DiscountCalculator

logging.basicConfig(
    filename='pipeline_log.txt', 
    level=logging.INFO, 
    format='[%(asctime)s][%(levelname)s] %(message)s'
    )

def pipeline():
    try:
        logging.info("Pipeline initiated. Loading CSV file")
        calculator = DiscountCalculator(r'C:\Users\nikes\Documents\Pythonht24\Retail_sales.csv')

        logging.info("Calculating discount and original price.")
        df_with_discount = calculator.calculate_discount()

        logging.info("Calculating ROI.")
        df_with_roi = calculator.return_on_investment()

        output_csv_file = 'db_w_discount_and_roi.csv'
        logging.info('Saving dataframe to csv-file')
        calculator.save_to_csv(output_csv_file)

        logging.info('Saving dataframe to SQLite database.')
        calculator.save_to_sql()

        logging.info("Pipeline completed successfully!")

    except Exception as e:
        logging.error(f"Error occurred during pipeline execution: {e}")
        raise
    
pipeline()