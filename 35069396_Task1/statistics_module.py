"""
This module should implement functions for statistical analysis of the dataset features.
The statistical functions should include the following:
mean, mode, median, standard deviation, minimum, maximum, variance, and range.
These functions will be used by other modules to compute statistics for different patient groups.
Additionally, implement a function that returns descriptive statistics for any specified numeric feature
of the dataset. This function should accept a feature name as a parameter
and return all relevant statistics (mean, median, mode, standard deviation, minimum, maximum, variance, range)
for that feature.

"""

import logging


class StatisticsModule:
    """
    Class to perform statistical analyses on the patient dataset
    """

    def __init__(self, dataset):
        # Initialize statistic module with the loaded data
        self.dataset = dataset

    # ---------------------------------------------
    # 1. Some statistic helper methods
    #    Can later also be used by the query module
    # ---------------------------------------------

    @staticmethod
    def calculate_mean(values):
        if not values:
            return None
        return sum(values) / len(values)

    @staticmethod
    def calculate_median(values):
        if not values:
            return None
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
        if not values:
            return None
        counts = {}
        # count every value and store the count in the dict
        for val in values:
            counts[val] = counts.get(val, 0) + 1
        # start with first value
        max_val = values[0]
        max_count = 1
        for val, count in counts.items():
            # if current value has higher count than last stored
            if count > max_count:
                # store new value in max_val
                max_count = count
                max_val = val
        return max_val

    @staticmethod
    def calculate_variance(values):
        if not values:
            return None
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
        if not values:
            return None
        """
        standard deviation:
        square_root(variance)
        """
        if len(values) < 2:
            return 0

        variance = StatisticsModule.calculate_variance(values)

        return variance**0.5

    @staticmethod
    def calculate_min(values):
        if not values:
            return None
        return min(values)

    @staticmethod
    def calculate_max(values):
        if not values:
            return None
        return max(values)

    @staticmethod
    def calculate_range(values):
        if not values:
            return None
        return max(values) - min(values)

    def get_descriptive_statistics_for_feature(self, feature):
        """
        Takes a column name as input and calculates all relevant statistics.
        Returns a dictionary containing the results.
        """
        logging.info(f"Calculating descriptive statistics for {feature}")

        if not self.dataset:
            logging.error("No data in dataset found.")
            return None

        # extract all valid (non-null and numeric) values from the column
        values = []
        for row in self.dataset:
            val = row.get(feature)
            # Check whether the value is a number (int or float)
            if isinstance(val, (int, float)):
                values.append(val)

        if not values:
            logging.warning("No descriptive statistics found.")
            return None

        # clculate statistics
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
            "Count": len(values),
            "Mean": mean,
            "Median": median,
            "Mode": mode,
            "Standard Deviation": standard_deviation,
            "Variance": variance,
            "Minimum": minimum,
            "Maximum": maximum,
            "Range": rangee,
        }

        return statistics
