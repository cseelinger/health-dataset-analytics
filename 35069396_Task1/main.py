from load_dataset_module import LoadDataset
from query_module import query_filter_patients_by_criteria


def print_test_result(title, result, show_rows=False, max_rows=3):
    """
    Prints the test title, number of matching patients,
    and optionally the first few rows.
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if result is None:
        print("Result is None")
        return

    print("Number of matching patients:", len(result))

    if not result:
        print("No matching patients found.")
        return

    if show_rows:
        print("\nFirst matching rows:")
        count = 0
        for row in result:
            print(row)
            count = count + 1
            if count >= max_rows:
                break


def main():
    # load dataset
    loader = LoadDataset("data.csv")
    data = loader.load_dataset()

    if not data:
        print("Dataset could not be loaded.")
        return

    print("Dataset loaded successfully.")
    print("Number of records:", len(data))

    # ------------------------------------------------------------
    # Tests for query_filter_patients_by_criteria
    # ------------------------------------------------------------

    # 1. no filter at all
    result = query_filter_patients_by_criteria(data)
    print_test_result("Test 1: No filters", result)

    # 2. only gender
    result = query_filter_patients_by_criteria(data, gender="Female")
    print_test_result("Test 2: Only gender = Female", result)

    # 3. only age range
    result = query_filter_patients_by_criteria(data, minAge=40, maxAge=60)
    print_test_result("Test 3: Age between 40 and 60", result)

    # 4. only region
    result = query_filter_patients_by_criteria(data, region="South")
    print_test_result("Test 4: Region = South", result)

    # 5. only smoking status
    result = query_filter_patients_by_criteria(data, smokingStatus="Formerly smoked")
    print_test_result("Test 5: Smoking Status = Formerly smoked", result)

    # 6. hypertension only
    result = query_filter_patients_by_criteria(data, hypertension=1)
    print_test_result("Test 6: Hypertension = 1", result)

    # 7. stroke occurrence only
    result = query_filter_patients_by_criteria(data, strokeOccurrence=1)
    print_test_result("Test 7: Stroke Occurrence = 1", result)

    # 8. BMI range only
    result = query_filter_patients_by_criteria(data, minBMI=20, maxBMI=30)
    print_test_result("Test 8: BMI between 20 and 30", result)

    # 9. glucose range only
    result = query_filter_patients_by_criteria(data, minAverageGlucoseLevel=100, maxAverageGlucoseLevel=200)
    print_test_result("Test 9: Average Glucose Level between 100 and 200", result)

    # 10. sleep range only
    result = query_filter_patients_by_criteria(data, minSleepHours=6, maxSleepHours=8)
    print_test_result("Test 10: Sleep Hours between 6 and 8", result)

    # 11. stroke risk score range only
    result = query_filter_patients_by_criteria(data, minStrokeRiskScore=50, maxStrokeRiskScore=80)
    print_test_result("Test 11: Stroke Risk Score between 50 and 80", result)

    # 12. combined: female + hypertension
    result = query_filter_patients_by_criteria(data, gender="Female", hypertension=1)
    print_test_result("Test 12: Female and Hypertension = 1", result)

    # 13. combined: male + age + region
    result = query_filter_patients_by_criteria(data, minAge=50, maxAge=70, gender="Male", region="North")
    print_test_result("Test 13: Male, age 50-70, region North", result)

    # 14. combined: smoking + bmi + glucose
    result = query_filter_patients_by_criteria(
        data,
        smokingStatus="Smokes",
        minBMI=25,
        maxBMI=35,
        minAverageGlucoseLevel=120
    )
    print_test_result("Test 14: Smokes, BMI 25-35, glucose >= 120", result)

    # 15. combined: physical activity + diet + alcohol
    result = query_filter_patients_by_criteria(
        data,
        physicalActivity="Light",
        dietaryHabits="Vegetarian",
        alcoholConsumption=0
    )
    print_test_result("Test 15: Light activity, Vegetarian, alcohol = 0", result)

    # 16. combined: heart disease + stroke occurrence
    result = query_filter_patients_by_criteria(
        data,
        heartDisease=1,
        strokeOccurrence=1
    )
    print_test_result("Test 16: Heart Disease = 1 and Stroke Occurrence = 1", result)

    # 17. combined: many filters together
    result = query_filter_patients_by_criteria(
        data,
        minAge=30,
        maxAge=80,
        gender="Female",
        hypertension=1,
        smokingStatus="Formerly smoked",
        region="South"
    )
    print_test_result("Test 17: Multiple filters together", result, show_rows=True)

    # 18. impossible combination -> should return 0 rows
    result = query_filter_patients_by_criteria(
        data,
        gender="Male",
        everMarried=0,
        minAge=120
    )
    print_test_result("Test 18: Impossible combination", result)

    # 19. education + income
    result = query_filter_patients_by_criteria(
        data,
        educationLevel="Tertiary",
        incomeLevel="High"
    )
    print_test_result("Test 19: Education = Tertiary and Income = High", result)

    # 20. family history + chronic stress + stroke
    result = query_filter_patients_by_criteria(
        data,
        familyHistoryOfStroke=1,
        chronicStress=1,
        strokeOccurrence=1
    )
    print_test_result("Test 20: Family history, chronic stress, and stroke", result, show_rows=True)


if __name__ == "__main__":
    main()