"""
Module that produces a user interface. Usage of tkinter. The user interface provides the
functionality for querying the system for any query in query_module and displaying the results. 
The queries and displayed results are user-friendly.
The interface includes:
i.	 A menu or selection system allowing users to choose which query or analysis to perform.
ii.	 Input fields where necessary (e.g., for entering age ranges, selecting regions, or choosing
     filter criteria).
iii. A results display area that presents the output in a clear, readable format.
iv.	 An option to export query results to a CSV file.
v.	 The ability to view descriptive statistics for any selected feature.
vi.	 The option for users to continue using the system or quit when they are done.

"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from query_module import QueryModule
from statistics_module import StatisticsModule
import logging


class UserInterface:
    def __init__(self, data):
        self.queries = QueryModule(data)
        self.statistics = StatisticsModule(data)

        self.last_left_result = []
        self.last_right_result = []

    # --------------------------------------
    # Some helper methods
    # --------------------------------------
    def get_int_or_none(self, integer):
        """
        Return int if parsable into int
        """
        value = integer.get().strip()
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            messagebox.showerror(title="ERROR", message=f"{value} is not an integer. Field will be ignored.")
            return None

    def get_float_or_none(self, number):
        """
        Return float if parsable into float
        """
        value = number.get().strip()
        if value == "":
            return None
        try:
            return float(value)
        except ValueError:
            messagebox.showerror(title="ERROR", message=f"{value} is not a float. Field will be ignored.")
            return None

    def get_string_or_none(self, value):
        """
        Return None if nothing is written in the field
        """
        if value == "":
            return None
        return value

    def get_bool_or_none(self, value):
        """
        Convert Yes/No into booleans
        """
        if value == "Yes":
            return 1
        elif value == "No":
            return 0
        return None

    # ---------------------------------
    # Start interface
    # 1. build left side of the window
    # 2. build right side of the window
    # ---------------------------------
    def start_interface(self):
        """
        Initialize tkinter Interface
        """
        self.root = tk.Tk()
        self.root.title("Patient Health Analytics System")
        self.root.geometry("1000x600")

        # create two columns
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.left = tk.Frame(self.root, padx=20, pady=20)
        self.right = tk.Frame(self.root, padx=20, pady=20)

        self.left.grid(row=0, column=0, sticky="nsew")
        self.right.grid(row=0, column=1, sticky="nsew")

        self.build_left_side()
        self.build_right_side()

        # create quit button to end program
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy)
        self.quit_button.grid(row=1, column=1, sticky="e", padx=20, pady=20)

        self.root.mainloop()

    def build_left_side(self):
        """
        Build everything placed/written on the left side of the window
        """
        # heading
        self.left_title = tk.Label(
            self.left, text="Queries", font=("Arial", 16, "bold")
        )
        self.left_title.pack(anchor="w", pady=(0, 10))

        # dropdown menu
        self.left_var = tk.StringVar()
        self.left_var.set("Please choose")

        self.query_descriptions = [
            "Smokers with Hypertension",
            "Patients with Heart Disease",
            "Patients with Hypertension, with/without Stroke, sort by Gender",
            "Average Values of Physical Activity Levels",
            "Urban vs Rural: Average Values of Stroke Patients",
            "Stroke vs no Stroke: Dietary Habits",
            "Patients whose Hypertension resulted in a Stroke",
            "Patients with Heart Disease and Stroke",
            "Average Sleep Hours of patients with and without Stroke",
            "Filter patients by following criteria:",
            "Categorize patients into Stroke Risk Groups",
            "Patient summary for each region of living",
        ]

        self.left_menu = tk.OptionMenu(
            self.left, self.left_var, *self.query_descriptions
        )
        self.left_menu.pack(anchor="w", fill="x")

        # run button
        self.left_run_button = tk.Button(
            self.left, text="Run", command=self.run_query
        )
        self.left_run_button.pack(anchor="w", pady=(10, 10))

        # result field
        self.left_result_text = tk.Text(self.left, height=20, width=55)
        self.left_result_text.pack(fill="both", expand=True)

        # export button
        self.left_export_button = tk.Button(
            self.left, text="Export Results", command=self.export_left_result
        )
        self.left_export_button.pack(anchor="w", pady=(10, 0))

    def build_right_side(self):
        """
        Build everything placed/written on the right side of the window
        """
        # heading
        self.right_title = tk.Label(
            self.right, text="Descriptive Statistics", font=("Arial", 16, "bold")
        )
        self.right_title.pack(anchor="w", pady=(0, 10))

        # dropdown menu
        self.right_var = tk.StringVar()
        self.right_var.set("Please choose")

        self.right_options = [
            "Age",
            "BMI",
            "Average Glucose Level",
            "Sleep Hours",
            "Stroke Risk Score",
        ]

        self.right_menu = tk.OptionMenu(
            self.right, self.right_var, *self.right_options
        )
        self.right_menu.pack(anchor="w", fill="x")

        # run button
        self.right_run_button = tk.Button(
            self.right, text="Run", command=self.run_descriptive_statistics
        )
        self.right_run_button.pack(anchor="w", pady=(10, 10))

        # result field
        self.right_result_text = tk.Text(self.right, height=20, width=55)
        self.right_result_text.pack(fill="both", expand=True)

        # export button
        self.right_export_button = tk.Button(
            self.right, text="Export Results", command=self.export_right_result
        )
        self.right_export_button.pack(anchor="w", pady=(10, 0))

    # ------------------
    # Run specific query
    # ------------------
    def run_query(self):
        """
        Run the query selected in the drop down menu.
        """
        selection = self.left_var.get()
        # get query for selection
        if selection == "Smokers with Hypertension":
            result = self.queries.query_smokers_hypertension()
        elif selection == "Patients with Heart Disease":
            result = self.queries.query_heart_disease()
        elif (
            selection
            == "Patients with Hypertension, with/without Stroke, sort by Gender"
        ):
            result = self.queries.query_hypertension_stroke_by_gender()
        elif selection == "Average Values of Physical Activity Levels":
            result = self.queries.query_averages_physical_activity_level()
        elif selection == "Urban vs Rural: Average Values of Stroke Patients":
            result = self.queries.query_urban_vs_rural_areas_with_stroke()
        elif selection == "Stroke vs no Stroke: Dietary Habits":
            result = self.queries.query_dietary_habits()
        elif selection == "Patients whose Hypertension resulted in a Stroke":
            result = self.queries.query_hypertension_results_in_stroke()
        elif selection == "Patients with Heart Disease and Stroke":
            result = self.queries.query_heart_diseases_and_stroke()
        elif selection == "Average Sleep Hours of patients with and without Stroke":
            result = self.queries.query_average_sleep_hours()
        elif selection == "Filter patients by following criteria:":
            self.open_window_for_filter_criteria()
            return
        elif selection == "Categorize patients into Stroke Risk Groups":
            result = self.queries.query_group_patients_stroke_risk()
        elif selection == "Patient summary for each region of living":
            result = self.queries.query_summary_report_for_region()
        else:
            messagebox.showwarning(title="WARNING", message="No query is chosen.")
            return

        if not result:
            messagebox.showwarning(
                title="WARNING", message="No data could be calculated."
            )
            return
        # save the result for exporting now or later
        self.last_left_result = result
        # show result in window field
        self.show_result(self.left_result_text, result)

    def run_descriptive_statistics(self):
        """
        Run the descriptive statistics method from the statistics module.
        """
        selection = self.right_var.get()

        if selection == "Please choose":
            messagebox.showwarning(title="WARNING", message="No feature is chosen.")
            return
        # calculate descriptive statistics
        result = self.statistics.get_descriptive_statistics_for_feature(selection)

        if result is None:
            self.last_right_result = []
        else:
            self.last_right_result = result
        # show result in field in window
        self.show_result(self.right_result_text, result)

    # --------------------------------------------
    # Show and export results in left/right window
    # --------------------------------------------
    def show_result(self, text, result):
        """
        Display result under the drop down menu, calculated by the query module.
        """
        text.delete("1.0", tk.END)

        if not result:
            text.insert(tk.END, "No suitable patients found.")
            return
        # result is alsways returned as list []
        # -> go through list and show result
        for item in result:
            for key, value in item.items():
                text.insert(tk.END, f"{key}: {value}\n")
            text.insert(tk.END, "\n")

    def export_left_result(self):
        self.export_result("left")

    def export_right_result(self):
        self.export_result("right")

    def export_result(self, side):
        """
        Export the result of the descriptive statistics to a csv file.
        """
        # decide what result from which side should be exported
        data_to_export = (
            self.last_left_result if side == "left" else self.last_right_result
        )
        # check if calculated data available for export
        if not data_to_export:
            messagebox.showwarning(
                title="WARNING", message="No result available for export."
            )
            return
        # open filedialog for choosing filename and path
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )

        if not filename:
            return
        # export_to_csv returns true or false when exported
        success = self.queries.export_to_csv(data_to_export, filename)
        # inform user about success or failing export
        if success:
            messagebox.showinfo(
                title="SUCCESS", message="Result exported successfully."
            )
        else:
            messagebox.showerror(title="ERROR", message="Export failed.")

    # ------------------------------------------------------
    # Query: Filter patients by following criteria
    # 1. Prepare the variables for the filter criteria query
    # 2. Open window to select/insert information for filter
    # ------------------------------------------------------
    def build_variables_for_filter_criteria(self, parent):
        """
        Build every line in two columns to build input fields for the filter criteria method
        -> For every feature can be inserted or selected a value
        """
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(3, weight=1)

        # age
        self.age_label = tk.Label(parent, text="Exact Age:")
        self.age_entry = tk.Entry(parent)

        # min age
        self.min_age_label = tk.Label(parent, text="Min Age:")
        self.min_age_entry = tk.Entry(parent)

        # max age
        self.max_age_label = tk.Label(parent, text="Max Age:")
        self.max_age_entry = tk.Entry(parent)

        # gender
        self.gender_label = tk.Label(parent, text="Gender:")
        self.gender_var = tk.StringVar()
        self.gender_var.set("")

        self.gender_menu = tk.OptionMenu(
            parent, self.gender_var, "", "Female", "Male", "Other"
        )

        # hypertension
        self.hypertension_label = tk.Label(parent, text="Hypertension:")
        self.hypertension_var = tk.StringVar()
        self.hypertension_var.set("")

        self.hypertension_menu = tk.OptionMenu(
            parent, self.hypertension_var, "", "Yes", "No"
        )

        # heart disease
        self.heart_disease_label = tk.Label(parent, text="Heart Disease:")
        self.heart_disease_var = tk.StringVar()
        self.heart_disease_var.set("")

        self.heart_disease_menu = tk.OptionMenu(
            parent, self.heart_disease_var, "", "Yes", "No"
        )

        # ever Married
        self.ever_married_label = tk.Label(parent, text="Ever Married:")
        self.ever_married_var = tk.StringVar()
        self.ever_married_var.set("")

        self.ever_married_menu = tk.OptionMenu(
            parent, self.ever_married_var, "", "Yes", "No"
        )

        # worktype
        self.worktype_label = tk.Label(parent, text="Worktype:")
        self.worktype_var = tk.StringVar()
        self.worktype_var.set("")

        self.worktype_menu = tk.OptionMenu(
            parent,
            self.worktype_var,
            "",
            "Government",
            "Private",
            "Never Worked",
            "Children",
            "Self-employed",
        )

        # residence type
        self.residence_label = tk.Label(parent, text="Residence Type:")
        self.residence_var = tk.StringVar()
        self.residence_var.set("")

        self.residence_menu = tk.OptionMenu(
            parent, self.residence_var, "", "Rural", "Urban"
        )

        # glucose
        self.glucose_label = tk.Label(parent, text="Exact Average Glucose Level:")
        self.glucose_entry = tk.Entry(parent)
        self.min_glucose_label = tk.Label(parent, text="Min Average Glucose Level:")
        self.min_glucose_entry = tk.Entry(parent)
        self.max_glucose_label = tk.Label(parent, text="Max Average Glucose Level:")
        self.max_glucose_entry = tk.Entry(parent)
        # bmi
        self.bmi_label = tk.Label(parent, text="Exact BMI:")
        self.bmi_entry = tk.Entry(parent)
        self.min_bmi_label = tk.Label(parent, text="Min BMI:")
        self.min_bmi_entry = tk.Entry(parent)
        self.max_bmi_label = tk.Label(parent, text="Max BMI:")
        self.max_bmi_entry = tk.Entry(parent)
        # smoking status
        self.smoking_label = tk.Label(parent, text="Smoking Status:")
        self.smoking_var = tk.StringVar()
        self.smoking_var.set("")

        self.smoking_menu = tk.OptionMenu(
            parent, self.smoking_var, "", "Never smoked", "Formerly smoked", "Smokes"
        )
        # physical activity
        self.physical_activity_label = tk.Label(parent, text="Physical Activity Level:")
        self.physical_activity_var = tk.StringVar()
        self.physical_activity_var.set("")

        self.physical_activity_menu = tk.OptionMenu(
            parent,
            self.physical_activity_var,
            "",
            "Sedentary",
            "Light",
            "Active",
            "Moderate",
        )
        # dietary habits
        self.dietary_label = tk.Label(parent, text="Dietary Habits:")
        self.dietary_var = tk.StringVar()
        self.dietary_var.set("")

        self.dietary_menu = tk.OptionMenu(
            parent, self.dietary_var, "", "Vegetarian", "Non-Vegetarian", "Mixed"
        )
        # alcohol consumption
        self.alcohol_label = tk.Label(parent, text="Alcohol Consumption:")
        self.alcohol_var = tk.StringVar()
        self.alcohol_var.set("")

        self.alcohol_menu = tk.OptionMenu(parent, self.alcohol_var, "", "Yes", "No")
        # chronic stress
        self.stress_label = tk.Label(parent, text="Chronic Stress:")
        self.stress_var = tk.StringVar()
        self.stress_var.set("")

        self.stress_menu = tk.OptionMenu(parent, self.stress_var, "", "Yes", "No")
        # sleep hours
        self.sleep_label = tk.Label(parent, text="Exact Sleep Hours:")
        self.sleep_entry = tk.Entry(parent)
        self.min_sleep_label = tk.Label(parent, text="Min Sleep Hours:")
        self.min_sleep_entry = tk.Entry(parent)
        self.max_sleep_label = tk.Label(parent, text="Max Sleep Hours:")
        self.max_sleep_entry = tk.Entry(parent)
        # family stroke history
        self.family_label = tk.Label(parent, text="Family Stroke History:")
        self.family_var = tk.StringVar()
        self.family_var.set("")

        self.family_menu = tk.OptionMenu(parent, self.family_var, "", "Yes", "No")
        # education level
        self.education_label = tk.Label(parent, text="Education Level:")
        self.education_var = tk.StringVar()
        self.education_var.set("")

        self.education_menu = tk.OptionMenu(
            parent, self.education_var, "", "Primary", "Secondary", "Tertiary"
        )
        # income level
        self.income_label = tk.Label(parent, text="Income Level:")
        self.income_var = tk.StringVar()
        self.income_var.set("")

        self.income_menu = tk.OptionMenu(
            parent, self.income_var, "", "Low", "Middle", "High"
        )
        # stroke risk score
        self.stroke_risk_label = tk.Label(parent, text="Exact Stroke Risk Score:")
        self.stroke_risk_entry = tk.Entry(parent)
        # stroke risk min
        self.min_stroke_risk_label = tk.Label(parent, text="Min Stroke Risk Score:")
        self.min_stroke_risk_entry = tk.Entry(parent)
        # stroke risk max
        self.max_stroke_risk_label = tk.Label(parent, text="Max Stroke Risk Score:")
        self.max_stroke_risk_entry = tk.Entry(parent)

        # region
        self.region_label = tk.Label(parent, text="Region:")
        self.region_var = tk.StringVar()
        self.region_var.set("")

        self.region_menu = tk.OptionMenu(
            parent, self.region_var, "", "North", "South", "East", "West"
        )

        # stroke occurrence
        self.stroke_occ_label = tk.Label(parent, text="Stroke Occurrence:")
        self.stroke_occ_var = tk.StringVar()
        self.stroke_occ_var.set("")

        self.stroke_occ_menu = tk.OptionMenu(
            parent, self.stroke_occ_var, "", "Yes", "No"
        )

        # -----------------------------------
        # Layout inside window
        # -----------------------------------
        # age
        self.age_label.grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.age_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        self.min_age_label.grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.min_age_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        self.max_age_label.grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.max_age_entry.grid(row=2, column=1, sticky="ew", padx=4, pady=4)
        # gender
        self.gender_label.grid(row=3, column=0, sticky="w", padx=4, pady=4)
        self.gender_menu.grid(row=3, column=1, sticky="ew", padx=4, pady=4)
        # hypertension
        self.hypertension_label.grid(row=4, column=0, sticky="w", padx=4, pady=4)
        self.hypertension_menu.grid(row=4, column=1, sticky="ew", padx=4, pady=4)
        # heart disease
        self.heart_disease_label.grid(row=5, column=0, sticky="w", padx=4, pady=4)
        self.heart_disease_menu.grid(row=5, column=1, sticky="ew", padx=4, pady=4)
        # ever married
        self.ever_married_label.grid(row=6, column=0, sticky="w", padx=4, pady=4)
        self.ever_married_menu.grid(row=6, column=1, sticky="ew", padx=4, pady=4)
        # worktype
        self.worktype_label.grid(row=7, column=0, sticky="w", padx=4, pady=4)
        self.worktype_menu.grid(row=7, column=1, sticky="ew", padx=4, pady=4)
        # residence type
        self.residence_label.grid(row=8, column=0, sticky="w", padx=4, pady=4)
        self.residence_menu.grid(row=8, column=1, sticky="ew", padx=4, pady=4)
        # Glucose
        self.glucose_label.grid(row=9, column=0, sticky="w", padx=4, pady=4)
        self.glucose_entry.grid(row=9, column=1, sticky="ew", padx=4, pady=4)
        self.min_glucose_label.grid(row=10, column=0, sticky="w", padx=4, pady=4)
        self.min_glucose_entry.grid(row=10, column=1, sticky="ew", padx=4, pady=4)
        self.max_glucose_label.grid(row=11, column=0, sticky="w", padx=4, pady=4)
        self.max_glucose_entry.grid(row=11, column=1, sticky="ew", padx=4, pady=4)
        # bmi
        self.bmi_label.grid(row=12, column=0, sticky="w", padx=4, pady=4)
        self.bmi_entry.grid(row=12, column=1, sticky="ew", padx=4, pady=4)
        self.min_bmi_label.grid(row=13, column=0, sticky="w", padx=4, pady=4)
        self.min_bmi_entry.grid(row=13, column=1, sticky="ew", padx=4, pady=4)
        self.max_bmi_label.grid(row=14, column=0, sticky="w", padx=4, pady=4)
        self.max_bmi_entry.grid(row=14, column=1, sticky="ew", padx=4, pady=4)
        # smoking status
        self.smoking_label.grid(row=15, column=0, sticky="w", padx=4, pady=4)
        self.smoking_menu.grid(row=15, column=1, sticky="ew", padx=4, pady=4)
        # physical activity
        self.physical_activity_label.grid(row=1, column=2, sticky="w", padx=4, pady=4)
        self.physical_activity_menu.grid(row=1, column=3, sticky="ew", padx=4, pady=4)
        # dietary habits
        self.dietary_label.grid(row=2, column=2, sticky="w", padx=4, pady=4)
        self.dietary_menu.grid(row=2, column=3, sticky="ew", padx=4, pady=4)
        # alcohol consumption
        self.alcohol_label.grid(row=3, column=2, sticky="w", padx=4, pady=4)
        self.alcohol_menu.grid(row=3, column=3, sticky="ew", padx=4, pady=4)
        # chronic stress
        self.stress_label.grid(row=4, column=2, sticky="w", padx=4, pady=4)
        self.stress_menu.grid(row=4, column=3, sticky="ew", padx=4, pady=4)
        # sleep hours
        self.sleep_label.grid(row=5, column=2, sticky="w", padx=4, pady=4)
        self.sleep_entry.grid(row=5, column=3, sticky="ew", padx=4, pady=4)
        self.min_sleep_label.grid(row=6, column=2, sticky="w", padx=4, pady=4)
        self.min_sleep_entry.grid(row=6, column=3, sticky="ew", padx=4, pady=4)
        self.max_sleep_label.grid(row=7, column=2, sticky="w", padx=4, pady=4)
        self.max_sleep_entry.grid(row=7, column=3, sticky="ew", padx=4, pady=4)
        # family stroke history
        self.family_label.grid(row=8, column=2, sticky="w", padx=4, pady=4)
        self.family_menu.grid(row=8, column=3, sticky="ew", padx=4, pady=4)
        # education level
        self.education_label.grid(row=9, column=2, sticky="w", padx=4, pady=4)
        self.education_menu.grid(row=9, column=3, sticky="ew", padx=4, pady=4)
        # income level
        self.income_label.grid(row=10, column=2, sticky="w", padx=4, pady=4)
        self.income_menu.grid(row=10, column=3, sticky="ew", padx=4, pady=4)
        # stroke risk score
        self.stroke_risk_label.grid(row=11, column=2, sticky="w", padx=4, pady=4)
        self.stroke_risk_entry.grid(row=11, column=3, sticky="ew", padx=4, pady=4)
        self.min_stroke_risk_label.grid(row=12, column=2, sticky="w", padx=4, pady=4)
        self.min_stroke_risk_entry.grid(row=12, column=3, sticky="ew", padx=4, pady=4)
        self.max_stroke_risk_label.grid(row=13, column=2, sticky="w", padx=4, pady=4)
        self.max_stroke_risk_entry.grid(row=13, column=3, sticky="ew", padx=4, pady=4)
        # region
        self.region_label.grid(row=14, column=2, sticky="w", padx=4, pady=4)
        self.region_menu.grid(row=14, column=3, sticky="ew", padx=4, pady=4)
        # stroke occurrence
        self.stroke_occ_label.grid(row=15, column=2, sticky="w", padx=4, pady=4)
        self.stroke_occ_menu.grid(row=15, column=3, sticky="ew", padx=4, pady=4)

    def open_window_for_filter_criteria(self):
        """
        Open a new window for selecting filter criteria.
        """
        # build window
        self.filter_window = tk.Toplevel(self.root)
        self.filter_window.title("Filter Patients")
        self.filter_window.geometry("650x650")

        self.filter_frame = tk.Frame(self.filter_window, padx=10, pady=10)
        self.filter_frame.pack(fill="both", expand=True)
        
        # build al variables to be set
        self.build_variables_for_filter_criteria(self.filter_frame)
        
        # build button OK
        button_frame = tk.Frame(self.filter_window, padx=10, pady=10)
        button_frame.pack(fill="x", side="bottom")
        ok_button = tk.Button(
            button_frame, text="OK", command=self.get_all_inserted_filter_from_window
        )
        ok_button.pack(side="left")

        # build button QUIT
        quit_button = tk.Button(
            button_frame, text="Quit", command=self.filter_window.destroy
        )
        quit_button.pack(side="right")

    def get_all_inserted_filter_from_window(self):
        """
        Read all filter values from the filter window and run the filter query.
        """
        # age
        exact_age = self.get_int_or_none(self.age_entry)
        min_age = self.get_int_or_none(self.min_age_entry)
        max_age = self.get_int_or_none(self.max_age_entry)

        # gender
        gender = self.get_string_or_none(self.gender_var.get())

        # hypertension
        hypertension = self.get_bool_or_none(self.hypertension_var.get())

        # heart disease
        heart_disease = self.get_bool_or_none(self.heart_disease_var.get())

        # ever married
        ever_married = self.get_bool_or_none(self.ever_married_var.get())

        # worktype
        work_type = self.get_string_or_none(self.worktype_var.get())

        # residence type
        residence_type = self.get_string_or_none(self.residence_var.get())

        # glucose
        glucose = self.get_float_or_none(self.glucose_entry)
        min_glucose = self.get_float_or_none(self.min_glucose_entry)
        max_glucose = self.get_float_or_none(self.max_glucose_entry)

        # bmi
        bmi = self.get_float_or_none(self.bmi_entry)
        min_bmi = self.get_float_or_none(self.min_bmi_entry)
        max_bmi = self.get_float_or_none(self.max_bmi_entry)

        # smoking status
        smoking_status = self.get_string_or_none(self.smoking_var.get())

        # physical activity
        physical_act = self.get_string_or_none(self.physical_activity_var.get())

        # dietary habits
        dietary_habits = self.get_string_or_none(self.dietary_var.get())

        # alcohol consumption
        alcohol = self.get_bool_or_none(self.alcohol_var.get())

        # chronic stress
        chronic_stress = self.get_bool_or_none(self.stress_var.get())

        # sleep hours
        sleep_hours = self.get_int_or_none(self.sleep_entry)
        min_sleep = self.get_int_or_none(self.min_sleep_entry)
        max_sleep = self.get_int_or_none(self.max_sleep_entry)

        # family stroke history
        family_stroke = self.get_bool_or_none(self.family_var.get())

        # education level
        education_level = self.get_string_or_none(self.education_var.get())

        # income level
        income_level = self.get_string_or_none(self.income_var.get())

        # stroke risk score
        stroke_risk = self.get_int_or_none(self.stroke_risk_entry)
        min_stroke = self.get_int_or_none(self.min_stroke_risk_entry)
        max_stroke = self.get_int_or_none(self.max_stroke_risk_entry)

        # region
        region = self.get_string_or_none(self.region_var.get())

        # stroke occurrence
        stroke_occ = self.get_bool_or_none(self.stroke_occ_var.get())

        result = self.queries.query_filter_patients_by_criteria(
            age=exact_age,
            minAge=min_age,
            maxAge=max_age,
            gender=gender,
            hypertension=hypertension,
            heartDisease=heart_disease,
            everMarried=ever_married,
            worktype=work_type,
            residenceType=residence_type,
            averageGlucoseLevel=glucose,
            minAverageGlucoseLevel=min_glucose,
            maxAverageGlucoseLevel=max_glucose,
            bmi=bmi,
            minBMI=min_bmi,
            maxBMI=max_bmi,
            smokingStatus=smoking_status,
            physicalActivity=physical_act,
            dietaryHabits=dietary_habits,
            alcoholConsumption=alcohol,
            chronicStress=chronic_stress,
            minSleepHours=min_sleep,
            sleepHours=sleep_hours,
            maxSleepHours=max_sleep,
            familyHistoryOfStroke=family_stroke,
            educationLevel=education_level,
            incomeLevel=income_level,
            strokeRiskScore=stroke_risk,
            minStrokeRiskScore=min_stroke,
            maxStrokeRiskScore=max_stroke,
            region=region,
            strokeOccurrence=stroke_occ,
        )

        if not result:
            logging.warning("No data could be calculated from filter function.")
            messagebox.showwarning(
                title="WARNING", message="No data could be calculated."
            )
            return
        # show result in field
        self.last_left_result = result
        self.show_result(self.left_result_text, result)

        self.filter_window.destroy()
