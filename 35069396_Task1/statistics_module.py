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

        for value in values:
            if value in counts:
                counts[value] = counts[value] + 1
            else:
                counts[value] = 1

        max_count = max(counts.values())

        mode_values = []
        for key, count in counts.items():
            if count == max_count:
                mode_values.append(key)

        if len(mode_values) == 1:
            return mode_values[0]
        else:
            # no unique mode found
            return None
    
    @staticmethod
    def calculate_variance(values):
        if len(values) < 2:
            return 0.0

        mean_value = sum(values) / len(values)
        squared_diff_sum = 0

        for value in values:
            squared_diff_sum = squared_diff_sum + (value - mean_value) ** 2
        # calculate sample variance by dividing through len(values) - 1
        return squared_diff_sum / (len(values) - 1)
    
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

    def get_descriptive_statistics_for_feature(self, feature_name):
        """
        Takes a column name as input and calculates all relevant statistics.
        Returns a dictionary containing the results.
        """
        try:
            # 1. Extract all valid (non-null) numeric values from the column
            values = []
            for row in self.dataset:
                val = row.get(feature_name)
                # Check whether the value is a number (int or float) and exists
                # ignore booleans although bool is a subtype of int in Python
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    values.append(val)

            # 2. Check whether we have found any figures that can be analysed at all
            if not values:
                raise ValueError(f"No numerical data for the feature '{feature_name}' found.")

            # 3. Calculate statistics and store them in a dictionary
            stats = {
                "Feature": feature_name,
                "Count (valid values)": len(values),
                "Mean": round(self.calculate_mean(values), 2),
                "Median": round(self.calculate_median(values), 2),
                "Mode": self.calculate_mode(values),
                "Standard Deviation": round(self.calculate_std_dev(values), 2),
                "Variance": round(self.calculate_variance(values), 2),
                "Minimum": self.calculate_min(values),
                "Maximum": self.calculate_max(values),
                "Range": self.calculate_range(values)
            }
            return stats

        except ValueError as ve:
            print(f"Error in statistical analysis: {ve}")
            return None
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
            return None