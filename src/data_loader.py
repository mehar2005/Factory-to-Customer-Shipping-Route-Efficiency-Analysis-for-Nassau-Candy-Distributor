# Data Loader for Shipping Route Efficiency Analysis:
import pandas as pd
import openpyxl

def load_data(path):
    """
    Load the required data from a CSV file.
    Parameters:
    path (str): The file path to the CSV file containing the data.
    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    try:
        extension = path.split('.')[-1]
        if extension == 'csv':
            data = pd.read_csv(path)
        elif extension == 'xlsx':
            data = pd.read_excel(path, engine='openpyxl')
        elif extension == 'pkl':
            data = pd.read_pickle(path)
        else:
            print("Error: Unsupported file format. Please provide a CSV or Excel file.")
            return None
        return data
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error while reading the file.")
        return None

