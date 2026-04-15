class StatisticsModule:
    """
    Class to perform statistical analyses on the patient dataset
    """
    def __init__(self, dataset):
        # Initialize statistic module with the loaded data
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
        # first sort values
        sorted_values = sorted(values)
        n = len(sorted_values)
        middle = n // 2
        # number of values is even: get the mean of the two values in the middle
        if n % 2 == 0:
            return (sorted_values[middle - 1] + sorted_values[middle]) / 2
        # number of values is odd: just get the middle
        else:
            return sorted_values[middle]

    @staticmethod
    def calculate_mode(values):
        counts = {}
        # count every value and store the count in the dict
        for val in values:
            counts[val] = counts.get(val, 0) + 1
        # start with first value
        max_val = values[0]
        max_count = 0
        for val, count in counts.items():
            # if current value has higher count than last stored
            if count > max_count:
                # store new value in max_val
                max_count = count
                max_val = val
        return max_val
    
    @staticmethod
    def calculate_variance(values):
        """
        variance:
        [ 1 / (n - 1) ] * sum( (x - mean(x))² )
        """
        if len(values) < 2:
            return 0
        # calculate mean value
        mean_value = sum(values) / len(values)
        variance = 0

        for val in values:
            # sum squared part of variance
            variance = variance + (val - mean_value) ** 2
        return variance / (len(values) - 1)
    
    @staticmethod
    def calculate_standard_deviation(values):
        """
        standard deviation:
        square_root(variance)
        """
        if len(values) < 2:
            return 0

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

    def get_descriptive_statistics_for_feature(self, feature):
        """
        Takes a column name as input and calculates all relevant statistics.
        Returns a dictionary containing the results.
        """
        try:
            # 1. Extract all valid (non-null and numeric) values from the column
            values = []
            for row in self.dataset:
                val = row.get(feature)
                # Check whether the value is a number (int or float)
                if type(val) == int or type(val) == float:
                    values.append(val)

            # 2. Check whether we have found any figures that can be analysed at all
            if not values:
                raise ValueError(f"No numerical data for the feature '{feature}' found.")

            # 3. Calculate statistics 
            mean = round(self.calculate_mean(values), 2)
            median = round(self.calculate_median(values), 2)
            mode = self.calculate_mode(values)
            standard_deviation = round(self.calculate_standard_deviation(values), 2)
            variance = round(self.calculate_variance(values), 2)
            minimum = self.calculate_min(values)
            maximum = self.calculate_max(values)
            rangee = self.calculate_range(values)

            # 4. store them in a dictionary
            statistics = {
                "Feature": feature,
                "Count (valid values)": len(values),
                "Mean": mean,
                "Median": median,
                "Mode": mode,
                "Standard Deviation": standard_deviation,
                "Variance": variance,
                "Minimum": minimum,
                "Maximum": maximum,
                "Range": rangee
            }
            return statistics

        except ValueError as e:
            print(f"Error in {feature}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected Error has occurred: {e}")
            return None