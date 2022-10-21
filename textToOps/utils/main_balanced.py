from parrot import Parrot
import torch
import warnings
import pandas as pd
import numpy as np
from collections import defaultdict
import json
warnings.filterwarnings("ignore")


# each class has at least > 1
EXCEL_PATH = "../data/processed/corpora_unique_ops_dropped.xlsx"
ENG_NAME_PATH = "../data/only_eng_sido_sigungu.csv"


def random_state(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available:
        torch.cuda.manual_seed_all(seed)


def run_paraphrase(phrases, parrot):
    new_df = phrases.copy()
    i = 0
    for row_dict in train_df.to_dict(orient="records"):
        i += 1
        new_df = new_df.append(row_dict, ignore_index=True)
        print(f"{i} th out of {len(train_df.to_dict(orient='records'))}")
        print(row_dict["Question"])
        para_phrases = parrot.augment(input_phrase=row_dict["Question"],
                                      use_gpu=True,
                                      do_diverse=True,
                                      max_length=60,
                                      adequacy_threshold=0.95
                                      )
        if para_phrases is None:
            continue
        for para_phrase in para_phrases:
            new_row = row_dict.copy()
            print(para_phrase[0])
            new_row['Question'] = para_phrase[0]
            new_df = new_df.append(new_row, ignore_index=True)
    new_df["Question"] = new_df['Question'].str.lower()
    new_df = new_df.drop_duplicates(subset=["Question"])


    new_df.to_excel("../data/processed/paraphrased_train.xlsx")
    #df.to_parquet("../data/paraphrased.gzip",
    #              compression='gzip')
    return df


def get_excel():
    df = pd.read_excel(EXCEL_PATH)
    return df


def substitue_place(df, frac_of_extents=0.01):
    eng = pd.read_csv(ENG_NAME_PATH)
    eng = eng["영문 표기"]
    eng = eng.apply(lambda x: str(x)+" ")
    eng_sample = eng.sample(frac=frac_of_extents, replace=True, random_state=1)
    new_df = df[df["extents"].apply(lambda x:len(x.split(','))==1)]
    m = eng_sample.shape[0]
    n = new_df.shape[0]
    new_df = pd.DataFrame(
        np.repeat(new_df.values, m, axis=0),
        columns = new_df.columns
    )
    eng_sample = pd.concat([eng_sample]*n, ignore_index=True).to_frame()
    new_df["영문 표기"] = eng_sample["영문 표기"]
    changed_question = new_df.apply(
        lambda x: x["Question"].replace(x["extents"], x["영문 표기"]), axis=1
                                    )
    new_df["Question"] = changed_question
    new_df.to_excel("../data/extent_substitute.xlsx")
    types_count = new_df['op_id'].value_counts()
    return new_df

def add_type_column(df):
    ops = df.iloc[:, 5:]
    print(f"ops : {ops}")
    op_type = ops[ops.columns[1:]].apply(
        lambda x: ','.join(x.dropna().astype(str)),
        axis=1
    )
    op_type=op_type.str.lower()
    df["op_type"] = op_type
    op_type = pd.DataFrame(op_type.unique(), columns=["op_type"])
    op_type["op_id"] = op_type.index
    op_type.to_excel("../data/op_type.xlsx")
    df = df.merge(op_type, how='left', on="op_type")
    df.to_excel("./text.xlsx")
    return df


if __name__ == '__main__':
    df = get_excel()
    # Stratified sampling
    train_df = df.groupby('op_id', group_keys=False).apply(
        lambda x: x.sample(frac=0.7,
                           random_state=124
                           )
    )
    test_df = df[~df.index.isin(train_df.index)]
    # 여기에서 Train / Test로 나눠야??
    test_df["for train"] = False
    print(test_df.shape)
    train_df.to_excel("../data/processed/stratified_train.xlsx")
    test_df.to_excel("../data/processed/stratified_test.xlsx")
    print(train_df.shape)
    random_state(23341)
    parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")
    train_df = run_paraphrase(train_df,
                              parrot
                              )
    train_df["for train"] = True
    print(train_df.shape)
    tr_te_df = pd.concat([train_df, test_df],
                         axis=0)
    print(tr_te_df.shape)
    tr_te_df.to_excel("../data/processed/train_test_only_paraphrased.xlsx")

