from operator import index
import pandas as pd
from collections import defaultdict
import json

df = pd.read_csv('./korea_geo_name.csv',encoding="utf-8")
df.drop(columns=["중분류","소분류"],axis=1,inplace=True)


# geo_lv3 = df.copy()
# sub_df = geo_lv3.dropna(inplace=True)
# j_lv3 = geo_lv3.groupby(["시도","시군구"]) \
#         .apply(lambda x:x[["읍면동", "영문 표기"]].to_dict('records')) \
#             .reset_index()\
#                 .rename(columns={0:"읍면동_영어"})\
#                     .to_json(orient='records')

# with open ("lv3_korea_geo.json","w") as outfile:
#     outfile.write(json.dumps(json.loads(j_lv3),indent=2,sort_keys=True,ensure_ascii=False))


geo_lv2 = df.copy()
geo_lv2 = geo_lv2[geo_lv2.T.count()==3]
geo_lv2.drop(columns=["읍면동"],inplace=True)
j_lv2 = geo_lv2.groupby(["시도"])\
    .apply(lambda x:x[["시군구","영문 표기"]].to_dict('records'))\
        .reset_index()\
            .rename(columns={0:"시군구_영어"})\
                .to_json(orient="records")
with open ("lv2_korea_geo.json","w") as outfile:
    outfile.write(json.dumps(json.loads(j_lv2),indent=2,sort_keys=False,ensure_ascii=False))

geo_lv1 = df.copy()
geo_lv1 = geo_lv1[geo_lv1.T.count()==2]
geo_lv1.drop(columns=["읍면동","시군구"],inplace=True)
geo_lv1_json = geo_lv1.to_json(orient="records")

with open ("lv1_korea_geo.json","w") as outfile:
    outfile.write(json.dumps(json.loads(geo_lv1_json),indent=2,sort_keys=False,ensure_ascii=False))