import pytest
from backend.services.swapi_service import SwapiService

class DummyClient:
    pass  # Not used for sort/paginate tests

@pytest.fixture
def service():
    return SwapiService(DummyClient())

def test_paginate_basic(service):
    data = [{'id': i} for i in range(25)]
    base_url = "/resource"
    result = service.paginate(data, page=2, base_url=base_url)
    assert result['count'] == 25
    assert result['results'] == data[10:20]
    assert result['next'] == f"{base_url}?page=3"
    assert result['previous'] == f"{base_url}?page=1"

def test_paginate_first_page(service):
    data = [{'id': i} for i in range(25)]
    base_url = "/resource"
    result = service.paginate(data, page=1, base_url=base_url)
    assert result['count'] == 25
    assert result['results'] == data[:10]
    assert result['next'] == f"{base_url}?page=2"
    assert result['previous'] is None

def test_paginate_last_page(service):
    data = [{'id': i} for i in range(25)]
    base_url = "/resource"
    result = service.paginate(data, page=3, base_url=base_url)
    assert result['results'] == data[20:25]
    assert result['next'] is None
    assert result['previous'] == f"{base_url}?page=2"

def test_paginate_out_of_range(service):
    data = [{'id': i} for i in range(5)]
    base_url = "/resource"
    result = service.paginate(data, page=2, base_url=base_url)
    assert result['results'] == []
    assert result['next'] is None
    assert result['previous'] == f"{base_url}?page=1"

def test_sort_data(service):
    data = [{'name': 'b'}, {'name': 'a'}, {'name': 'c'}]
    sorted_data = service.sort_data(data, 'name')
    assert [d['name'] for d in sorted_data] == ['a', 'b', 'c']

def test_sort_data_missing_key(service):
    data = [{'name': 'b'}, {'other': 1}, {'name': 'a'}]
    sorted_data = service.sort_data(data, 'name')
    assert sorted_data[0]['name'] == 'a' 