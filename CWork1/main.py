from cwork import UrlAnalyzer

if __name__ == "__main__":

    try:
        app = UrlAnalyzer('https://www.makeuseof.com/useful-python-one-liners-you-must-know/')
        # app = UrlAnalyzer()
        print('Url to check - ', app.url)
        app.run()
    except Exception as ex:
        print("Sorry, but something went wrong.")
        print(f' ... {ex}')