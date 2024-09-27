import pytest
import pandas as pd
import os
from discount_calculator import DiscountCalculator

@pytest.fixture
#Pytest fixture to create sample CSV-file to use in both tests
def sample_data_file():
    
    sample_data = {
        'Sales Revenue (USD)': [1000, 2200, 3000],
        'Discount Percentage': [0, 20, 30], 
        'Marketing Spend (USD)': [0, 200, 1500]
    }
    test_df = pd.DataFrame(sample_data)
    test_file = 'test_sales_data.csv'
    test_df.to_csv(test_file, index=False)
    yield test_file
    
     # Sample file deleted after test
    if os.path.exists(test_file):
        os.remove(test_file)

    
@pytest.fixture        
def output_file():
    
    test_output_file = 'test_output.csv'
    yield test_output_file
    
    #Output file deleted after test
    if os.path.exists(test_output_file):
        os.remove(test_output_file)
        
def test_calculate_discount(sample_data_file):
    
    calculator = DiscountCalculator(sample_data_file)
    df = calculator.calculate_discount()

    #Test if the correct columns were added successfully 
    assert 'Original Price (USD)' in df.columns
    assert 'Discount Amount (USD)' in df.columns
   

    # Test if the calculated original price is correct
    expected_original_prices = [1000.00, 2750.00, 4285.71]
    expected_discount_amounts = [0.00, 550.00, 1285.71]
    assert round(df['Original Price (USD)'][0], 2) == expected_original_prices[0]
    assert round(df['Original Price (USD)'][1], 2) == expected_original_prices[1]
    assert round(df['Original Price (USD)'][2], 2) == expected_original_prices[2]
    
    #Test if the calculated discount amount is correct
    assert round(df['Discount Amount (USD)'][0], 2) == expected_discount_amounts[0]
    assert round(df['Discount Amount (USD)'][1], 2) == expected_discount_amounts[1]
    assert round(df['Discount Amount (USD)'][2], 2) == expected_discount_amounts[2]


        
def test_calculate_roi(sample_data_file):
    
    calculator = DiscountCalculator(sample_data_file)
    df = calculator.return_on_investment()
    
    #Test if the ROI column was added successfully
    assert 'ROI (%)' in df.columns
    
    #Test if the calculated ROI is correct
    expected_roi = [0, 1000, 100]
    assert df['ROI (%)'][0] == expected_roi[0]
    assert df['ROI (%)'][1] == expected_roi[1]
    assert df['ROI (%)'][2] == expected_roi[2]
    
    
