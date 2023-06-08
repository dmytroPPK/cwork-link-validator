from enum import Enum
import re
import os
import logging


logger = logging.getLogger(__name__)

class Headers(Enum):
    AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"


class FileManager:
    FOLDER = 'output'
    VALID_LINKS = 'valid_links.txt'
    BROKEN_LINKS = 'broken_links.txt'
    @classmethod
    def save_links(cls, links:[str], file, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder,file)
        with open(file_path, 'w+') as f:
            f.writelines(links)
        logger.info(f'File {file} was written')

    @classmethod
    def save_valid_links(cls, links:[str]):
        cls.save_links(links, file=cls.VALID_LINKS, folder=cls.FOLDER)

    @classmethod
    def save_broken_links(cls, links: [str]):
        cls.save_links(links, file=cls.BROKEN_LINKS, folder=cls.FOLDER)



class ResourceManager:

    @classmethod
    def check_type(cls, resource:str) -> str:
        if resource.startswith('http'):
            return 'url'
        if resource.endswith('.pdf'):
            return 'pdf'
        return 'underfined'

    @classmethod
    def url_name_isvalid(cls, url) -> bool:
        patern = "(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
        if re.match(patern, url):
            return True
        return False

    @classmethod
    def pdf_path_isvalid(cls, path:str) -> bool:
        if os.path.isfile(path):
            return True
        return False

    @classmethod
    def resource_validate(cls, resource: str, from_side='user') -> (str, str):
        resource_type = cls.check_type(resource)
        if (resource_type == 'url' and from_side == 'user') or (resource_type == 'url' and from_side == 'url'):
            if cls.url_name_isvalid(resource):
                return resource, resource_type
            else:
                print('Not valid url. use -h to check format of supported url')
                exit()
        elif (resource_type == 'pdf' and from_side == 'user') or (resource_type == 'pdf' and from_side == 'pdf'):
            if cls.pdf_path_isvalid(resource):
                return resource, resource_type
            else:
                print('Incorrect path or file does not exist. Try again')
                exit()
        else:
            raise ValueError(f'Unsupported format of resource - "{resource}"\n'
                             f' ... Use main.py -h to check supported formats')


