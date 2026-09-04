import platform
import sqlite3
import subprocess
import os
from helper_functions.display_table import create_table
from helper_functions.job_functions import add_job,modify_job,input_validation
from helper_functions.create_database import database_creation
from helper_functions.export_table import export_table
is_windows= True if platform.system()=="Windows" else False
clear_command = "cls" if is_windows else "clear"


if __name__ == "__main__":
    if not os.path.exists("jobs.db"):
        print("Jobs database not found, creating database...")
        database_creation()
    job_connector=sqlite3.connect("jobs.db")
    job_cursor=job_connector.cursor()
    functions={"display":{"function":create_table,"label":"display table"},"add":{"function":add_job,"label":"add job"},"modify":{"function":modify_job,"label":"update job status"},"export":{"function":export_table,"label":"export table to CSV file"}}
    function_keys=list(functions.keys())
    while True:
        input_message="Press "
        for index,function_name in enumerate(function_keys):
            input_message+=f"{index+1} to {functions[function_name]["label"]}, "
        input_message+="or 'q' to quit: "
        print("""                                                                     
             ▄▄▄▄▄▄          ▄▄▄▄▄▄▄                                   
             █▀ ██       █▄█▀▀ ██▀▀▀▀                                  
                ██       ██    ██   ▄                ▄▄           ▄    
                ██ ▄███▄ ████▄ ██   ████▄▄▀▀█▄ ▄███▀ ██ ▄█▀ ▄█▀█▄ ████▄
                ██ ██ ██ ██ ██ ██   ██   ▄█▀██ ██    ████   ██▄█▀ ██   
                ██▄▀███▀▄████▀ ▀██▄▄█▀   ▀█▄██▄▀███▄▄██ ▀█▄▄▀█▄▄▄▄█▀   
            ▄   ██                                                     
            ▀████▀                                                     
""")
        selection=input_validation(input_message)
        try:
            numbered_selection=int(selection)-1
            functions[function_keys[numbered_selection]]["function"](job_cursor,job_connector)
            clearing=subprocess.run([clear_command],check=True,shell=True)
            try:
                clearing.check_returncode()
            except subprocess.CalledProcessError:
                print("Unable to successfully clear")
                quit()
        except(ValueError,IndexError):
            print("Invalid function selection, please try again!")

