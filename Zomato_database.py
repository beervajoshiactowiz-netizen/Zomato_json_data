import json
import mysql.connector

input_file="ZOMATO_2026-02-24.json"
def load_validated_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
    return data

extracted = load_validated_json(input_file)

#Mysql Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="flight_db"
)
cursor = conn.cursor()

#Restaurant table
create_res_query = """
        CREATE TABLE IF NOT EXISTS zomato_Restaurant(
        RestaurantId int,
        RestaurantName varchar(20),
        RestaurantUrl varchar(500),
        FssaiNo JSON,
        Address TEXT,
        City TEXT,
        Pincode JSON,
        Cuisine JSON,
        Timing JSON

      );
"""
cursor.execute(create_res_query)

res = []
res.append((
    extracted["restaurant_id"],
    extracted["restaurant_name"],
    extracted["restaurant_url"],
    json.dumps(extracted["fssai_licence_number"]),
    extracted["address_info"]["full_address"],
    extracted["address_info"]["city"],
    extracted["address_info"]["pincode"],
    json.dumps(extracted["cuisines"]),
    json.dumps(extracted["timings"]),
))
#insert values
insert_res_query = """
        insert into zomato_Restaurant(
            RestaurantId, RestaurantName,RestaurantUrl,FssaiNo,Address,City,Pincode,Cuisine,Timing 
        )VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
cursor.executemany(insert_res_query, res)

#Menu Table
create_menu_query = """
        CREATE TABLE IF NOT EXISTS zomato_menu(
        SrNo int auto_increment primary key,
        ItemId VARCHAR(100) ,
        RestaurantName varchar(20) ,
        ItemName VARCHAR(50),
        Category varchar(50),
        Description varchar(100),
        IsVeg boolean,
        ItemSlug text
    );
"""
cursor.execute(create_menu_query)
res_name=extracted["restaurant_name"]
row = []
dtaa = extracted["menu_categories"]
for category in dtaa:
    name = category["category_name"]
    for item in category["items"]:
        row.append((
            item["item_id"],
            res_name,
            item["item_name"],
            name,
            item.get("item_description"),
            item.get("is_veg"),
            ",".join(item.get("item_slug", []))
        ))
#insert values
insert_query = """
        insert into zomato_menu(
            ItemId,restaurantName,ItemName,Category,Description,IsVeg,ItemSlug
        )VALUES(%s,%s,%s,%s,%s,%s,%s)
"""
cursor.executemany(insert_query, row)
conn.commit()