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
        # directly load dataset
        self.load_dataset()

    def load_dataset(self):
        """
        Read and parse the dataset csv file and store it directly in self.dataset
        """
        try:
            with open(self.filepath, 'r') as f:
                csv_reader = csv.reader(f)
                # get header from first row
                try:
                    headers = next(csv_reader)
                except Exception:
                    print("ERROR: The file is empty.")
                    return None

                row_number = 1
                # go through all rows
                for row in csv_reader:
                    row_number += 1
                    # new storage for the rows (dict)
                    new_row = {}
                    i = 0
                    # go through all columns and sort values to headers (key)
                    while i < len(headers):
                        # get value just if there is content in this column
                        if i < len(row):
                            new_row[headers[i]] = row[i]
                        else:
                            # if there are columns with headers without content
                            new_row[headers[i]] = ""
                        i += 1
                    try: 
                        # turn missing values into None and number into int/float
                        parsed_row = self.process_row(new_row)
                        self.dataset.append(parsed_row)
                    except Exception as e:
                        print(f"Error while parsing row {row_number}: {e}. Row will be skipped.")            
            
            print(f"Successfully loaded patient data: {len(self.dataset)}")
            return self.dataset

        except FileNotFoundError:
            print(f"ERROR: The File {self.filepath} was not found.")
            return None
        except Exception as e:
            print(f"Unknown Error while loading the dataset: {e}")
            return None

    def catch_missing_values(self, value):
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

    def process_row(self, current_row):
        """
        Method parsing a row with converting into int or float if necessary/possible
        """
        row = {}
        for key, value in current_row.items():
            # catch empty values ("") or "NaN" or "NN" etc. -> set to None
            if self.catch_missing_values(value):
                row[key] = None
                # skip remaining code in process_row
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
            except Exception:
                # in case something unexpected gone wrong
                row[key] = None
        
        return row