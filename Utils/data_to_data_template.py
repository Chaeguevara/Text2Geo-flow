from numpy import single
import pandas as pd
import json


def get_kor_geoname_as_df():
    input_1 = open("../02_Dataset2Template/lv1_korea_geo.json")
    input_2 = open("../02_Dataset2Template/lv2_korea_geo.json")
    input_3 = open("../02_Dataset2Template/lv3_korea_geo.json")
    js_ar1 = json.load(input_1)
    js_ar2 = json.load(input_2)
    js_ar3 = json.load(input_3)
    js_df1 = pd.json_normalize(js_ar1)
    js_df2 = pd.json_normalize(js_ar2)
    js_df3 = pd.json_normalize(js_ar3)
    return js_df1, js_df2, js_df3


def json_to_frame(data_path):
    input_file = open(data_path)
    json_arry = json.load(input_file)
    json_to_df = pd.json_normalize(json_arry)
    return json_to_df


def list_in_df_to_df(df):
    extent_frame = df["cctrans.extent"].apply(pd.Series)
    extent_frame.columns = ["extent", "extent", "extent"]
    return extent_frame


def get_index_by_length(extent_frame):
    extent_count_df = extent_frame.T.count().to_frame()
    extent_count_df.columns = ['count']
    singe_ext_idx = extent_count_df[extent_count_df['count'] != 1].index
    double_ext_idx = extent_count_df[extent_count_df['count'] != 2].index
    triple_ext_idx = extent_count_df[extent_count_df['count'] != 3].index
    return singe_ext_idx, double_ext_idx, triple_ext_idx


def df_by_index(idx_1, idx_2, idx_3, df):
    df = df.copy()
    df_1 = df.drop(idx_1)
    df_2 = df.drop(idx_2)
    df_3 = df.drop(idx_3)
    return df_1, df_2, df_3


if __name__ == "__main__":
    data_path = '../Data/Results_test_Manual.json'
    ko_geo1, ko_geo2, ko_geo3 = get_kor_geoname_as_df()
    print(ko_geo2.iloc[0, :])
    data_frame = json_to_frame(data_path)
    extent_frame = list_in_df_to_df(data_frame)
    single_idx, double_idx, triple_idx = get_index_by_length(extent_frame)
    df_1, df_2, df_3 = df_by_index(
        single_idx, double_idx, triple_idx, data_frame
    )


