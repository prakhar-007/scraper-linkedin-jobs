from typing import Iterable
import scrapy
from scrapy.http import Request
import time
import logging
import datetime
from bs4 import BeautifulSoup
import requests
import gspread


gc = gspread.service_account(filename='creds.json')
sh = gc.open('gspread').sheet1
sh.clear()
sh.append_row(['job_title','job_detail_url','job_listed', 'company_name', 'company_link','company_location', 'Seniority level', 'Employment type', 'Job function', 'Industries', 'Job Poster Information'])
sh.freeze(rows=1)
logger = logging.basicConfig(level = logging.INFO, filename='jobs.log',format= '%(asctime)s %(message)s:')
class LinkedinJobs(scrapy.Spider):
    name = 'job_details'
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?f_WT=2&location=Worldwide&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&start='
    # Above url is used as starting url to start the crawler (having 25 job posts)
    # with the initial value of first_job_page as 0 which will feed '&start=0', 
    # then will keep increasing the 25,50 and so on
    
    def start_requests(self) -> Iterable[Request]:
          first_job_page = 0
          first_url = self.api_url + str(first_job_page)
          yield scrapy.Request(url=first_url,callback=self.parse, meta={'first_job_page': first_job_page})
          
    def parse(self, response):
        
        first_job_page = response.meta['first_job_page']
        job_item = {}
        jobs = response.css('li')
        num_jobs_returned = len(jobs)
        
        
        for job in jobs:
            
            job_item['job_title'] = job.css("h3::text").get(default='not-found').strip()
            job_item['job_detail_url'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            job_item['job_listed'] = job.css('time::text').get(default='not-found').strip()

            job_item['company_name'] = job.css('h4 a::text').get(default='not-found').strip()
            job_item['company_link'] = job.css('h4 a::attr(href)').get(default='not-found')
            job_item['company_location'] = job.css('.job-search-card__location::text').get(default='not-found').strip()
            
            try: #this block of code handles the scraping part by going to job_detail_url and fetching required info using bs4
                URL = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
                r = requests.get(URL) 
                soup = BeautifulSoup(r.content, 'html.parser')
                
                job_type = soup.find_all('span', attrs = {'class':'description__job-criteria-text description__job-criteria-text--criteria'}) 
                job_item['Seniority level'] = job_type[0].text.strip()
                job_item['Employment type'] = job_type[1].text.strip()
                job_item['Job function'] = job_type[2].text.strip()
                job_item['Industries'] = job_type[3].text.strip()

                job_info = soup.find('div', attrs = {'class':'show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden'}) 
                job_item['Job Poster Information'] = job_info.text.strip()
            except:
                job_item['Seniority level'] = 'not-found'
                job_item['Employment type'] = 'not-found'
                job_item['Job function'] = 'not-found'
                job_item['Industries'] = 'not-found'
                job_item['Job Poster Information'] = 'not-found'
            
            #using append_row method to add each row automatically in the gspread spreadsheet
            sh.append_row([job_item['job_title'], 
                           job_item['job_detail_url'],
                           job_item['job_listed'],
                           job_item['company_name'],
                           job_item['company_link'],
                           job_item['company_location'],
                           job_item['Seniority level'],
                           job_item['Employment type'],
                           job_item['Job function'],
                           job_item['Industries'],
                           job_item['Job Poster Information']])
            logging.info("Getting row")
            
        
            
            yield job_item
            
            
        time.sleep(0.1)
        

        #### REQUEST NEXT PAGE OF JOBS HERE ######
        if num_jobs_returned > 0:
            first_job_page = int(first_job_page) + 25
            next_url = self.api_url + str(first_job_page)
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'first_job_page': first_job_page})