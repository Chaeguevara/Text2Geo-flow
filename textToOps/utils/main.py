from hashlib import new
from parrot import Parrot
import torch
import warnings
import pandas as pd
import numpy as np
from collections import defaultdict
import json
warnings.filterwarnings("ignore")

EXCEL_PATH = "../data/DataCorpus_classfied_중분류_1차 연구.xlsx"
ENG_NAME_PATH = "../data/only_eng_sido_sigungu.csv"


def random_state(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available:
        torch.cuda.manual_seed_all(seed)


def run_paraphrase(phrases,ids, parrot):
    d = defaultdict(list)
    phrases = list(phrases["Question"])
    print(f"phrases:{phrases}")
    print(f"ids:{ids}")
    i = 0
    for phrase,op in zip(phrases,ids):
        print(f"{i} th out of {len(phrases)}")
        print(phrase)
        d[op].append(phrase)
        para_phrases = parrot.augment(input_phrase=phrase, use_gpu=True)
        if para_phrases is None:
            continue
        for para_phrase in para_phrases:
            d[op].append(para_phrase[0])
    df = pd.DataFrame.from_dict(d,orient='index')
    df.to_excel("../data/paraphrased.xlsx")
    #df.to_parquet("../data/paraphrased.gzip",
    #              compression='gzip')
    return df


def get_excel():
    df = pd.read_excel(EXCEL_PATH)
    return df


def substitue_place(df):
    eng = pd.read_csv(ENG_NAME_PATH)
    eng = eng["영문 표기"]
    eng = eng.apply(lambda x: str(x)+" ")
    eng_sample = eng.sample(frac=0.25, replace=True, random_state=1)
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
    print(types_count)
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
    df= get_excel()
    df = add_type_column(df)
    word_sub_df = substitue_place(df)
    test_df = word_sub_df.groupby('op_id',
                                  group_keys=False).apply(
                                      lambda x: x.sample(frac=1)
                                  )
    test_df = test_df.groupby('op_id',
                                  group_keys=False).apply(
                                      lambda x: x.sample(50)
                                  )
    test_df.to_excel("./substitute_extent.xlsx")
    print(test_df)
    random_state(1234)
    parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")
    run_paraphrase(test_df,
                   test_df['op_id'].to_list(),
                   parrot
                   )
