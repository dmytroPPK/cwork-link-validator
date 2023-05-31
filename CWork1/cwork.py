import argparse
import re
from urllib.parse import urlparse
from enum import Enum
import requests

class Headers(Enum):
    AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"


class UrlAnalyzer:

    def __new__(cls, *args, **kwargs):
        analyzer = super().__new__(cls)
        if not args and not kwargs:
            analyzer.url = cls.user_input()
        return analyzer

    def __init__(self, url=None):
        if url:
            if not self.validate_user_url(url):
                print('Invalid url format was detected. Use [(http|https)://site.co] format. Run program again')
                exit()
            self.url = url
        self.link_analyzer = LinkAnalyzer()

    @classmethod
    def user_input(cls):
        parse = argparse.ArgumentParser(description="Parse all site's links")
        parse.add_argument('-url', '--url', type=str, help='Please type url in format - [(http|https)://site.com]')
        args = parse.parse_args()
        if args.url:
            if cls.validate_user_url(args.url):
                return args.url
            print('Not valid url. use -h to check format of supported url')
            exit()
        else:
            url = input('Please type url for parsing in format - [(http|https)://site.com]\n -> ')
            if cls.validate_user_url(url):
                return url
            print('Invalid url was typed. Run program again')
            exit()

    def __parse_resource(self):
        links = self.__get_links_from_url(self.url)
        pretty_links = self.__pretty_links(links)
        self.link_analyzer.check_links(pretty_links)

    def __get_links_from_url(self, url) -> list:
        res = requests.get(self.url, headers={'user-agent': Headers.AGENT.value})
        if res.status_code == 200:
            return re.findall('href=[\'"]?([^\'" >]+)', res.text)
        else:
            print('Cannot get resource. ',
                  f'URL "{self.url}" has status code {res.status_code}',
                  'Try again with valid url',
                  sep='\n')
            exit()
    def __pretty_links(self, links:list[str]) -> [str]:
        result = []
        for item in links:
            if item.startswith("http") or item.startswith("https"):
                result.append(item)
            if item.startswith("//"):
                continue
            if item.startswith("/"):
                link = self.clear_url(self.url) + item
                result.append(link)
        return result

    def run(self):
        print('Wait ...')
        self.__parse_resource()
        print('Done.')

    @classmethod
    def validate_user_url(cls, url) -> bool:
        patern = "(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
        if re.match(patern, url):
            return True
        return False

    @classmethod
    def clear_url(cls, url) -> str:
        parsed_url = urlparse(url)
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc
        return clean_url

class LinkAnalyzer:

    def check_link(self, link) -> bool:
        res = requests.get(link,headers={'user-agent': Headers.AGENT.value})
        if res.status_code == 200:
            return True
        return False

    def check_links(self, links):
        valid_links = []
        invalid_links = []
        for link in links:
            if self.check_link(link):
                valid_links.append(link+'\n')
            else:
                invalid_links.append(link+'\n')

        self.write_links(valid_links, isvalid=True)
        self.write_links(invalid_links, isvalid=False)


    def write_links(self, links:list, isvalid:bool):
        if isvalid:
            with open('valid_links.txt','a+') as file:
                file.writelines(links)
        else:
            with open('broken_links.txt', 'a+') as file:
                file.writelines(links)




