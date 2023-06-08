import argparse
import re
from urllib.parse import urlparse
import requests
from pypdf import PdfReader
import logging
from app.services import Headers, FileManager, ResourceManager


logger = logging.getLogger(__name__)

class LinkValidator:

    def __new__(cls, *args, **kwargs):
        validator = super().__new__(cls)
        if not args and not kwargs:
            validator.resource, validator.resource_type = cls.user_input()
        return validator

    def __init__(self, resource=None):
        if resource:
            self.resource, self.resource_type = ResourceManager.resource_validate(resource)
            logger.info(f'get resource by constructor [{resource}]')



    @classmethod
    def user_input(cls):
        parser = argparse.ArgumentParser(description="Get all links from site or pdf")
        main_group = parser.add_mutually_exclusive_group()
        main_group.add_argument('-url', '--url', type=str, help='Url address in format - [(http|https)://site.com]')
        main_group.add_argument('-pdf', '--pdf', type=str, help='Path to pdf file')
        args = parser.parse_args()
        if args.pdf:
            logger.info(f'get resource by --pdf option [{args.pdf}]')
            return ResourceManager.resource_validate(args.pdf, 'pdf')
        elif args.url:
            logger.info(f'get resource by --url option [{args.url}]')
            return ResourceManager.resource_validate(args.url, 'url')
        else:
            resource = input('Please type url of site or path to .pdf file\n -> ')
            logger.info(f'get resource by user input [{resource}]')
            return ResourceManager.resource_validate(resource)

    def _parse_content(self):
        if self.resource_type == 'url':
            links = self._get_links_from_url(self.resource)
            pretty_links = LinkAnalyzer.make_pretty_links(links, self.resource)
            LinkAnalyzer.check_links(pretty_links)
        if self.resource_type == 'pdf':
            links = self._get_links_from_pdf(self.resource)
            LinkAnalyzer.check_links(links)

    def _get_links_from_url(self, url: str) -> [str]:
        logger.info('Start method get_links_from_url')
        res = requests.get(url, headers={'user-agent': Headers.AGENT.value})
        if res.status_code == 200:
            return re.findall('href=[\'"]?([^\'" >]+)', res.text)
        else:
            print('Cannot get resource. ',
                  f'URL "{url}" has status code {res.status_code}',
                  'Try again with valid url',
                  sep='\n')
            exit()

    def _get_links_from_pdf(self, file_path: str) -> [str]:
        logger.info('Start method get_links_from_pdf')
        result = []
        reader = PdfReader(file_path)
        count_pages = len(reader.pages)
        for page_item in range(count_pages):
            page = reader.pages[page_item]
            text_of_page = page.extract_text()
            search_patern = re.compile(r"https?://(?:[\w-]+\.)+[a-z]{2,}(?:/[\w.-]*)*/?")
            all_matches = re.findall(search_patern, text_of_page)
            result.extend(all_matches)

        return result

    def run(self):
        print('Wait ...')
        self._parse_content()
        print('Done.')




class LinkAnalyzer:

    @classmethod
    def check_link(cls, link) -> bool:
        try:
            res = requests.get(link, headers={'user-agent': Headers.AGENT.value})
            if res.status_code == 200:
                return True
            return False
        except:
            return False

    @classmethod
    def check_links(cls, links):
        valid_links = ['--- Valid links of resource ---\n']
        broken_links = ['--- Broken links of resource ---\n']
        for link in links:
            if cls.check_link(link):
                valid_links.append(link + '\n')
            else:
                broken_links.append(link + '\n')

        FileManager.save_valid_links(valid_links)
        FileManager.save_broken_links(broken_links)

    @classmethod
    def make_pretty_links(cls, links: [str], url) -> [str]:
        result = []
        for item in links:
            if item.startswith("http") or item.startswith("https"):
                result.append(item)
            if item.startswith("//"):
                continue
            if item.startswith("/"):
                link = cls.clear_link(url) + item
                result.append(link)
        return result

    @classmethod
    def clear_link(cls, url) -> str:
        parsed_url = urlparse(url)
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc
        return clean_url
