from ctypes import alignment
import json
from operator import concat
from tkinter import Grid
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def path_2_df(path):
    input_file = open(path)
    json_array = json.load(input_file)
    json_to_df = pd.json_normalize(json_array)
    return json_to_df

path1 = '../17009003/CCTransformationExtraction/CCTrans_evaluation/Results_test_Auto.json'
path2 = '../17009003/CCTransformationExtraction/CCTrans_evaluation/Results_test_Manual.json'

data_df = path_2_df(path2)


extent_seriese=data_df["cctrans.extent"].apply(pd.Series) # list to each element
extent_df = extent_seriese.T.count().to_frame()
extent_df.columns=['Number of Extent']
print(extent_df)
print(type(extent_df))

num_of_extent = extent_df['Number of Extent'].value_counts()
num_of_extent = num_of_extent.to_frame()
print(num_of_extent)
print(type(num_of_extent))

num_of_extent.plot(
    title="Number of extents in each question",
    kind="bar",
)
plt.xlabel("Number of extents in a question")
plt.ylabel("Corresponding questions")
plt.yticks(np.arange(0,120,5))

plt.show()

# print(set(oneD_to_2D.values.ravel()))


## Visualize all type
# types = json_to_df["cctrans.types"].apply(pd.Series)


# print(types.T.count())