from hashlib import new
from parrot import Parrot
import torch
import warnings
import pandas as pd
import numpy as np
from collections import defaultdict
warnings.filterwarnings("ignore")

EXCEL_PATH = "../data/DataCorpus_classfied_중분류_1차 연구.xlsx"
ENG_NAME_PATH = "../data/only_eng.csv"


def random_state(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available:
        torch.cuda.manual_seed_all(seed)


def run_paraphrase(phrases, parrot):
    d = defaultdict(list)
    phrases = list(phrases["Question"])
    for phrase in phrases:
        print("-"*100)
        print("Input_phrase: ", phrase)
        print("-"*100)
        para_phrases = parrot.augment(input_phrase=phrase, use_gpu=False)
        for para_phrase in para_phrases:
            try:
                print(para_phrase[0])
            except TypeError:
                pass


def get_excel():
    df = pd.read_excel(EXCEL_PATH)
    return df


def substitue_place(df):
    eng = pd.read_csv(ENG_NAME_PATH)
    eng = eng["영문 표기"]
    eng_sample = eng.sample(frac=0.05, replace=True, random_state=1)
    new_df = df[df["extents"].apply(lambda x:len(x.split(','))==1)]
    m = eng_sample.shape[0]
    n = new_df.shape[0]
    new_df = pd.DataFrame(
        np.repeat(new_df.values, m, axis=0),
        columns = new_df.columns
    )
    eng_sample = pd.concat([eng_sample]*n, ignore_index=True).to_frame()
    print(new_df.head)
    print(eng_sample.tail)
    new_df["영문 표기"] = eng_sample["영문 표기"]
    changed_question = new_df.apply(
        lambda x: x["Question"].replace(x["extents"], x["영문 표기"]), axis=1
                                    )
    new_df["Question"] = changed_question
    return new_df



if __name__ == '__main__':

    df= get_excel()
    word_sub_df = substitue_place(df)
    test_df = df.sample(frac=0.1)
    print(test_df)
    # random_state(1234)
    parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")
    run_paraphrase(test_df, parrot)
