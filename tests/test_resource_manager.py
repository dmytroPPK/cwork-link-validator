import pytest
import logging

from app.services import ResourceManager


@pytest.mark.resource_manager
@pytest.mark.parametrize(
    ('resource','expected'),
    (
        ('https//site.com', 'url'),
        ('http://google.com', 'url'),
        ('test.pdf', 'pdf'),
        ('www.site.com', 'underfined'),
        ('test_pdf', 'underfined'),
        ('trulala', 'underfined')
    )
)
@pytest.mark.resource_manager
def test_check_type(resource, expected):
    assert ResourceManager.check_type(resource) == expected



@pytest.mark.resource_manager
@pytest.mark.parametrize(
    'pdf_path',
    [
        'test.pdf'
    ]
)
@pytest.mark.resource_manager
def test_pdf_path_isvalid(pdf_path):
    assert ResourceManager.pdf_path_isvalid(pdf_path)


@pytest.mark.resource_manager
@pytest.mark.negative_test
def test_pdf_path_isvalid_negative():
    assert not ResourceManager.pdf_path_isvalid('trulala.pdf')

@pytest.mark.resource_manager
@pytest.mark.parametrize(
    'url',
    [
        'http://google.com',
        'https://google.com/bro',
        'https://google.com?kd=1',
        'http://google.com/utr/?fr=name',
    ]
)
def test_url_name_isvalid(url):
    assert ResourceManager.url_name_isvalid(url)

@pytest.mark.resource_manager
@pytest.mark.negative_test
@pytest.mark.parametrize(
    'url',
    [
        'http//www.site.com',
        'www.bulka.com',
        'http:/www.fword.com'
    ]
)
def test_url_name_isvalid_negative(url, request):
    assert not ResourceManager.url_name_isvalid(url)


@pytest.mark.resource_manager
@pytest.mark.parametrize(
    ('resource', 'side', 'expected_type'),
    [
        ('test.pdf', 'user', 'pdf'),
        ('https://site.com', 'user', 'url'),
        ('test.pdf', 'pdf', 'pdf'),
        ('https://site.com', 'url', 'url'),
    ]
)
@pytest.mark.resource_manager
def test_resource_validate(resource, side, expected_type):
    r,t = ResourceManager.resource_validate(resource, side)
    assert (r == resource) and (t == expected_type)

@pytest.mark.negative_test
@pytest.mark.resource_manager
@pytest.mark.parametrize(
    ('resource', 'side'),
    [
        ('test.pdf', 'new_type'),
        ('https://site.com', 'new_type'),
        ('test.pdff', 'user'),
        ('htdtps://site.com', 'url'),
        ('file.txt', 'pdf'),
    ]
)
def test_resource_validate_negative(resource, side):
    with pytest.raises(ValueError):
        ResourceManager.resource_validate(resource, side)

