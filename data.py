import json
from pprint import pprint
new={}
def inp(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        return data

def parser(d):
    new["restaurant_id"]=d["page_data"]["sections"]["SECTION_BASIC_INFO"]["res_id"]

    new["restaurant_name"] = d["page_data"]["sections"]["SECTION_BASIC_INFO"]["name"]

    new["restaurant_url"] = d["page_data"]["sections"]["SECTION_BASIC_INFO"]["resUrl"]

    new["restaurant_contact"]=[d["page_data"]["sections"]["SECTION_RES_CONTACT"]["phoneDetails"]["phoneStr"]]

    new["fssai_licence_number"]=d["page_data"]["order"]["menuList"]["fssaiInfo"]["text"].split()[2]

    new["address_info"]={}
    new["address_info"]["full_address"]=d["page_data"]["sections"]["SECTION_RES_CONTACT"]["address"]
    new["address_info"]["city"]=d["page_data"]["sections"]["SECTION_RES_CONTACT"]["city_name"]
    new["address_info"]["pincode"] = d["page_data"]["sections"]["SECTION_RES_CONTACT"]["zipcode"]
    try:
        new["address_info"]["region"] = d["page_data"]["sections"]["SECTION_RES_CONTACT"]["region"]
    except KeyError:
        new["address_info"]["region"]="None"
    try:
        new["address_info"]["state"] = d["page_data"]["sections"]["SECTION_RES_CONTACT"]["state"]
    except KeyError:
        new["address_info"]["state"] = "None"


    new["cuisines"]=[]
    for i in range(len(d["page_data"]["sections"]["SECTION_RES_HEADER_DETAILS"]["CUISINES"])):
        new["cuisines"].append({"name":d["page_data"]["sections"]["SECTION_RES_HEADER_DETAILS"]["CUISINES"][i]["name"],"url":d["page_data"]["sections"]["SECTION_RES_HEADER_DETAILS"]["CUISINES"][i]["url"]})


    new["timings"]={"monday":{"open":d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[0],"close":d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"]["opening_hours"][0]["timing"].split()[2]},
                    "Tuesday": {"open":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[0], "close":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[2]},
                    "wednesday": {"open":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[0], "close":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[2]},
                    "Thursday": {"open":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[0], "close":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[2]},
                    "friday": {"open":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[0], "close":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[2]},
                    "saturday": {"open":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[0], "close":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[2]},
                    "sunday": {"open":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[0], "close":
                                    d["page_data"]["sections"]["SECTION_BASIC_INFO"]["timing"]["customised_timings"][
                                        "opening_hours"][0]["timing"].split()[2]}
                    }


    new["menu_categories"]=[]

    for i in range(len(d["page_data"]["order"]["menuList"]["menus"])):
        for j in range(len(d["page_data"]["order"]["menuList"]["menus"][i]["menu"]["categories"])):
            categories_name=d["page_data"]["order"]["menuList"]["menus"][i]["menu"]["categories"][j]["category"]["name"]
            for k in range(len(d["page_data"]["order"]["menuList"]["menus"][i]["menu"]["categories"][j]["category"]["items"])):
                category_entry = {
                    "category_name": categories_name,
                    "items": []
                }
                items=d["page_data"]["order"]["menuList"]["menus"][i]["menu"]["categories"][j]["category"]["items"][k]["item"]

                item_data={
                    "item_id": items.get("id"),
                    "item_name": items.get("name"),
                    "item_slug":items.get("tag_slugs"),
                    "item_description": items.get("desc"),
                    "is_veg": items.get("")
                }

                category_entry["items"].append(item_data)
            new["menu_categories"].append(category_entry)
    return new

def convert_to_json(processed_data):
    with open("ZOMATO_16-02-2026.json","w") as f:
        json.dump(processed_data,f,indent=4)



file=input("enter file name: ")
d=inp(file)
extracted=parser(d)
convert_to_json(extracted)
