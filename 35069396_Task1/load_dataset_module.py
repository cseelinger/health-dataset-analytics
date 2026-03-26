import csv

class LoadDataset():
    """
    Class to load and parse the dataset
    """
    def __init__(self, file_path: str):
        self.data = []
        self.file_path = file_path
        # helpful to inform the user if there were missing values 
        # or unexpected problems occured
        self.missing_values_count = 0

    def load_dataset(self):
        """
        Read and parse the dataset csv file
        """
        try:
            with open(self.file_path, 'r') as f:
                csv_reader = csv.DictReader(f)

                for index, row in enumerate(csv_reader, 1):
                    try: 
                        parsed_row = self.parse_row(row)
                        self.data.append(parsed_row)
                    except Exception as e:
                        print(f"Error while parsing of row {index}: {e}. Row will be skipped.")            
            # information about missing values or unexpected problems while parsing a value
            if self.missing_values_count > 0:
                print(f"\033[93mWARNING: {self.missing_values_count} values could not be parsed correctly or were empty/missing values. They entered 'None' in the record.\033[0m")
            else:
                print(f"Successfully loaded patient data: {len(self.data)}")
            return self.data

        except FileNotFoundError:
            print(f"Error: The File {self.file_path} was not found.")
            return None
        except Exception as e:
            print(f"Unnkown Error while loading the dataset: {e}")
            return None

    def _catch_missing_values(value) -> bool:
        """
        Returns True if a value represents a missing value (e.g. NaN)
        """
        if value is None:
            return True

        if isinstance(value, str):
            value = value.strip().lower()

        match value:
            case "" | "nan" | "none" | "null" | "n/a" | None:
                return True
            case _:
                return False

    def parse_row(self, row: dict):
        """
        Parse a row with converting into int or float if necessary/possible
        """
        parsed_data = {}
        for key, value in row.items():
            # clear each key and value to coninue (delete spaces)
            clean_key = key.strip() if key else key
            clean_value = value.strip() if isinstance(value, str) else value
            # continue if there is now no key
            if not clean_key:
                continue
            # catch empty values ("") or "NaN" or "NN"
            if self._catch_missing_values(clean_value):
                parsed_data[clean_key] = None
                # count empty values to inform the user that values are missing
                self.missing_values_count += 1
                continue

            # parse data to int/float if possible
            try:
                # first try to convert into float
                float_value = float(clean_value)
                # check the possibility of the value being an int
                if float_value.is_integer():
                    # it is an integer
                    parsed_data[clean_key] = int(float_value)
                else:
                    # it is a float
                    parsed_data[clean_key] = float_value
            except ValueError:
                # if it is not a number stay being a string
                parsed_data[clean_key] = clean_value
            except Exception as e:
                # normally this exception will never happen because DictReader of csv
                # garantees that we get all values as strings
                # but for defensive programming reasons, I decided to add this
                parsed_data[clean_key] = None
                self.missing_values_count += 1
        
        return parsed_data