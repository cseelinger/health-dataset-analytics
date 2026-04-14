import csv

class LoadDataset:
    """
    Class to load and parse the dataset
    """
    def __init__(self, file_path):
        self.data = []
        self.file_path = file_path

    def load_dataset(self):
        """
        Read and parse the dataset csv file
        """
        try:
            with open(self.file_path, 'r') as f:
                csv_reader = csv.reader(f)
                # get header from first row
                try:
                    headers = next(csv_reader)
                except Exception:
                    print("ERROR: The file is empty.")
                    return None

                row_number = 1

                for values in csv_reader:
                    row_number += 1
                    row = {}
                    i = 0
                    while i < len(headers):
                        if i < len(values):
                            row[headers[i]] = values[i]
                        else:
                            # if there are columns with headers without content
                            row[headers[i]] = ""
                        i = i + 1
                    try: 
                        parsed_row = self.parse_row(row)
                        self.data.append(parsed_row)
                    except Exception as e:
                        print(f"Error while parsing row {row_number}: {e}. Row will be skipped.")            
            
            print(f"Successfully loaded patient data: {len(self.data)}")
            return self.data

        except FileNotFoundError:
            print(f"ERROR: The File {self.file_path} was not found.")
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
        
        missing_values = ["", "nan", "NaN", "nan", "none", "null", "Null", "N/A", "n/a", "nn", "NN"]

        if value in missing_values:
            return True
        else:
            return False

    def parse_row(self, row):
        """
        Method parsing a row with converting into int or float if necessary/possible
        """
        result_row = {}
        for key, value in row.items():
            # clear each key and value to coninue (delete spaces)
            key = key.strip() if key else key
            val = value.strip() if isinstance(value, str) else value
            # continue if there is now no key
            if not key:
                continue
            # catch empty values ("") or "NaN" or "NN" etc. -> set to None
            if self.catch_missing_values(val):
                result_row[key] = None
                # skip remaining code
                continue

            # parse data to int/float if possible
            try:
                # try converting into int
                result_row[key] = int(val)
            except ValueError:
                try:
                    # try converting into float (it is not int)
                    result_row[key] = float(val)
                except ValueError:
                    # not int or float -> string
                    result_row[key] = val
            except Exception:
                # in case something unexpected gone wrong
                result_row[key] = None
        
        return result_row