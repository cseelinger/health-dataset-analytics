class StatisticsModule:
    """
    Class to perform statistical analyses on the patient dataset
    """
    def __init__(self, dataset):
        """
        Initialize statistic module with the loaded data
        """
        if not dataset:
            raise ValueError("Dataset is empty or invalid.")
        self.dataset = dataset

    # ---------------------------------------------
    # 1. Some statistic helper methods
    #    Can later also be used by the query module
    # ---------------------------------------------

    @staticmethod
    def calculate_mean(values):
        return sum(values) / len(values)

    @staticmethod
    def calculate_median(values):
        sorted_values = sorted(values)
        n = len(sorted_values)
        middle = n // 2

        if n % 2 == 0:
            return (sorted_values[middle - 1] + sorted_values[middle]) / 2
        else:
            return sorted_values[middle]

    @staticmethod
    def calculate_mode(values):
        counts = {}
        for val in values:
            counts[val] = counts.get(val, 0) + 1
        
        max_val = values[0]
        max_count = 0
        for val, count in counts.items():
            if count > max_count:
                max_count = count
                max_val = val
        return max_val
    
    @staticmethod
    def calculate_variance(values):
        if len(values) < 2:
            return 0.0

        mean_value = sum(values) / len(values)
        squared_diff_sum = 0

        for value in values:
            squared_diff_sum = squared_diff_sum + (value - mean_value) ** 2
        return squared_diff_sum / (len(values))
    
    @staticmethod
    def calculate_std_dev(values):
        if len(values) < 2:
            return 0.0

        variance = StatisticsModule.calculate_variance(values)
        return variance ** 0.5

    @staticmethod
    def calculate_min(values):
        return min(values)

    @staticmethod
    def calculate_max(values):
        return max(values)

    @staticmethod
    def calculate_range(values):
        return max(values) - min(values)

    def get_descriptive_statistics_for_feature(self, column):
        """
        Takes a column name as input and calculates all relevant statistics.
        Returns a dictionary containing the results.
        """
        try:
            # 1. Extract all valid (non-null) numeric values from the column
            values = []
            for row in self.dataset:
                val = row.get(column)
                # Check whether the value is a number (int or float)
                if type(val) == int or type(val) == float:
                    values.append(val)

            # 2. Check whether we have found any figures that can be analysed at all
            if not values:
                raise ValueError(f"No numerical data for the feature '{column}' found.")

            # 3. Calculate statistics 
            mean = round(self.calculate_mean(values), 2)
            median = round(self.calculate_median(values), 2)
            mode = self.calculate_mode(values)
            stdv = round(self.calculate_std_dev(values), 2)
            variance = round(self.calculate_variance(values), 2)
            minimum = self.calculate_min(values)
            maximum = self.calculate_max(values)
            rangee = self.calculate_range(values)

            # 4. store them in a dictionary
            stats = {
                "Feature": column,
                "Count (valid values)": len(values),
                "Mean": mean,
                "Median": median,
                "Mode": mode,
                "Standard Deviation": stdv,
                "Variance": variance,
                "Minimum": minimum,
                "Maximum": maximum,
                "Range": rangee
            }
            return stats

        except ValueError as e:
            print(f"Error in {column}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected Error has occurred: {e}")
            return None