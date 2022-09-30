import json
import pandas as pd
import numpy as np
import argparse


JSON_PATH = "../Data/Results_test_Manual.json"
KOR_PATH_1 = "../Data/lv1_korea_geo.json"
KOR_PATH_2 = "../Data/lv2_korea_geo.json"
KOR_PATH_3 = "../Data/lv3_korea_geo.json"
CC_DUP_BEFORE_PATH = "../Data/cctrans_dup_before.gzip"
KOR_DUP_PATH = "../Data/kor_dup_before.gzip"


def get_cctrans_as_df():
    input_file = open(JSON_PATH)
    json_array = json.load(input_file)
    json_to_df = pd.json_normalize(json_array)
    json_to_df.to_csv("../Data/dataset_to_df.csv")
    return json_to_df


def get_korea_extents():
    # Load data -> Initial DF
    kor_input_1 = open(KOR_PATH_1)
    kor_input_2 = open(KOR_PATH_2)
    kor_input_3 = open(KOR_PATH_3)
    kor_geojson_1 = json.load(kor_input_1)
    kor_geojson_2 = json.load(kor_input_2)
    kor_geojson_3 = json.load(kor_input_3)
    kor_df_1 = pd.json_normalize(kor_geojson_1)
    kor_df_2 = pd.json_normalize(kor_geojson_2)
    kor_df_3 = pd.json_normalize(kor_geojson_3)

    kor_eng_1 = (kor_df_1["영문 표기"]).to_frame()

    kor_eng_2 = kor_df_2["시군구_영어"].apply(pd.Series)
    kor_eng_2 = pd.DataFrame.to_numpy(kor_eng_2)
    kor_eng_2 = kor_eng_2.reshape(-1, )
    bool_array = np.apply_along_axis(lambda x: x == x, 0, kor_eng_2)
    kor_eng_2 = kor_eng_2[bool_array]
    get_kor2_eng = np.vectorize(lambda x: x['영문 표기'])
    kor_eng_2 = get_kor2_eng(kor_eng_2)
    kor_eng_2 = kor_eng_2.reshape(-1, 1)
    kor_eng_2 = pd.DataFrame(kor_eng_2, columns=["영문 표기"])

    kor_eng_3 = kor_df_3["읍면동_영어"].apply(pd.Series)
    kor_eng_3 = pd.DataFrame.to_numpy(kor_eng_3)
    kor_eng_3 = kor_eng_3.reshape(-1, )
    bool_array = np.apply_along_axis(lambda x: x == x, 0, kor_eng_3)
    kor_eng_3 = kor_eng_3[bool_array]
    get_kor3_eng = np.vectorize(lambda x: x['영문 표기'])
    kor_eng_3 = get_kor3_eng(kor_eng_3)
    kor_eng_3 = kor_eng_3.reshape(-1, 1)
    kor_eng_3 = pd.DataFrame(kor_eng_3, columns=["영문 표기"])

    # All kor geo name in english as (n,1) dataframe
    kor_eng_df = pd.concat([kor_eng_1, kor_eng_2, kor_eng_3])

    kor_eng_df.to_csv("../Data/only_eng.csv")
    return kor_eng_df


def save_to_parquet(cctrans_df, kor_df):
    m = cctrans_df.shape[0]
    n = kor_df.shape[0]
    cctrans_dup = pd.DataFrame(np.repeat(cctrans_df.values, n, axis=0))
    cctrans_dup.columns = cctrans_df.columns
    kor_dup = pd.concat([kor_df]*m)
    cctrans_dup.to_parquet(CC_DUP_BEFORE_PATH,
                           compression='gzip')

    kor_dup.to_parquet(KOR_DUP_PATH,
                       compression='gzip')
    return


def split_cctrans_by_ext_length(cctrans_df):
    idx_df = cctrans_df["cctrans.extent"].apply(lambda x: len(x))
    idx_df_1 = idx_df == 1
    idx_df_2 = idx_df == 2
    idx_df_3 = idx_df == 3

    cct1 = cctrans_df[idx_df_1]
    cct2 = cctrans_df[idx_df_2]
    cct3 = cctrans_df[idx_df_3]
    return cct1, cct2, cct3


def replace_string(q, before, after):
    return q.replace(before, after)


def exchange_extents_for_one(cct1, kor_df, n):
    m = cct1.shape[0]
    cct1_dup = pd.DataFrame(
        np.repeat(cct1.values, n, axis=0)
    )
    cct1_dup.columns = cct1.columns
    kor_dup = pd.concat([kor_df]*m, ignore_index=True)
    cct1_dup["cctrans.extent"] = cct1_dup["cctrans.extent"]\
        .apply(lambda x: x[0])
    cct1_dup["kor_eng"] = kor_dup
    cct1_dup["question"] = cct1_dup.apply(
        lambda x: replace_string(
            x["question"], x["cctrans.extent"], x["kor_eng"]),
        axis=1
    )
    cct1_dup["cctrans.extent"] = cct1_dup["kor_eng"]\
        .apply(lambda x: [item for item in x.split(" in ")])
    cct1_dup = cct1_dup.drop(columns=["kor_eng"])
    return cct1_dup


def replace_string_v2(q, before, after):
    if before[0] in q:
        return q.replace(before[0],after)
    elif before[1] in q:
        return q.replace(before[1], after)
    elif before[2] in q:
        return q.replace(before[2], ", ".join(after.split(" in ")))
    else:
        return q.replace(before[3], ", ".join(after.split(" in ")))


def exchange_extents_for_two(cct2, kor_df, n):
    m = cct2.shape[0]
    cct2_dup = pd.DataFrame(
        np.repeat(cct2.values, n, axis=0)
    )
    cct2_dup.columns = cct2.columns
    kor_dup = pd.concat([kor_df]*m, ignore_index=True)

    cct2_dup["cctrans.extent"] = cct2_dup["cctrans.extent"]\
        .apply(lambda x: [x[0] + " in " + x[1],
                          x[1] + " in " + x[0],
                          x[0] + ", " + x[1],
                          x[1] + ", " + x[0]])
    cct2_dup["kor_eng"] = kor_dup
    cct2_dup["question"] = cct2_dup.apply(
        lambda x: replace_string_v2(
            x["question"], x["cctrans.extent"], x["kor_eng"]
        ),
        axis=1
    )
    cct2_dup["cctrans.extent"] = cct2_dup["kor_eng"]\
        .apply(lambda x: [item for item in x.split(" in ")])
    cct2_dup = cct2_dup.drop(columns=["kor_eng"])
    return


if __name__ == "__main__":
    """
    about ipnut arguments
    """
    parser = argparse.ArgumentParser(description='Test your implementations.')
    parser.add_argument('function', nargs='?', type=str, default='all',
                        help='Name of the function you would like to test.')
    args = parser.parse_args()

    """
    main logic part
    """
    cctrans_df = get_cctrans_as_df()
    kor_df = get_korea_extents()
    n = kor_df.shape[0]
    if args.function == 'saveToParquet':
        save_to_parquet(cctrans_df, kor_df)
    cct1, cct2, cct3 = split_cctrans_by_ext_length(cctrans_df)
    cct1_dup = exchange_extents_for_one(cct1, kor_df, n)
    cct2_dup = exchange_extents_for_two(cct2, kor_df, n)

