import csv
from statistics_module import StatisticsModule

class QueryModule:
    """
    Class 
    """
    def __init__(self, dataset):
        if not dataset:
            raise ValueError("Dataset is empty or not valid.")
        self.dataset = dataset
    
    def export_to_csv(self, data, filename):
        """
        Save the result of a query (list of dictionaries) in a csv file
        """
        if not data:
            print(f"No data available for export of '{filename}'.")
            return False
        
        try:
            fieldnames = data[0].keys()
            with open(filename, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error while exporting to CSV: {e}")
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
            # 1. filter data
            filtered_ages = []
            for row in self.dataset:
                # check if hypertension and smoking
                status = str(row.get('Smoking Status', '')).lower()
                hypertension = row.get('Hypertension')

                # it is a smoking person with hypertension
                if hypertension == 1 and (status == 'smokes' or status == 'formerly smokes'):
                    age = row.get('Age')
                    if type(age) == int or type(age) == float:
                        filtered_ages.append(age)
            if not filtered_ages:
                return [{"Message": "No suitable patients found."}]
            
            # 2. Statistics (uses statistics_module)
            result = [{
                "Query": "Smokers (or Former Smokers) with Hypertension",
                "Count": len(filtered_ages),
                "Average Age": round(StatisticsModule.calculate_mean(filtered_ages), 2),
                "Median Age": round(StatisticsModule.calculate_median(filtered_ages), 2),
                "Modal Age": StatisticsModule.calculate_mode(filtered_ages)
            }]
            return result

        except Exception as e:
            print(f"Error in Query i (smokers hypertension): {e}")
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
            # 1. filter data
            filtered_ages = []
            filtered_glucose = []
            for row in self.dataset:
                # check if heart disease
                heart_disease = row.get('Heart Disease')

                # it is person with heart disease
                if heart_disease == 1:
                    age = row.get('Age')
                    glucose = row.get('Average Glucose Level')
                    if type(age) == int or type(age) == float:
                        filtered_ages.append(age)
                    if type(glucose) == int or type(glucose) == float:
                        filtered_glucose.append(glucose)
            if not filtered_ages or not filtered_glucose:
                return [{"Message": "No suitable patients found."}]
            
            # 2. Statistics (uses statistics_module)
            result = [{
                "Query": "Persons with Heart Diseases",
                "Count": len(filtered_ages),
                "Average Age": round(StatisticsModule.calculate_mean(filtered_ages), 2),
                "Median Age": round(StatisticsModule.calculate_median(filtered_ages), 2),
                "Modal Age": StatisticsModule.calculate_mode(filtered_ages),
                "Average Glucose Level": round(StatisticsModule.calculate_mean(filtered_glucose), 2)
            }]
            return result

        except Exception as e:
            print(f"Error in Query ii (heart diseases): {e}")
            return []

    # ----------------------------------------------------------------
    # iii. Patients with hypertension
    #      Comparing patients with heart attacks with patients without,
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
            # 1. Collect ages by gender and stroke status
            grouped_data = {}
            for row in self.dataset:
                # get necessary data
                hypertension = row.get('Hypertension')
                stroke = row.get('Stroke Occurrence')
                gender = str(row.get('Gender', 'Unknown')).strip()
                age = row.get('Age')

                # only include patients with hypertension
                if hypertension == 1 and stroke in [0, 1]:
                    if type(age) == int or type(age) == float:
                        if gender not in grouped_data:
                            grouped_data[gender] = {
                                1: [],   # with stroke
                                0: []    # without stroke
                            }
                        grouped_data[gender][stroke].append(age)

            if not grouped_data:
                return [{"Message": "No suitable patients found."}]
            
            # 2. Build result list
            result = []
            
            # 3. Get all information for the result
            for gender, stroke_groups in grouped_data.items():
                for stroke_status, ages in stroke_groups.items():
                    if ages:
                        result.append({
                            "Query": "Hypertension by Gender and Stroke Status",
                            "Gender": gender,
                            "Stroke Occurrence": "Had Stroke" if stroke_status == 1 else "No Stroke",
                            "Count": len(ages),
                            "Average Age": round(StatisticsModule.calculate_mean(ages), 2),
                            "Median Age": round(StatisticsModule.calculate_median(ages), 2),
                            "Modal Age": StatisticsModule.calculate_mode(ages)
                        })

            if not result:
                return [{"Message": "No suitable patients found."}]

            return result

        except Exception as e:
            print(f"Error in Query iii (hypertension stroke by gender): {e}")
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
            grouped_activity = {}
            # Store/Sort every value into the dictionary
            for row in self.dataset:
                activity = str(row.get('Physical Activity', '')).strip()

                if not activity:
                    continue

                if activity not in grouped_activity:
                    grouped_activity[activity] = {
                        "bmi": [],        # store all bmi values of this activity level
                        "glucose": [],    # store all glucose values of this activity level
                        "stroke_risk": [] # store all stroke risk values of this activity level
                    }
                bmi = row.get('BMI')
                glucose = row.get('Average Glucose Level')
                stroke_risk = row.get('Stroke Risk Score')

                if type(bmi) == int or type(bmi) == float:
                    grouped_activity[activity]["bmi"].append(bmi)

                if type(glucose) == int or type(glucose) == float:
                    grouped_activity[activity]["glucose"].append(glucose)

                if type(stroke_risk) == int or type(stroke_risk) == float:
                    grouped_activity[activity]["stroke_risk"].append(stroke_risk)

            result = []

            for level, values in grouped_activity.items():
                if values["bmi"] and values["glucose"] and values["stroke_risk"]:
                    result.append({
                                "Query": "Average values for activity level",
                                "Physical Activity": level,
                                "Average BMI": round(StatisticsModule.calculate_mean(values["bmi"]), 2),
                                "Average Glucose Level": round(StatisticsModule.calculate_mean(values["glucose"]), 2),
                                "Average Stroke Risk Score": round(StatisticsModule.calculate_mean(values["stroke_risk"]), 2)
                            })

            if not result:
                return [{"Message": "No suitable patients found."}]

            return result

        except Exception as e:
            print(f"Error in Query iv (averages physical activity level): {e}")
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
            filtered_ages_rural = []
            filtered_ages_urban = []
            for row in self.dataset:
                stroke = row.get('Stroke Occurrence')
                residence = str(row.get('Residence Type', '')).strip()
                age = row.get('Age')

                if stroke != 1:
                    continue
                if type(age) != int and type(age) != float:
                    continue
                if residence == "Rural":
                    filtered_ages_rural.append(age)
                if residence == "Urban":
                    filtered_ages_urban.append(age)
            
            result = []
            if filtered_ages_rural:
                result.append({
                            "Query": "Average values for Rural stroke patients",
                            "Residence Type": "Rural",
                            "Count": len(filtered_ages_rural),
                            "Average Age": round(StatisticsModule.calculate_mean(filtered_ages_rural), 2),
                            "Modal Age": StatisticsModule.calculate_mode(filtered_ages_rural),
                            "Median Age": round(StatisticsModule.calculate_median(filtered_ages_rural), 2)
                        })
            if filtered_ages_urban:
                result.append({
                            "Query": "Average values for Urban stroke patients",
                            "Residence Type": "Urban",
                            "Count": len(filtered_ages_urban),
                            "Average Age": round(StatisticsModule.calculate_mean(filtered_ages_urban), 2),
                            "Modal Age": StatisticsModule.calculate_mode(filtered_ages_urban),
                            "Median Age": round(StatisticsModule.calculate_median(filtered_ages_urban), 2)
                        })

            if not result:
                return [{"Message": "No suitable patients found."}]

            return result
                
        except Exception as e:
            print(f"Error in Query v (urban vs rural areas with stroke): {e}")
            return []
