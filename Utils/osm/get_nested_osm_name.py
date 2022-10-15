import pandas as pd
import xml.etree.ElementTree as ET
import argparse
from urllib.request import urlopen


BASE_URL = "https://www.openstreetmap.org/api/0.6/relation/"


def get_seoul_xml_from_osm(rel_id):
    seoul_url = BASE_URL + str(rel_id)
    seoul_xml = urlopen(seoul_url)
    seoul_xml = ET.parse(seoul_xml)
    root = seoul_xml.getroot()
    seoul_pd = pd.DataFrame(
      columns=["root1_en", "root1_id",
               "root2_en", "root2_id",
               "root3_en", "root3_id"]
    )
    relation_root = root[0]
    root2_ids = []
    root1_en = ''
    for child in relation_root:
        try:
            if (child.attrib["role"] == 'subarea'):
                root2_ids.append(child.attrib['ref'])
        except KeyError:
            pass
        try:
            if (child.attrib['k'] == 'name:en'):
                root1_en = child.attrib['v']
        except KeyError:
            continue
    seoul_pd["root2_id"] = root2_ids
    seoul_pd["root1_en"] = root1_en
    seoul_pd["root1_id"] = seoul_rel_id
    return seoul_pd


def get_gu_info(seoul_lv1):
    # loop
    for i in range(seoul_lv1.shape[0]):
        single_row = seoul_lv1.iloc[i, :]
        name = get_single_gu_info(single_row)
        seoul_lv1.iloc[i, :] = name
    print(f"Upto gu filled: \n {seoul_lv1}")
    return seoul_lv1


def get_single_gu_info(single_lv_2):
    lv_2_id = single_lv_2["root2_id"]
    lv2_url = BASE_URL + str(lv_2_id)
    lv2_xml = urlopen(lv2_url)
    lv2_xml = ET.parse(lv2_xml)
    root = lv2_xml.getroot()
    root = root[0]
    root3_ids = []
    for child in root:
        try:
            if (child.attrib["role"] == 'subarea'):
                root3_ids.append(child.attrib['ref'])
        except KeyError:
            pass
        try:
            if (child.attrib['k'] == 'name:en'):
                single_lv_2["root2_en"] = child.attrib['v']
        except KeyError:
            continue
    single_lv_2["root3_id"] = root3_ids
    return single_lv_2


def get_dong_info(seoul_lv2):
    lv3 = seoul_lv2["root3_id"].apply(lambda x: pd.Series(x))\
        .stack()\
        .reset_index(level=1, drop=True)\
        .to_frame("root3_id")\
        .join(seoul_lv2[["root2_id"]], how="left")
    seoul_lv2 = seoul_lv2.copy()
    seoul_lv2 = seoul_lv2.drop(columns=["root3_id"])
    seoul_lv3 = seoul_lv2.merge(lv3, how="right", on="root2_id")
    print(f"Dong exploded: \n {seoul_lv3}")
    for i in range(seoul_lv3.shape[0]):
        seoul_lv3.iloc[i, :] = \
            change_dong_single_info(seoul_lv3.iloc[i, :])
    print(f"final processed data : \n{seoul_lv3}")

    return seoul_lv3


def change_dong_single_info(single_lv_3):
    lv_3_id = single_lv_3["root3_id"]
    lv3_url = BASE_URL + str(lv_3_id)
    lv3_xml = urlopen(lv3_url)
    lv3_xml = ET.parse(lv3_xml)
    root = lv3_xml.getroot()
    root = root[0]
    for child in root:
        try:
            if (child.attrib['k'] == 'name:en'):
                single_lv_3["root3_en"] = child.attrib['v']
        except KeyError:
            continue
    print(f"single_dong_filled: \n {single_lv_3}")
    return single_lv_3


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test your implementations.')
    parser.add_argument('function', nargs='?', type=str, default='fromLocal',
                        help='Name of the function you would like to test.')
    args = parser.parse_args()
    if args.function == "getFromWeb":
        seoul_rel_id = 2297418
        seoul_lv1 = get_seoul_xml_from_osm(seoul_rel_id)
        print("lv1 processed")
        seoul_lv2 = get_gu_info(seoul_lv1)
        print("lv2 processed")
        seoul_lv3 = get_dong_info(seoul_lv2)
        print("now save to csv")
        seoul_lv3.to_csv("../../Data/osm_seoul_table.csv")
    elif args.function == "fromLocal":
        to_be_nested = pd.read_csv("../../Data/osm_seoul_table.csv")
        print(to_be_nested)
        to_be_nested = to_be_nested.iloc[:, 1:]
        to_be_nested["nested_name"] = to_be_nested.apply(
            lambda x:
            x["root3_en"] + " , " +
            x["root2_en"] + " , " +
            x["root1_en"] + " , " +
            "Korea",
            axis=1
        )
        to_be_nested.to_csv("../../Data/osm_seoul_table_nested_english.csv")
