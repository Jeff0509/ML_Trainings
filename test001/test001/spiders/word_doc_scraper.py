import scrapy
import os

class WordDocScraper(scrapy.Spider):
    name = 'word_doc_scraper'
    allowed_domains = ['vic.gov.au']  # Replace with the website's domain
    start_urls = ['https://www.vic.gov.au/vet-funding-contracts']  # Replace with the website's URL

    def parse(self, response):
        # Specify the file extension you want to download (e.g., .docx)
        file_extension = '.docx'

        # Find all links on the webpage
        links = response.css('a::attr(href)').getall()

        for link in links:
            if link.endswith(file_extension):
                # Download the file and save it in the 'downloaded_files' directory
                file_url = response.urljoin(link)
                yield {
                    'file_url': file_url
                }
                # Create a filename based on the URL and save the file
                file_name = os.path.join('downloaded_files', file_url.split('/')[-1])
                yield scrapy.Request(file_url, callback=self.save_file, meta={'file_name': file_name})

    def save_file(self, response):
        file_name = response.meta['file_name']
        with open(file_name, 'wb') as f:
            f.write(response.body)

# Create a directory to store downloaded files
if not os.path.exists('downloaded_files'):
    os.makedirs('downloaded_files')