import sqlite3
from rich.console import Console
from rich.table import Table

def fetch_items(sql_cursor:sqlite3.Cursor,query:str):
    return sql_cursor.execute(query).fetchall()

def create_table(sql_cursor:sqlite3.Cursor,sql_connector:sqlite3.Connection):
    headers=["Job ID","Job Title","Last Updated","Job Status","Employer","Job Site","Interview Date"]
    search_query='''select job_id,job_title,last_updated_date, job_status.status_name, employer.employer_name, job_site.site_name,job.interview_date
    from job left join employer on job.employer_id=employer.employer_id left join job_site on job.site_id=job_site.site_id left join job_status on job.job_status=job_status.job_status;'''
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



