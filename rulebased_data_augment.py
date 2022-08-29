import json
import numpy as np
import pandas as pd

input_file = open('./17009003/CCTransformationExtraction/CCTrans_evaluation/Results_test_Manual_for_Unit_Test.json')
json_array = json.load(input_file)

print(json_array[0]["question"])

json_to_df = pd.json_normalize(json_array)
print(json_to_df["cctrans.extent"].unique())