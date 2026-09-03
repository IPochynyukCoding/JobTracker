import sqlite3

def initial_insert_operation(pulled_data:list[tuple],data:dict[str,str],query:str,cursor:sqlite3.Cursor,connection:sqlite3.Connection):
    if len(pulled_data)==0:
        for part in data:
            cursor.execute(query,[part,data[part]])
            connection.commit()

def database_creation():
    tables={"employer":{"columns":["employer_id","employer_name"],"types":["INTEGER PRIMARY KEY AUTOINCREMENT","TEXT"]},
            "job_site":{"columns":["site_id","site_name","site_base_url"],"types":["INTEGER PRIMARY KEY AUTOINCREMENT","TEXT","TEXT"]},
            "job_status":{"columns":["job_status","status_name","hex_color"],"types":["INTEGER PRIMARY KEY AUTOINCREMENT","TEXT",'VARCHAR(7) CHECK(length("hex_color") == 7)']},
            "job":{"columns":["job_id","job_title","last_updated_date","job_status","employer_id","site_id","interview_date"],"types":["INTEGER PRIMARY KEY AUTOINCREMENT","TEXT","DATE DEFAULT CURRENT_TIMESTAMP","INTEGER","INTEGER","INTEGER","DATETIME DEFAULT NULL"]}
            }
    foreign_keys={"employer":"employer_id","job_site":"site_id","job_status":"job_status"}
    job_sites={"LinkedIn":"https://linkedin.com","Indeed":"https://indeed.com","ZipRecruiter":"https://ziprecruiter.com"}
    job_statuses={"Pending":"#ffffff","Ghosted":"#6b6b69","Accepted":"#16c60c","Rejected":"#e74856","Pending Interview":"#e0eb1e","Pending Resume":"#FFAC1C"}
    job_connection=sqlite3.connect("jobs.db")
    job_cursor=job_connection.cursor()
    for table in tables:
        query_body=""
        current=tables[table]
        for index,column in enumerate(current["columns"]):
            query_body+= f"{column} {current["types"][index]}," if index!=len(current["columns"])-1 else f"{column} {current["types"][index]}"
        if table=="job":
            for foreign_key in foreign_keys:
                query_body+=f", FOREIGN KEY ({foreign_keys[foreign_key]}) REFERENCES {foreign_key}({foreign_keys[foreign_key]})"
        job_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({query_body})")
        job_connection.commit()
    job_site_result=job_cursor.execute("SELECT * FROM job_site").fetchall()
    job_status_result=job_cursor.execute("SELECT * FROM job_status").fetchall()
    initial_insert_operation(job_site_result,job_sites,"INSERT INTO job_site(site_name,site_base_url) VALUES(?,?);",job_cursor,job_connection)
    initial_insert_operation(job_status_result,job_statuses,"INSERT INTO job_status(status_name,hex_color) VALUES(?,?);",job_cursor,job_connection)
    job_connection.close()



