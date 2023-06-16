import pytest

from app.core import LinkAnalyzer

@pytest.mark.link_analyzer
@pytest.mark.parametrize(
    ('url', 'expected'),
    [
        ('https://movie.com/actions', 'https://movie.com',),
        ('https://movie.com/?a=1', 'https://movie.com',)
    ]
)
def test_clear_link(url, expected):
    assert LinkAnalyzer.clear_link(url) == expected

@pytest.mark.link_analyzer
@pytest.mark.parametrize(
    ('links', 'url', 'expected'),
    [
        (['/actions'], 'https://movie.com', 'https://movie.com/actions'),
        (['/?a=1'], 'https://movie.com', 'https://movie.com/?a=1')
    ]
)
def test_make_pretty_links(links, url, expected):
    assert LinkAnalyzer.make_pretty_links(links, url)[0] == expected

@pytest.mark.link_analyzer
def test_check_link():
    link = 'https://www.google.com'
    assert LinkAnalyzer.check_link(link)

@pytest.mark.link_analyzer
@pytest.mark.negative_test
def test_check_link_negative():
    link = 'http://www.brokensite.com/path'
    assert  not LinkAnalyzer.check_link(link)
