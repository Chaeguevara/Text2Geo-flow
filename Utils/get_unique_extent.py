import pandas as pd
import json

def path_2_df(path):
    input_file = open(path)
    json_array = json.load(input_file)
    json_to_df = pd.json_normalize(json_array)
    return json_to_df

path_1="../Results_test_Manual.json"

df = path_2_df(path_1)
extent_frame=df["cctrans.extent"].apply(pd.Series) # list to each element
extent_frame.columns=["Extent","Extent","Extent"]
extent1 = extent_frame.iloc[:, 0].to_frame()
extent2 = extent_frame.iloc[:, 1].to_frame()
extent3 = extent_frame.iloc[:, 2].to_frame()
un_1 = extent1["Extent"].unique()
un_2 = extent2["Extent"].unique()
un_3 = extent3["Extent"].unique()
unique_set = set(un_1.flatten())
unique_set = unique_set .union(set(un_2.flatten()), set(un_3.flatten()))
unique_set = {x for x in unique_set if x == x}
unique_list = list(unique_set)
unique_list.sort()
con_2_cor = []
for item in unique_list:
    con_2_cor.append({item: {"Nation": "", "Admin_lv": ""}})


print(con_2_cor)

# %%
res = json.dumps(con_2_cor, indent=3)
with open("./Unique_extent_from_origin.json", "w") as f:
    f.write(res)
