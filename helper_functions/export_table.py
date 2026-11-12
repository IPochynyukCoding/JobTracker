import sqlite3
import datetime
import csv
import os
import subprocess
from helper_functions.input_validation import input_table_validation
from helper_functions.display_table import fetch_items

def resolve_path(subdirectory:str):
    current_directory=os.getcwd()
    planned_path=os.path.normpath(current_directory+subdirectory)
    if not os.path.isdir(planned_path):
        os.mkdir(planned_path)
    return planned_path



def select_export(sql_cursor:sqlite3.Cursor,sql_connection:sqlite3.Connection):
    export_options=[
        {"headers":["Job ID","Job Title","Employer","Job Site","URL","Last Updated","Job Status","Interview Date"],
         "query":
         '''
        select job_id,job_title,employer.employer_name, job_site.site_name,job.job_listing_url,last_updated_date, job_status.status_name,job.interview_date
        from job 
        left join employer on job.employer_id=employer.employer_id 
        left join job_site on job.site_id=job_site.site_id 
        left join job_status on job.job_status=job_status.job_status;
        ''',
        "directory_name":"job_listings",
        "file_name":"job_listings",
        "label":"Current status for all Jobs"
        },
        {"headers":["Job ID","Job Title","Employer","Update Time","Status"],
         "query":
         '''
        select job_history.job_id,job.job_title,employer.employer_name,job.job_listing_url,job_history.update_time,job_status.status_name
        from job_history
        left join job on job_history.job_id=job.job_id
        left join job_status on job_history.job_status=job_status.job_status
        left join employer on job.employer_id=employer.employer_id;
        ''',
        "directory_name":"job_history",
        "file_name":"job_history_chronological",
        "label":"Job History ordered chronologically"
        },
        {"headers":["Job ID","Job Title","Employer","Update Time","Status"],
         "query":
         '''
        select job_history.job_id,job.job_title,employer.employer_name,job_history.update_time,job_status.status_name
        from job_history
        left join job on job_history.job_id=job.job_id
        left join job_status on job_history.job_status=job_status.job_status
        left join employer on job.employer_id=employer.employer_id
        order by job.job_id,job_history.update_time;
        ;
        ''',
        "directory_name":"job_history",
        "file_name":"job_history",
        "label":"Job History ordered by Job ID"
        }
    ]
    while True:
        for index,export in enumerate(export_options):
            print(f"{index+1}. {export['label']}")
        selection=input_table_validation(export_options,"Select which export you want to implement or press 'q' to quit: ")
        try:
            selected=export_options[selection-1]
            export_table(sql_cursor,selected['headers'],selected['query'],selected['directory_name'],selected['file_name'])
            break
        except(IndexError,TypeError):
            print(f"Invalid input: {selection}")


def export_table(sql_cursor:sqlite3.Cursor,headers:list[str],search_query:str,directory_name:str,file_export_name:str):
    job_results=fetch_items(sql_cursor,search_query)
    planned_path=resolve_path(f"\\exported_reports\\{directory_name}")
    current_date=datetime.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    file_name=f"{file_export_name}_{current_date}.csv"
    with open(f"./exported_reports/{directory_name}/{file_name}","w",newline="") as exported_file:
        exported_csv=csv.writer(exported_file,delimiter=";",skipinitialspace=True,quoting=csv.QUOTE_MINIMAL)
        exported_csv.writerow(headers)
        exported_csv.writerows(job_results)
    if os.name=="nt":
        os.startfile(planned_path)
    else:
        subprocess.run(["open",planned_path])
    input(f"Successfully added {file_name} to {planned_path}, press any key to go back to main interface ")