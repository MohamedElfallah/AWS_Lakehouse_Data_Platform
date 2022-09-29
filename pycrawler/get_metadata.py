import sqlalchemy
import pymysql

engine = sqlalchemy.create_engine("mysql+pymysql://postgres:mytestdb@15.237.13.14:3306/db2")
store = []
with engine.connect() as con :
    schema = con.execute("select table_name from information_schema.tables where table_schema = 'db2';")
    tables = schema.all()
    tables = [x[0] for x in tables]
    for table in tables : 
        result_set = con.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'db2' AND TABLE_NAME = '{table}';")
        meta_data = {
            "location" : "",
            "columns" : []
        }
        for row in result_set :
            meta_data["location"] = row[0]+"."+row[1]+"."+row[2] 
            meta_data["columns"].append({"name" : row[3], "type" : row[7]})
        store.append(meta_data)
refined_store = str(store).replace("'",'"')
with open(f"../infrastructure/custom_crawlers/db.tfvars", "w") as file :
    file.write(f'database = "db2_source" \ntables = {refined_store}')   