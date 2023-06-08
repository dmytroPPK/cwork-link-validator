from app.core import LinkValidator
import logging

logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s : %(levelname)s -> %(message)s')

if __name__ == "__main__":

    try:

        app = LinkValidator()
        # app = LinkValidator('https://www.makeuseof.com/useful-python-one-liners-you-must-know/')
        # app = LinkValidator('test.pdf')
        print('Resource to check - ', app.resource)
        app.run()
    except Exception as ex:
        print("Error was occured:")
        print(f' ... {ex}')