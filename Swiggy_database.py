import json
import mysql.connector

input_file="Swiggy_2026-02-18.json"

def load_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        return data

extracted=load_file(input_file)

conn= mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="flight_db"
)
cursor=conn.cursor()

#create table
create_query="""
        CREATE TABLE IF NOT EXISTS Swiggy_items(
        Name varchar(255),
        ProductId varchar(10),
        Price float,
        Quantity varchar(20),
        ImageUrl JSON,
        Discount int,
        Mrp float,
        InStock boolean
        );
"""
cursor.execute(create_query)

#insert query
insert_query = """
INSERT INTO Swiggy_items(
    Name, ProductId, Price, Quantity, ImageUrl, Discount, Mrp, InStock
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# Insert data
for f in extracted:
    cursor.execute(insert_query, (
        f.get("name"),
        f.get("Prod_id"),
        f.get("Prod_price"),
        f.get("Prod_quantity"),           # keep as string
        json.dumps(f.get("Image_URL")),   # convert list to JSON
        f.get("Discount_per"),
        f.get("mrp"),
        f.get("In_stock")
    ))

conn.commit()