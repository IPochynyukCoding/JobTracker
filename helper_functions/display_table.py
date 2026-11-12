import sqlite3
from rich.console import Console
from rich.table import Table
from helper_functions.input_validation import input_table_validation
def fetch_items(sql_cursor:sqlite3.Cursor,query:str,parameters=None):
    return sql_cursor.execute(query,parameters).fetchall() if parameters else sql_cursor.execute(query).fetchall()

def create_table(sql_cursor:sqlite3.Cursor,sql_connector:sqlite3.Connection):
    headers=["Job ID","Job Title","Employer","Job Site","Last Updated","Job Status""Interview Date"]
    search_query='''
    select job_id,job_title,employer.employer_name, job_site.site_name,last_updated_date, job_status.status_name,job.interview_date
    from job 
    left join employer on job.employer_id=employer.employer_id 
    left join job_site on job.site_id=job_site.site_id 
    left join job_status on job.job_status=job_status.job_status;'''
    sql_results:list[tuple]=fetch_items(sql_cursor,search_query)
    fetch_statuses=fetch_items(sql_cursor,"select status_name,hex_color from job_status")
    job_statuses=[]
    job_table=Table(title="Jobs")
    for status in fetch_statuses:
        job_statuses.append(status[0])
    for header in headers:
        job_table.add_column(header)
    for result in sql_results:
        job_status=result[3]
        job_table.add_row(*list(map(lambda x:str(x),result)),style=fetch_statuses[job_statuses.index(job_status)][1])
    console=Console()
    console.print(job_table,overflow="fold")
    input("Press any key to stop viewing ")


def display_application_history(sql_cursor:sqlite3.Cursor,sql_connector:sqlite3.Connection):
    fetch_jobs=fetch_items(sql_cursor,"select job_id,job_title,employer.employer_name,job_status.status_name,job_status.hex_color from job left join employer on job.employer_id=employer.employer_id left join job_status on job.job_status=job_status.job_status")
    fetch_statuses=fetch_items(sql_cursor,"select status_name,hex_color from job_status")
    console=Console(highlight=False)
    for index,job in enumerate(fetch_jobs):
        job_name=job[1]
        company=job[2]
        current_status=job[3]
        color=job[4]
        console.print(f"{index+1}. {job_name} from {company} with status '{current_status}'",style=color)

    selected_job=input_table_validation(fetch_jobs,"Select a job to view its application history or press 'q' to quit: ")
    headers=["Job Title","Employer","Update Date","Job Status","Interview Date"]
    search_query='''
    select job.job_title,employer.employer_name,job_history.update_time,job_status.status_name,job_history.interview_date
    from job_history
    join job on job_history.job_id=job.job_id
    join employer on job.employer_id=employer.employer_id
    join job_site on job.site_id=job_site.site_id
    join job_status on job.job_status=job_status.job_status
    where job.job_id=?;
    '''
    fetch_history=fetch_items(sql_cursor,search_query,[selected_job])
    job_statuses=[]
    job_table=Table(title=f"Application History for {fetch_history[0][0]} at {fetch_history[0][1]}")
    for status in fetch_statuses:
        job_statuses.append(status[0])
    for header in headers:
        job_table.add_column(header)
    for result in fetch_history:
        job_status=result[3]
        job_table.add_row(*list(map(lambda x:str(x),result)),style=fetch_statuses[job_statuses.index(job_status)][1])
    console=Console()
    console.print(job_table,overflow="fold")
    input("Press any key to stop viewing ")
