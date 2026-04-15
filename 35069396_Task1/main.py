from load_dataset_module import LoadDataset
from query_module import QueryModule

dataload = LoadDataset("data.csv")

print(dataload.dataset[:1])

query_iii = QueryModule.query_hypertension_stroke_by_gender(dataload)

for i in query_iii:
    print(i)

