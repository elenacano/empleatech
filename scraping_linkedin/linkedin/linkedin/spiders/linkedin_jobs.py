import scrapy

class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_jobs"
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2Bscience&location=Madrid&geoId=100994331&trk=public_jobs_jobs-search-bar_search-submit&start='

    # custom_settings = {
    #     'FEEDS': {
    #         'data/linkedin_madrid_data_analyst.csv': {'format': 'csv', 'overwrite': False},
    #     },
    #     'LOG_LEVEL': 'INFO',
    # }

    def __init__(self, START_POINT=0, SEARCH_TERM="", *args, **kwargs):
        super(LinkedJobsSpider, self).__init__(*args, **kwargs)
        self.START_POINT = int(START_POINT)
        self.MAX_JOBS_PER_BLOCK = 250
        self.search_term = SEARCH_TERM
        empleo = self.search_term.split("_")[1]
        print(empleo)
        self.api_url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2B{empleo}&location=Madrid&geoId=100994331&trk=public_jobs_jobs-search-bar_search-submit&start='

        self.output_file = f"data/linkedin_madrid_{self.search_term}.csv"
        # self.custom_settings = {
        #     'FEEDS': {
        #         output_file: {'format': 'csv', 'overwrite': False},
        #     },
        #     'LOG_LEVEL': 'INFO',
        # }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LinkedJobsSpider, cls).from_crawler(crawler, *args, **kwargs)

        # Configuración dinámica de FEEDS
        feed_config = {
            spider.output_file: {'format': 'csv', 'overwrite': False}
        }
        crawler.settings.set('FEEDS', feed_config, priority='spider')
        crawler.settings.set('LOG_LEVEL', 'INFO', priority='spider')
        return spider

    def start_requests(self):
        first_job_on_page = self.START_POINT
        calls = 0
        total_jobs = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page, 'calls': calls, 'total_jobs': total_jobs})

    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']
        total_jobs = response.meta['total_jobs']
        calls = response.meta['calls']
        
        jobs = response.css("li")
        num_jobs_returned = len(jobs)

        # Si no devuelve 25 jobs es porque algo ha ido mal, por lo que repetimos la llamada
        if num_jobs_returned != 25:
            print(f"\n La llamada ha devuelto {num_jobs_returned} jobs\n")
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page, 'calls': calls, 'total_jobs': total_jobs})

        else:
            calls += 1
            total_jobs += num_jobs_returned

            print("******* Metadata *******")
            print(f"First job on page: {first_job_on_page}")
            print(f"Number of jobs returned: {num_jobs_returned}")
            print(f"Number of calls in block: {calls}")
            print(f"Total jobs so far: {total_jobs}")
            print('**************************')

            for job in jobs:
                job_item = {
                    'job_title': job.css("h3::text").get(default='not-found').strip(),
                    'job_detail_url': job.css(".base-card__full-link::attr(href)").get(default='not-found').strip(),
                    'job_listed': job.css('time::text').get(default='not-found').strip(),
                    'company_name': job.css('h4 a::text').get(default='not-found').strip(),
                    'company_link': job.css('h4 a::attr(href)').get(default='not-found'),
                    'company_location': job.css('.job-search-card__location::text').get(default='not-found').strip(),
                }
                yield job_item

            # Continuar al siguiente bloque si no se ha alcanzado el límite de llamadas
            if num_jobs_returned > 0 and total_jobs < self.MAX_JOBS_PER_BLOCK:
                first_job_on_page += num_jobs_returned
                next_url = self.api_url + str(first_job_on_page)
                yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page, 'calls': calls, 'total_jobs': total_jobs})
            