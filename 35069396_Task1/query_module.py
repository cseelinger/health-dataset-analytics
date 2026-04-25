"""
Query_module that contains several functions for querying the loaded self.datasetset
for various information and insights.
"""

import csv
import logging
from statistics_module import StatisticsModule


class QueryModule:
    def __init__(self, data):
        self.dataset = data

    def export_to_csv(self, data, filename):
        """
        Save the result of a query (list of dictionaries) in a csv file
        """
        try:
            logging.info("Start exporting results to csv.")
            if not data:
                logging.error(f"No data available for export in '{filename}'.")
                return False

            headers = list(data[0].keys())
            with open(filename, "w", newline="") as output_file:
                export_data = csv.writer(output_file)
                # column names
                export_data.writerow(headers)
                # go through rows
                for row in data:
                    values = []
                    # go through headers to store into list
                    for column in headers:
                        values.append(row.get(column))
                    export_data.writerow(values)
            logging.info("Successfully exported results.")
            return True
        except Exception as e:
            logging.error(f"ERROR while exporting to CSV: {e}")
            return False

    # ----------------------------------------------------------------
    # i. Patients who smoke (or formerly smoked) and have hypertension
    # ----------------------------------------------------------------
    def query_smokers_hypertension(self):
        """
        Returns the mean, modal and median ages of patients
        who smoke or have smoked AND have hypertension.
        """
        try:
            logging.info("Start query i: Smokers with Hypertension.")
            if not self.dataset:
                return []
            ages = []
            for row in self.dataset:
                # check if hypertension and smoking
                smoke_status = row.get("Smoking Status")
                hypertension = row.get("Hypertension")

                # it is a smoking person with hypertension
                if hypertension == 1 and (
                    smoke_status == "Smokes" or smoke_status == "Formerly smoked"
                ):
                    age = row.get("Age")
                    # add age to ages list
                    ages.append(age)

            if not ages:
                return []

            # 2. Statistics (uses statistics_module)
            all_stats = {
                "Average Age": round(StatisticsModule.calculate_mean(ages), 2),
                "Median Age": round(StatisticsModule.calculate_median(ages), 2),
                "Modal Age": StatisticsModule.calculate_mode(ages),
            }
            # build result
            logging.info("Successfully filtered query i.")
            return [all_stats]
        except Exception as e:
            logging.error(f"ERROR in Query i (smokers hypertension): {e}")
            return []

    # ----------------------------------------------------------------
    # ii. Patients who have heart deseases
    # ----------------------------------------------------------------
    def query_heart_disease(self):
        """
        Returns the mean, modal and median ages, and the average glucose level
        of patients who have heart disease.
        """
        try:
            logging.info("Start query ii: Patients with Heart Disease.")
            if not self.dataset:
                return []
            # 1. filter data
            ages = []
            glucoses = []
            for row in self.dataset:
                # check if heart disease
                heart_disease = row.get("Heart Disease")

                # it is person with heart disease
                if heart_disease == 1:
                    age = row.get("Age")
                    glucose = row.get("Average Glucose Level")
                    if isinstance(age, int):
                        ages.append(age)
                    if isinstance(glucose, (int, float)):
                        glucoses.append(glucose)

            if not ages or not glucoses:
                return []

            # 2. Statistics (uses statistics_module)
            all_stats = {
                "Average Age": round(StatisticsModule.calculate_mean(ages), 2),
                "Median Age": round(StatisticsModule.calculate_median(ages), 2),
                "Modal Age": StatisticsModule.calculate_mode(ages),
                "Average Glucose Level": round(
                    StatisticsModule.calculate_mean(glucoses), 2
                ),
            }
            logging.info("Successfully filtered query ii.")
            return [all_stats]
        except Exception as e:
            logging.error(f"ERROR in Query ii (heart diseases): {e}")
            return []

    # ----------------------------------------------------------------
    # iii. Patients with hypertension
    #      Comparing patients with stroke occurrence and without,
    #      Grouped by gender
    # ----------------------------------------------------------------
    def query_hypertension_stroke_by_gender(self):
        """
        Returns the mean, modal and median ages of patients,
        comparing those with hypertension who had a stroke versus those with
        hypertension who did not have a stroke.
        Grouped by gender.
        """
        try:
            logging.info(
                "Start query iii: Patients with Hypertension, with/without Stroke, sort by Gender."
            )
            if not self.dataset:
                return []
            collected_data = {}
            for row in self.dataset:
                # get necessary self.dataset
                hypertension = row.get("Hypertension")
                stroke = row.get("Stroke Occurrence")
                gender = row.get("Gender")
                age = row.get("Age")

                # only include patients with hypertension
                if hypertension == 1:
                    # add new gender group (e.g. "Other") if not already in dict
                    if gender not in collected_data:
                        collected_data[gender] = {
                            "Stroke": [],  # with stroke
                            "No Stroke": [],  # without stroke
                        }
                    stroke_store_name = "Stroke" if stroke == 1 else "No Stroke"
                    # store age in correct gender/stroke combination
                    collected_data[gender][stroke_store_name].append(age)

            # 3. Get all information for the result from collected_data
            all_info = []
            for gender, stroke_groups in collected_data.items():
                for stroke_status, ages in stroke_groups.items():
                    if ages:
                        all_info.append(
                            {
                                "Gender": gender,
                                "Stroke Occurrence": (
                                    "Yes" if stroke_status == "Stroke" else "No"
                                ),
                                "Average Age": round(
                                    StatisticsModule.calculate_mean(ages), 2
                                ),
                                "Median Age": round(
                                    StatisticsModule.calculate_median(ages), 2
                                ),
                                "Modal Age": StatisticsModule.calculate_mode(ages),
                            }
                        )

            # build result
            logging.info("Successfully filtered query iii.")
            return all_info
        except Exception as e:
            logging.error(f"ERROR in Query iii (hypertension stroke by gender): {e}")
            return []

    # ----------------------------------------------------------------
    # iv. Physical activity: average values per level
    # ----------------------------------------------------------------
    def query_averages_physical_activity_level(self):
        """
        Computes the average BMI, average glucose level, and average stroke risk score
        for each physical activity level (Sedentary, Light, Moderate, Active).
        """
        try:
            logging.info("Start query iv: Average Values of Physical Activity Levels.")
            if not self.dataset:
                return []
            activities_values = {}
            # Store/Sort every value into the dictionary
            for row in self.dataset:
                activity = row.get("Physical Activity")
                if not activity:
                    continue

                # add activity level to the dict if not yet available
                if activity not in activities_values:
                    activities_values[activity] = {
                        "bmi": [],  # store all bmi values of this activity level
                        "glucose": [],  # store all glucose values of this activity level
                        "stroke_risk": [],  # store all stroke risk values of this activity level
                    }
                # get values
                bmi = row.get("BMI")
                glucose = row.get("Average Glucose Level")
                stroke_risk = row.get("Stroke Risk Score")
                # add every value to the list
                if isinstance(bmi, (int, float)):
                    activities_values[activity]["bmi"].append(bmi)
                if isinstance(glucose, (int, float)):
                    activities_values[activity]["glucose"].append(glucose)
                if isinstance(stroke_risk, (int, float)):
                    activities_values[activity]["stroke_risk"].append(stroke_risk)

            # build result dict
            averages = []

            for level, values in activities_values.items():
                if values["bmi"] and values["glucose"] and values["stroke_risk"]:
                    averages.append(
                        {
                            "Physical Activity": level,
                            "Average BMI": round(
                                StatisticsModule.calculate_mean(values["bmi"]), 2
                            ),
                            "Average Glucose Level": round(
                                StatisticsModule.calculate_mean(values["glucose"]), 2
                            ),
                            "Average Stroke Risk Score": round(
                                StatisticsModule.calculate_mean(values["stroke_risk"]),
                                2,
                            ),
                        }
                    )
            # build result
            logging.info("Successfully filtered query iv.")
            return averages
        except Exception as e:
            logging.error(f"ERROR in Query iv (averages physical activity level): {e}")
            return []

    # ----------------------------------------------------------------
    # v. Urban vs rural: averages of stroke patients
    # ----------------------------------------------------------------
    def query_urban_vs_rural_areas_with_stroke(self):
        """
        Computing the average age, modal age, and median age of patients
        who live in urban areas versus those in rural areas, for patients who had a stroke.
        """
        try:
            logging.info(
                "Start query v: Urban vs Rural: Average Values of Stroke Patients."
            )
            if not self.dataset:
                return []
            ages_rural = []
            ages_urban = []
            for row in self.dataset:
                # get data
                stroke = row.get("Stroke Occurrence")
                residence = row.get("Residence Type")
                age = row.get("Age")

                # just patients with stroke
                if stroke != 1:
                    continue

                if isinstance(age, (int, float)):
                    # add age to rural list
                    if residence == "Rural":
                        ages_rural.append(age)
                    # add age to urban list
                    if residence == "Urban":
                        ages_urban.append(age)

            # build result dicts
            rural_dict = {}
            urban_dict = {}
            # rural
            rural_dict = {
                "Residence Type": "Rural",
                "Average Age": round(StatisticsModule.calculate_mean(ages_rural), 2),
                "Modal Age": StatisticsModule.calculate_mode(ages_rural),
                "Median Age": round(StatisticsModule.calculate_median(ages_rural), 2),
            }
            # urban
            urban_dict = {
                "Residence Type": "Urban",
                "Average Age": round(StatisticsModule.calculate_mean(ages_urban), 2),
                "Modal Age": StatisticsModule.calculate_mode(ages_urban),
                "Median Age": round(StatisticsModule.calculate_median(ages_urban), 2),
            }

            # build result
            logging.info("Successfully filtered query v.")
            return [rural_dict, urban_dict]
        except Exception as e:
            logging.error(f"ERROR in Query v (urban vs rural areas with stroke): {e}")
            return []

    # ----------------------------------------------------------------
    # vi. Stroke vs no stroke: dietary habits
    # ----------------------------------------------------------------
    def query_dietary_habits(self):
        """
        Count number of different dietary habits for patients with stroke and no stroke.
        """
        try:
            logging.info("Start query vi: Stroke vs no Stroke: Dietary Habits.")
            if not self.dataset:
                return []
            # 1. retrieve dietary habits
            habits = []
            for row in self.dataset:
                habit = row.get("Dietary Habits")
                if habit not in habits:
                    habits.append(habit)

            dietary_stroke = []
            dietary_no_stroke = []
            for row in self.dataset:
                # get data
                habit = row.get("Dietary Habits")
                stroke = row.get("Stroke Occurrence")
                # sort in list for stroke or no stroke
                if stroke == 1:
                    dietary_stroke.append(habit)
                if stroke == 0:
                    dietary_no_stroke.append(habit)

            stroke_dict = {"Stroke Occurrence": "Yes"}
            no_stroke_dict = {"Stroke Occurrence": "No"}
            # add all habits for stroke and no stroke to the dict
            for habit in habits:
                stroke_dict[habit] = dietary_stroke.count(habit)
                no_stroke_dict[habit] = dietary_no_stroke.count(habit)

            # build result
            logging.info("Successfully filtered query vi.")
            return [stroke_dict, no_stroke_dict]
        except Exception as e:
            logging.error(f"ERROR in Query vi (dietary: stroke vs no stroke): {e}")
            return []

    # ----------------------------------------------------------------
    # vii. Patients with hypertension and stroke
    # ----------------------------------------------------------------
    def query_hypertension_results_in_stroke(self):
        """
        Return all patients whose hypertension resulted in a stroke
        """
        try:
            logging.info(
                "Start query vii: Patients whose Hypertension resulted in a Stroke."
            )
            if not self.dataset:
                return []

            result = []
            for row in self.dataset:
                # get information
                hypertension = row.get("Hypertension")
                stroke = row.get("Stroke Occurrence")
                # only add patient to list if they have hypertension and stroke
                if hypertension == 1 and stroke == 1:
                    result.append(row)

            logging.info("Successfully filtered query vii.")
            return result
        except Exception as e:
            logging.error(f"ERROR in Query vii (hypertension and stroke): {e}")
            return []

    # ----------------------------------------------------------------
    # viii. Patients with heart diseases and stroke
    # ----------------------------------------------------------------
    def query_heart_diseases_and_stroke(self):
        """
        Return all patients who have a heart disease and had a stroke
        """
        try:
            logging.info("Start query viii: Patients with Heart Disease and Stroke.")
            if not self.dataset:
                return []

            result = []
            for row in self.dataset:
                # get information
                heart_disease = row.get("Heart Disease")
                stroke = row.get("Stroke Occurrence")
                # only add patient to list if they have heart disease and stroke
                if heart_disease == 1 and stroke == 1:
                    result.append(row)

            logging.info("Successfully filtered query viii.")
            return result
        except Exception as e:
            logging.error(f"ERROR in Query viii (heart diseases and stroke): {e}")
            return []

    # ----------------------------------------------------------------
    # ix. Average sleep hours of patients with and without stroke
    # ----------------------------------------------------------------
    def query_average_sleep_hours(self):
        """
        Calculate the average sleep hours for patients with and without a stroke
        """
        try:
            logging.info(
                "Start query ix: Average Sleep Hours of patients with and without Stroke."
            )
            if not self.dataset:
                return []

            sleep_no_stroke = []
            sleep_stroke = []
            for row in self.dataset:
                stroke = row.get("Stroke Occurrence")
                if stroke == 1:
                    sleep_stroke.append(row.get("Sleep Hours"))
                if stroke == 0:
                    sleep_no_stroke.append(row.get("Sleep Hours"))
            sleep_avg_stroke = {
                "Stroke Occurrence": "Yes",
                "Average sleep hours": round(
                    StatisticsModule.calculate_mean(sleep_stroke), 2
                ),
            }
            sleep_avg_no_stroke = {
                "Stroke Occurrence": "No",
                "Average sleep hours": round(
                    StatisticsModule.calculate_mean(sleep_no_stroke), 2
                ),
            }

            logging.info("Successfully filtered query ix.")
            return [sleep_avg_stroke, sleep_avg_no_stroke]
        except Exception as e:
            logging.error(f"ERROR in Query ix (average sleep hours): {e}")
            return []

    # ----------------------------------------------------------------
    # x. Method to filter patients by given criteria
    # ----------------------------------------------------------------
    def query_filter_patients_by_criteria(
        self,
        age=None,
        minAge=None,
        maxAge=None,
        gender=None,
        hypertension=None,
        heartDisease=None,
        everMarried=None,
        worktype=None,
        residenceType=None,
        averageGlucoseLevel=None,
        minAverageGlucoseLevel=None,
        maxAverageGlucoseLevel=None,
        bmi=None,
        minBMI=None,
        maxBMI=None,
        smokingStatus=None,
        physicalActivity=None,
        dietaryHabits=None,
        alcoholConsumption=None,
        chronicStress=None,
        minSleepHours=None,
        sleepHours=None,
        maxSleepHours=None,
        familyHistoryOfStroke=None,
        educationLevel=None,
        incomeLevel=None,
        strokeRiskScore=None,
        minStrokeRiskScore=None,
        maxStrokeRiskScore=None,
        region=None,
        strokeOccurrence=None,
    ):
        """
        Return patients with given criteria
        """
        try:
            logging.info("Start query x: Filter patients by given criteria.")
            if not self.dataset:
                return []

            # set string for each parameter
            params = {
                "Age": age,
                "Gender": gender,
                "Hypertension": hypertension,
                "Heart Disease": heartDisease,
                "Ever Married": everMarried,
                "Work Type": worktype,
                "Residence Type": residenceType,
                "Average Glucose Level": averageGlucoseLevel,
                "BMI": bmi,
                "Smoking Status": smokingStatus,
                "Physical Activity": physicalActivity,
                "Dietary Habits": dietaryHabits,
                "Alcohol Consumption": alcoholConsumption,
                "Chronic Stress": chronicStress,
                "Sleep Hours": sleepHours,
                "Family History of Stroke": familyHistoryOfStroke,
                "Education Level": educationLevel,
                "Income Level": incomeLevel,
                "Stroke Risk Score": strokeRiskScore,
                "Region": region,
                "Stroke Occurrence": strokeOccurrence,
            }
            result = []
            for row in self.dataset:
                # go through all min/max possible values
                # min age
                if minAge is not None and row.get("Age") < minAge:
                    continue
                # max age
                if maxAge is not None and row.get("Age") > maxAge:
                    continue
                # min glucose level
                if (
                    minAverageGlucoseLevel is not None
                    and row.get("Average Glucose Level") < minAverageGlucoseLevel
                ):
                    continue
                # max glucose level
                if (
                    maxAverageGlucoseLevel is not None
                    and row.get("Average Glucose Level") > maxAverageGlucoseLevel
                ):
                    continue
                # min sleep hours
                if minSleepHours is not None and row.get("Sleep Hours") < minSleepHours:
                    continue
                # max sleep hours
                if maxSleepHours is not None and row.get("Sleep Hours") > maxSleepHours:
                    continue
                # min bmi
                if minBMI is not None and row.get("BMI") < minBMI:
                    continue
                # max bmi
                if maxBMI is not None and row.get("BMI") > maxBMI:
                    continue
                # min StrokeRiskScore
                if (
                    minStrokeRiskScore is not None
                    and row.get("Stroke Risk Score") < minStrokeRiskScore
                ):
                    continue
                # max StrokeRiskScore
                if (
                    maxStrokeRiskScore is not None
                    and row.get("Stroke Risk Score") > maxStrokeRiskScore
                ):
                    continue
                # go through all other values (no min/max)
                relevant = True
                for key, value in params.items():
                    # check if parameter is set
                    if value is not None:
                        # check if the set parameter is correct
                        if row.get(key) != value:
                            # parameter is set but not relevant/correct
                            relevant = False
                            break

                # add the patient to the result list because he/she relevant
                if relevant:
                    result.append(row)

            logging.info("Successfully filtered query x.")
            return result
        except Exception as e:
            logging.error(f"ERROR in Query x (feature extraction): {e}")
            return []

    # ----------------------------------------------------------------
    # xi. Categorize patients into stroke risk groups
    # ----------------------------------------------------------------
    def query_group_patients_stroke_risk(self):
        """
        Categorize patients into risk groups (Low, Medium, High) based on their stroke risk score.
        Returns the count and percentage of patients in each category.
        """
        try:
            logging.info("Start query xi: Categorize patients into Stroke Risk Groups.")
            if not self.dataset:
                return []

            # calculate risk groups through all stroke risk scores
            low = []
            medium = []
            high = []

            # sort patients into groups
            for row in self.dataset:
                stroke_risk_score = row.get("Stroke Risk Score")
                if stroke_risk_score < 34:
                    low.append(row)
                elif stroke_risk_score > 66:
                    high.append(row)
                else:
                    medium.append(row)

            # store all information
            result = []
            levels = ["Low", "Medium", "High"]
            index = 0
            for group in [low, medium, high]:
                information = {
                    "Stroke Risk Level": f"{levels[index]}",
                    "Count": len(group),
                    "Percentage": round((len(group) / len(self.dataset)) * 100, 2),
                }
                index += 1
                result.append(information)

            logging.info("Successfully filtered query xi.")
            return result
        except Exception as e:
            logging.error(
                f"ERROR in Query xi (group patients into stroke risk scores): {e}"
            )
            return []

    # ----------------------------------------------------------------
    # xii. Get a patient summary for each region
    # ----------------------------------------------------------------
    def query_summary_report_for_region(self):
        """
        Generate a summary report comparing health statistics across different regions (North, South, East, West),
        including average age, average BMI, average glucose level, and stroke occurrence rate for each region.
        """

        def get_average_of_feature(patients, feature):
            """
            Small funktion to calculate the average of a feature
            """
            feature_list = []

            for patient in patients:
                value = patient.get(feature)
                # check for int or float for calculating later
                if isinstance(value, (int, float)):
                    feature_list.append(value)

            if not feature_list:
                return None
            # get the stroke occurrence rate in percent
            if feature == "Stroke Occurrence":
                return round(StatisticsModule.calculate_mean(feature_list) * 100, 2)
            # otherwise just calculate the mean and round
            return round(StatisticsModule.calculate_mean(feature_list), 2)

        logging.info("Start query xii: Patient summary for each region of living.")
        if not self.dataset:
            return []

        try:
            # calculate region groups
            north = []
            south = []
            east = []
            west = []
            # sort patients into groups
            for row in self.dataset:
                region = row.get("Region")
                if region == "North":
                    north.append(row)
                elif region == "South":
                    south.append(row)
                elif region == "East":
                    east.append(row)
                elif region == "West":
                    west.append(row)

            # store all information
            result = []
            regions = ["North", "South", "East", "West"]
            index = 0
            for group in [north, south, east, west]:
                information = {
                    "Region": f"{regions[index]}",
                    "Count": len(group),
                    "Average Age": get_average_of_feature(group, "Age"),
                    "Average BMI": get_average_of_feature(group, "BMI"),
                    "Average Glucose Level": get_average_of_feature(
                        group, "Average Glucose Level"
                    ),
                    "Stroke Occurrence Rate": get_average_of_feature(
                        group, "Stroke Occurrence"
                    ),
                }
                index += 1
                result.append(information)

            logging.info("Successfully filtered query xii.")
            return result
        except Exception as e:
            logging.error(
                f"ERROR in Query xii (summary of patients from specific regions): {e}"
            )
            return []
