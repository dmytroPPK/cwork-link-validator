from app.core import LinkValidator

class TestLinkValidator:
    def test_get_links_from_url(self):
        url = 'https://www.google.com'
        result = LinkValidator(url)._get_links_from_url(url)
        assert len(result) > 0

    def test_get_links_from_pdf(self):
        pdf = 'test.pdf'
        result = LinkValidator(pdf)._get_links_from_pdf(pdf)
        assert len(result) > 0