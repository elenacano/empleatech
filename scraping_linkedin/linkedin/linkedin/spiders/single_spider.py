import scrapy

class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_single_jobs"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2Bscience&location=Madrid&geoId=100994331&trk=public_jobs_jobs-search-bar_search-submit&start=' 

    custom_settings = {
        'FEEDS':{
            'data/linkedin_madrid_data_science.json' :{'format':'csv', 'overwrite':True},
        }
    }

    def start_requests(self):
        first_job_on_page = 0
        calls = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page, 'calls': calls, 'total_jobs':0})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']
        total_jobs = response.meta['total_jobs']
        calls = response.meta['calls']
        calls += 1

        job_item = {}
        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        total_jobs += num_jobs_returned

        print("******* Metadata *******")
        print(f"Number of jobs returned: {num_jobs_returned}")
        print(f"Number of calls: {calls}")
        print(f"Total jobs: {total_jobs}")
        print('*****')
        
        for job in jobs:
            
            job_item['job_title'] = job.css("h3::text").get(default='not-found').strip()
            job_item['job_detail_url'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            job_item['job_listed'] = job.css('time::text').get(default='not-found').strip()

            job_item['company_name'] = job.css('h4 a::text').get(default='not-found').strip()
            job_item['company_link'] = job.css('h4 a::attr(href)').get(default='not-found')
            job_item['company_location'] = job.css('.job-search-card__location::text').get(default='not-found').strip()
            yield job_item
        

        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + num_jobs_returned
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page, 'calls' : calls, 'total_jobs':total_jobs})

    

