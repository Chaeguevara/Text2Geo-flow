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


extent_frame=data_df["cctrans.extent"].apply(pd.Series) # list to each element
extent_frame.columns=["Extent","Extent","Extent"]
extent_df = extent_frame.T.count().to_frame()
extent_df.columns=['Number of Extent']
# print(extent_df)
# print(type(extent_df))

# get unique extents count
extent1 = extent_frame.iloc[:,0].to_frame()
extent1_count = extent1.value_counts()
extent2 = extent_frame.iloc[:,1].to_frame()
extent2_count = extent2.value_counts()
extent3 = extent_frame.iloc[:,2].to_frame()
extent3_count = extent3.value_counts()

extent_count = pd.concat([extent1_count,extent2_count,extent3_count]).groupby("Extent").sum().reset_index()
extent_count.columns=["Extent","Extent Count"]
# print(extent_count)

def plot_dataframe(df_name,title,kind,xlabel,ylabel,x_column,rotation,fontsize):
    df_name.plot(
        title=title,
        kind=kind,
        x=x_column
    )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation,ha='center',fontsize=fontsize)
    return plt




'''plot  ,
# num_of_extent.plot(
#     title="Number of extents in each question",
#     kind="bar",
# )
# plt.xlabel("Number of extents in a question")
# plt.ylabel("Corresponding questions")
# plt.yticks(np.arange(0,120,5))

# plt.show()
'''


'''
get all unique extent name
'''

# print(extent_frame.count(axis="columns"))
# extent_per_question_plot = plot_dataframe(extent_frame.count(axis="columns"),"Extent count by Question index","bar","question idx","used extent count","extent",rotation=90,fontsize=6)
# extent_per_question_plot.yticks(np.arange(0,4,1))
# extent_per_question_plot.show()

# plot_dataframe(extent_count,"Extent usage count","bar","extent","number","Extent",45).show()


'''
About transformation
'''

# trx_frame=data_df["cctrans.transformation"].apply(pd.Series) # list to each element
# print(trx_frame)
# trx_count_by_quest_id = trx_frame.count(axis="columns")

# plot_dataframe(trx_count_by_quest_id,"Trasformation count per question idx","bar","question idx","transformation count","extent",rotation=90,fontsize=6).show()
# print(trx_count_by_quest_id)

'''
Abount types used
'''
types_frame = data_df["cctrans.types"].apply(pd.Series) # list to each element
types_frame.columns=["type1","type2","type3","type4","type5","type6","type7","type8"]
# 1. count most frequently used  type
# convert json into something
def get_value_from_dict(x,key):
    try:
        x[key]
        return x[key]
    except KeyError:
        return

print(type(types_frame["type1"][0]))
types_frame_only_types = types_frame.applymap(lambda x:get_value_from_dict(x,"type"),na_action="ignore")
types_frame_only_types = types_frame_only_types.applymap(lambda x:len(list(x)),na_action="ignore")
type_count_only = pd.DataFrame(types_frame_only_types.to_numpy().ravel()).value_counts()
type_count_only.plot(
    title="test",
    kind='bar'
)
plt.show()

# types_frame_nested = pd.json_normalize(
#     types_frame.to_dict(),
#     record_path=["type1"]
# )
# print(types_frame_nested)

# print(types_frame)