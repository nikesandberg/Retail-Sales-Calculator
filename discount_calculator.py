import pandas as pd
import logging
import sqlite3

logging.basicConfig(
    filename='pipeline_log.txt', 
    format='[%(asctime)s][%(levelname)s] %(message)s', 
    level=logging.DEBUG
)


class DiscountCalculator:
    """A class to calculate the original price, discount and ROI from sales data."""
    
    def __init__(self, data_file):
        self.data_file = data_file
        self.logger = logging.getLogger(__name__)
        
        try:
            self.df = pd.read_csv(data_file)
        except Exception as e:
            logging.error(f'Could not read the CSV file: {e}')
            raise e
    
    def calculate_discount(self):
        
        # Calculate the original price in USD before the discount
        try: 
            self.df['Original Price (USD)'] = self.df['Sales Revenue (USD)'] / (1 - self.df['Discount Percentage'] / 100)
        
        # Calculate the discount amount in USD
            self.df['Discount Amount (USD)'] = self.df['Original Price (USD)'] - self.df['Sales Revenue (USD)']
            self.logger.info('Discount calculator worked successfully')
        
        except Exception as e:
            self.logger.error(f'Error during discount calculation: {e}')
            raise e
        
        return self.df
    
    def return_on_investment(self):
        #Calculate the ROI in %
        roi_values = []
        for index, row in self.df.iterrows():
            try:
                if row['Marketing Spend (USD)'] == 0:
                # If Marketing Spend is 0, set ROI to 0
                    roi_values.append(0)
                else:
                    roi = ((row['Sales Revenue (USD)'] - row['Marketing Spend (USD)']) / row['Marketing Spend (USD)']) * 100
                    roi_values.append(roi)
          
            except Exception as e:
                self.logger.error(f'Error occured during ROI calcualtion: {e}')

        self.df['ROI (%)'] = roi_values

    
        return self.df
    
    def save_to_csv(self, output_file):
       
        try: 
            self.df.to_csv(output_file, index=False)
            self.logger.info(f'File saved successfully: {output_file}')
        except Exception as e: 
            self.logger.error(f'Error occured saving the CSV file: {e}')
            raise e
        
    def save_to_sql(self):
        try: 
            con = sqlite3.connect('retail_sales_db.db')
            self.df.to_sql('sales_data', con, if_exists='replace', index=False)
            self.logger.info('Data saved to SQL database successfully.')
        except Exception as e: 
            self.logger.error(f'Error saving to SQL: {e}')
            raise e