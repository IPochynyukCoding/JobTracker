import sqlite3
import datetime
from helper_functions.display_table import fetch_items
from rich.console import Console

pending=1
pending_submission=6

def input_validation(message:str):
    output=input(message)
    if output.lower()=="q":
        quit()
    return output

def input_table_validation(query_results:list[tuple],input_message:str):
    valid_selection=False
    while not valid_selection:
        selection=input(input_message)
        try:
            if selection.lower()=="q":
                quit()
            selected_result=query_results[int(selection)-1]
            return int(selection)
        except(ValueError,IndexError):
            print("Invalid selection, please try again!")
            continue

def input_date_validation(format:str,input_message:str,example:str):
    is_valid=False
    print(example)
    while not is_valid:
        date=input(input_message)
        try:
            date_conversion=datetime.datetime.strptime(date,format)
            return date_conversion.strftime(format)
        except ValueError:
            print(f"Invalid time format {date}, it must match {format}")


def job_log(db_cursor:sqlite3.Cursor,db_connection:sqlite3.Connection,job_id=None):
    query="select job_id,last_updated_date,job_status from job order by job_id desc limit 1" if job_id==None else f"select job_id,last_updated_date,job_status from job where job_id={job_id}"
    parameters=fetch_items(db_cursor,query)[0]
    db_cursor.execute("insert into job_history(job_id,update_time,job_status) values(?,?,?)",parameters)



def add_job(db_cursor:sqlite3.Cursor,db_connection:sqlite3.Connection):
    is_new_site=True
    is_valid_site=False
    fetch_sites=fetch_items(db_cursor,"select site_id,site_base_url from job_site")
    while not is_valid_site:
        current_url=input_validation("Insert a URL for the job or press 'q' to quit: ")
        if not current_url.startswith("https://"):
            print("All sites must start with https:// to be valid")
            continue
        else:
            is_valid_site=True
    for site in fetch_sites:
        if site[1] in current_url:
            is_new_site=False
            job_site_id=site[0]

    if is_new_site:
        print(f"Unrecognized site detected, attempting to add to database...")
        base_url=current_url.removeprefix("https://")
        base_url=base_url[0:base_url.index("/")+1]
        base_url="https://"+base_url
        base_name=input_validation("Insert the site's name for the database or press 'q' to quit: ")
        db_cursor.execute("insert into job_site(site_name,site_base_url) values(?,?)",[base_name,base_url])
        db_connection.commit()
        job_site_id:int=db_cursor.execute("select site_id from job_site where site_base_url=?",[base_url]).fetchone()[0]
    job_title=input_validation("Insert the job title or press 'q' to quit: ")
    employer=input_validation("Insert the employer for the job or press 'q' to quit: ")
    employer_search=db_cursor.execute("select employer_id from employer where employer_name LIKE ?",[employer]).fetchall()
    if len(employer_search)==0:
        db_cursor.execute("insert into employer(employer_name) values(?)",[employer])
        db_connection.commit()
    employer_id:list[tuple[int]]=db_cursor.execute("select employer_id from employer where employer_name LIKE ?",[employer]).fetchall()[0][0]

    while True:
        is_submitted=input_validation("Have you submitted the application? (Y/N): ")
        if is_submitted.lower()=="y":
            job_status=pending
            break
        elif is_submitted.lower()=="n":
            job_status=pending_submission
            break
    #1 is for pending status
    query_parameters=[job_title,job_status,employer_id,job_site_id,current_url]
    db_cursor.execute("insert into job(job_title,job_status,employer_id,site_id,job_listing_url) values(?,?,?,?,?)",query_parameters)
    db_connection.commit()
    job_log(db_cursor,db_connection)
    input("Successfully added job, press any key to go back to main interface ")


def modify_job(db_cursor:sqlite3.Cursor,db_connection:sqlite3.Connection):
    fetch_jobs=fetch_items(db_cursor,"select job_id,job_title,employer.employer_name,job_status.status_name,job_status.hex_color from job left join employer on job.employer_id=employer.employer_id left join job_status on job.job_status=job_status.job_status")
    fetch_statuses=fetch_items(db_cursor,"select status_name from job_status")
    console=Console()
    for index,job in enumerate(fetch_jobs):
        job_name=job[1]
        company=job[2]
        current_status=job[3]
        color=job[4]
        console.print(f"{index+1}. {job_name} from {company} with status '{current_status}'",style=color,highlight=False)

    selected_job=input_table_validation(fetch_jobs,"Select a job to modify its status or press 'q' to quit: ")
    for index,status in enumerate(fetch_statuses):
        print(f"{index+1}. {status[0]}")
    selected_status=input_table_validation(fetch_statuses,"Select a status or press 'q' to quit: ")
    #In case you get a interview
    if selected_status==5:
        date=input_date_validation("%Y-%m-%d","What is the interview date (format must be YYYY-MM-DD): ","YYYY means year (i.e., 2026), MM means month (i.e.,03), and DD means day (i.e., 03), so 2026-03-03 will be March 3rd, 2026")
        time=input_date_validation("%H:%M","What is the interview time (format must be in 24-hour format): ","For 24-hour format, 2:00PM would be 14:00, 9:00AM would be 09:00, and 12:00AM would be 00:00")
        interview_time=datetime.datetime.strptime(f"{date} {time}","%Y-%m-%d %H:%M")
        db_cursor.execute("update job set interview_date=? where job_id=?",[interview_time,selected_job])
        db_connection.commit()
    current_time=datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    db_cursor.execute("update job set job_status=?,last_updated_date=? where job_id=?",[selected_status,current_time,selected_job])
    job_log(db_cursor,db_connection,selected_job)
    db_connection.commit()
    input("Successfully modified job, press any key to go back to main interface ")

    
def auto_update_ghost(db_cursor:sqlite3.Cursor,db_connection:sqlite3.Connection):
    ghost_parameters=(2,)
    ghost_query="select job_id,job_title,employer_name, floor(julianday('now')-julianday(last_updated_date)) as time_elapsed from job left join employer on job.employer_id=employer.employer_id where datetime(last_updated_date) <= datetime('now','-30 days') and job_status=1;"
    ghost_update_query="update job set job_status=? where datetime(last_updated_date) <= datetime('now','-30 days') and job_status=1;"
    fetch_ghost_jobs=fetch_items(db_cursor,ghost_query)
    db_cursor.execute(ghost_update_query,ghost_parameters)
    db_connection.commit()
    for ghost_job in fetch_ghost_jobs:
        ghosted_job_id=ghost_job[0]
        ghosted_job=ghost_job[1]
        ghosted_company=ghost_job[2]
        ghosted_time=int(ghosted_job[3])
        job_log(db_cursor,db_connection,job_id=ghosted_job_id)
        print(f"{ghosted_job} at {ghosted_company} is now a ghosted job because you hadn't heard back in {ghosted_time} days")
    



    
    