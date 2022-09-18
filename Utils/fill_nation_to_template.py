import json

template_path = "../Data/Unique_template.json"
data_path = "../Data/Unique_extent_from_origin.json"
output_path = "../Data/nation_filled_data.json"

with open(template_path, "r") as template_data, \
     open(data_path, "r") as org_data:
    template_json = json.load(template_data)
    data_json = json.load(org_data)
    tmp_to_indx = dict()
    for i, item in enumerate(template_json):
        tmp_to_indx[list(item.keys())[0]] = i

    for item in data_json:
        ntl_key = list(item.keys())[0]
        ntl_name = list(item.values())[0]
        indx = tmp_to_indx[ntl_key]
        template_json[indx][ntl_key]["Nation"] = ntl_name
    print(template_json)
    result = json.dumps(template_json, indent=3)
    with open(output_path, "w") as f:
        f.write(result)
