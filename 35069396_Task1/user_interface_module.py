import tkinter as tk
from query_module import QueryModule

class UserInterface:
    def __init__(self, data):
        self.dataset = data
        self.queries = QueryModule(data)
    
    def run_query(self, number):
        result = []
        if number == 1:
            result = self.queries.query_smokers_hypertension()
        if number == 2:
            result = self.queries.query_heart_disease()
        if number == 3:
            result = self.queries.query_hypertension_stroke_by_gender()
        if number == 4:
            result = self.queries.query_averages_physical_activity_level()
        if number == 5:
            result = self.queries.query_urban_vs_rural_areas_with_stroke()
        if number == 6:
            result = self.queries.query_dietary_habits()
        if number == 7:
            result = self.queries.query_hypertension_results_in_stroke()
        if number == 8:
            result = self.queries.query_heart_diseases_and_stroke()
        if number == 9:
            result = self.queries.query_average_sleep_hours()
        if number == 10:
            result = self.queries.query_filter_patients_by_criteria()
        if number == 11:
            result = self.queries.query_group_patients_stroke_risk()
        if number == 12:
            result = self.queries.query_summary_report_for_region()

        self.result_label.config(text=str(result))    


    def start_interface(self):
        self.root = tk.Tk()
        self.root.title("Patient Health Analytics System")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        self.button = tk.Button(self.root, 
                                text="Run Query", 
                                command=lambda: self.run_query(1))
        self.button.pack()

        self.root.mainloop()
    









