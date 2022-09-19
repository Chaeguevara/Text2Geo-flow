import pandas as pd
import json
import numpy as np


def get_data_from_csv():
    df = pd.read_csv('../Data/korea_geo_name.csv', encoding="utf-8")
    df = df[df["시도"].notna()]
    return df


def handle_dup_siGunGu(geo_lv2):
    sigungu = geo_lv2[geo_lv2["소분류"].isna()]  # 시군구명 + 시도명
    sido = geo_lv2[geo_lv2.T.count() == 2]  # 시도
    sido_for_dict = sido.copy()  # 영어 시도명 딕셔너리
    # 인덱스 스왑
    sido_for_dict["orgidx"] = sido_for_dict.index
    sido_for_dict.index = sido_for_dict["시도"]
    sido_in_eng_dict = sido_for_dict.to_dict('index')
    sigungu_name_count = sigungu["시군구"].value_counts()  # 모든 시군구이름 중복갯수
    dup_sigungu_name = sigungu_name_count.\
        loc[sigungu_name_count != 1].index  # 중복 시군구 ['중구','동구',...]

    def dup_engname_to_nest(
            x, dup_sigungu_name, sido, sigungu, sido_in_eng_dict
    ):
        """
        Jung-gu -> Jung-gu in Seoul

        """
        if (x.name == "시군구"):
            dup_idx = x[x.isin(dup_sigungu_name)].index
            sido_eng_for_dup_sigungu = \
                sigungu.loc[dup_idx, "시도"].apply(
                    lambda x: sido_in_eng_dict[x]["영문 표기"]
                )
            sigungu.loc[dup_idx, "영문 표기"] = sigungu.loc[dup_idx, "영문 표기"]\
                + " in "\
                + sido_eng_for_dup_sigungu
            sigungu["지명 갯수"] = 1
            sigungu.loc[dup_idx, "지명 갯수"] = 2
            return sigungu

    sigungu[["시도", "시군구"]].apply(
        lambda x: dup_engname_to_nest(
            x,
            dup_sigungu_name,
            sido,
            sigungu,
            sido_in_eng_dict
        )
    )
    return sigungu


def write_geo_lv2(kor_geo_data):
    geo_lv2 = kor_geo_data.copy()
    nested_sigungu_df = handle_dup_siGunGu(geo_lv2)
    nested_sigungu_df = nested_sigungu_df.copy()
    geo_lv2 = nested_sigungu_df[nested_sigungu_df.T.count() == 5]
    geo_lv2.drop(columns=["읍면동", "소분류", "중분류"], inplace=True)
    print(geo_lv2)
    j_lv2 = geo_lv2.groupby(["시도"])\
        .apply(lambda x: x[["시군구", "영문 표기", "지명 갯수"]].to_dict('records'))\
        .reset_index()\
        .rename(columns={0: "시군구_영어"})\
        .to_json(orient="records")
    with open("../Data/lv2_korea_geo.json", "w") as outfile:
        outfile.write(
            json.dumps(json.loads(j_lv2),
                       indent=2,
                       sort_keys=False,
                       ensure_ascii=False)
        )
    return


def write_geo_lv1(kor_geo_data):
    geo_lv1 = kor_geo_data.copy()
    geo_lv1 = geo_lv1[geo_lv1.T.count() == 2]
    geo_lv1.drop(columns=["읍면동", "시군구"], inplace=True)
    geo_lv1_json = geo_lv1.to_json(orient="records")

    with open("lv1_korea_geo.json", "w") as outfile:
        outfile.write(
            json.dumps(
                json.loads(geo_lv1_json),
                indent=2,
                sort_keys=False,
                ensure_ascii=False
            )
            )


if __name__ == "__main__":
    kor_geo_data = get_data_from_csv()
    write_geo_lv2(kor_geo_data)

