"""
The data to be retrieved will be temporarily stored in memory (for additional processing) 
using an appropriate data structure such as a dictionary or a list of dictionaries.
This module should return a data structure (e.g., patient_data dictionary) that contains patient records 
with their corresponding health features. 
The module should also handle any data type conversions needed 
(e.g., converting numeric strings to integers or floats).

"""

import csv

class LoadDataset:
    """
    Class to load and parse the dataset
    data is stored in an array of dictionaries, e.g.
    [   
        <<-- first row -->>
        {'ID': 1, 
        'Age': 78, 
        'Gender': 'Female', 
        'Hypertension': 0, 
        ...
        'Stroke Occurrence': 0}, 

        <<-- second row -->>
        {'ID': 2, 
        'Age': 60, 
        'Gender': 'Female', 
        'Hypertension': 0, 
        ...},

        <<-- next rows -->>
    ]
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataset = []

    def load_dataset(self):
        """
        Read and parse the dataset csv file and store it directly in self.dataset
        """
        try:
            with open(self.filepath, 'r') as f:
                loaded_data = csv.reader(f)
                # get header from first row
                try:
                    headers = next(loaded_data)
                except Exception:
                    print("ERROR: The file is empty.")
                    return None

                row_number = 1
                # go through all rows of the file
                for row in loaded_data:
                    row_number += 1
                    # new storage for the row
                    new_row = {}
                    # go through all columns and sort values to headers (key)
                    for i in range(len(headers)):
                        # get value just if there is content in this column
                        if i < len(row):
                            new_row[headers[i]] = row[i]
                        else:
                            # if there are columns with headers without content
                            new_row[headers[i]] = ""
                    try: 
                        # turn missing values into None and number into int/float
                        finished_row = self.process_one_row(new_row)
                        self.dataset.append(finished_row)
                    except Exception as e:
                        print(f"ERROR while parsing row {row_number}: {e}. Row will be skipped.")            
            
            print(f"Successfully loaded patient data: {len(self.dataset)}")
            return self.dataset

        except FileNotFoundError:
            print(f"ERROR: The File {self.filepath} was not found.")
            return None
        except Exception as e:
            print(f"Unknown ERROR while loading the dataset: {e}")
            return None

    def get_missing_values(self, value):
        """
        Returns True if a value represents a missing value (e.g. NaN)
        """
        if value is None:
            return True
        
        missing_values = ["", "nan", "NaN", "nan", "none", "None", "null", "Null", "N/A", "n/a", "nn", "NN"]
        
        # return true if it is a missing value so it can be set to None
        if value in missing_values:
            return True
        else:
            return False

    def process_one_row(self, current_row):
        """
        Method parsing a row with converting into int or float if necessary/possible
        """
        row = {}
        for key, value in current_row.items():
            # get empty values ("") or "NaN" or "NN" etc. -> set to None
            if self.get_missing_values(value):
                row[key] = None
                # skip remaining code in process_one_row
                continue

            # parse data to int/float if possible
            try:
                # try converting into int
                row[key] = int(value)
            except ValueError:
                try:
                    # try converting into float (it is not int)
                    row[key] = float(value)
                except ValueError:
                    # not int or float -> string
                    row[key] = value
        
        return row