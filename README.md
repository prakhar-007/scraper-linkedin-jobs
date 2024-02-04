# Getting Started - Cheat Sheet

1. Clone this project: `git clone https://github.com/prakhar-007/scraper-linkedin-jobs.git`
2. Create a Python Virtual Environment: `python3 -m venv venv`
3. Activate the Python Virtual Environment: `source venv/bin/activate`
4. Install Scrapy,other libraries using pip: `pip install -r requirements.txt`
5. Changing the directory: `cd scraper-linkedin-jobs`
6. Listing the scrapy projects `scrapy list` 
7. Running the scrapy project: `scrapy crawl job_details` 
8. Alternatively you can save the output file using: `scrapy crawl job_details -O 'jobs.csv'` 

## Key Features

+ Implemented `Scrapy` framework to extract various fields from linkedin Job page
+ Scrap without login to linkedin
+ Dumping `output file`, `log file`
+ Integeration with `gspread` library for sending the output to google sheet [link](https://docs.google.com/spreadsheets/d/1RegbfLIgMk6qH6NAKWdSa6Of9nqTc9qLRO04JQoeX_w/edit?usp=sharing)


**Linkedin Jobs Page**

+ `Job Title`
+ `Job Post URL`
+ `Job Listed`
+ `Company Name`
+ `Company Page URL`
+ `Job Location`
+ `Seniority level`
+ `Employment type`
+ `Job function`
+ `Industries`
+ `Job Poster Information`