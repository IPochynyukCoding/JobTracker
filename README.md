# JobTracker CLI Application
## Disclaimer
**MAKE SURE TO NOT OPEN THE jobs.db FILE ON ANY OTHER SQLite BROWSERS OR EDITORS SUCH AS DB BROWSER, OTHERWISE IT WILL GIVE YOU A "Database is Locked" ERROR!**
## Purpose
JobTracker is a simple Python CLI interface to add jobs, modify job statuses, and view all jobs in a simple and elegant table. JobTracker also uses a SQLite database to ensure entirely local functionality without any online connections or fancy software. Lastly, JobTracker only requires one outside dependency to work, Rich, to ensure a nice and clean table interface, compared to using Pandas, MatPlotLib, and Plottable to provide the same (if not more complex) interface.
## Steps to set up the project
1. Use ```git clone https://github.com/IPochynyukCoding/jobtracker``` to initialize the repository.
2. Make sure you go to the "jobtracker" folder to ensure the files will work
3. Use ```pip install requirements.txt``` to install the Rich Python library 
4. Open main_interface.py to setup the SQLite database to create the database.

## How to add a job to the database
1. Open the main_interface.py file and press '2' on the menu
2. Paste the job URL from your browser (if the base URL does not exist, it will prompt you to add the site's name to add to the database)
3. Paste the job title from the job listing
4. Paste the employer name from the job listing
5. Wait for the database to add the job

## How to modify a job's status
1. Open the main_interface.py file and press '3' on the menu
2. Find the job you want to update
3. Select the most recent status in the list (i.e., if you get a rejection email, select "Rejected")
### Special Case, in case you get an interview
4. Input the date with the format of "YYYY-MM-DD", which if you get an interview date on Feburary 4th, 2026, input ```2026-02-04``` to the prompt.
5. Input the time with the 24-hour format, which if you get an interview at "2:00PM", input ```14:00``` to the prompt, or if you have an interview at "12:00AM", input ```00:00``` to the prompt. Lastly, if you have an interview at "9:00AM", input ```09:00``` to the prompt.

## How to view the job table
1. Open the main_interface.py file and press '1' on the menu.
2. View the table to your heart's content, though it will not update if you open another instance of 'main_interface.py' and either update the job's status or add a job.
3. Press any key to exit the table view.
