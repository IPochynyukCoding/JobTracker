import sqlite3
import datetime
import csv
import os
from helper_functions.display_table import fetch_items
def export_table(sql_cursor:sqlite3.Cursor,sql_connection:sqlite3.Connection):
    headers=["Job ID","Job Title","Last Updated","Job Status","Employer","Job Site","Interview Date"]
    search_query='''select job_id,job_title,last_updated_date, job_status.status_name, employer.employer_name, job_site.site_name,job.interview_date
    from job left join employer on job.employer_id=employer.employer_id left join job_site on job.site_id=job_site.site_id left join job_status on job.job_status=job_status.job_status;'''
    job_results=fetch_items(sql_cursor,search_query)
    current_directory=os.getcwd()
    planned_path=os.path.normpath(current_directory+"\\exported_reports")
    if not os.path.isdir(planned_path):
        os.mkdir(planned_path)
    current_date=datetime.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    file_name=f"job_export_{current_date}.csv"
    with open(f"./exported_reports/{file_name}","w",newline="") as exported_file:
        exported_csv=csv.writer(exported_file,delimiter=";",skipinitialspace=True,quoting=csv.QUOTE_MINIMAL)
        exported_csv.writerow(headers)
        exported_csv.writerows(job_results)
    input(f"Successfully added {file_name} to {planned_path}, press any key to go back to main interface ")