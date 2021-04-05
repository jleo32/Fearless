import pytest

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_basic(client):
    add_response = client.post('/item', data={'names': 'name1,name2,name3'})
    assert add_response.json.get('success')

    get_response = client.get('/item')
    assert len(get_response.json.get('data')) == 3

    put_response = client.put('/item/1/updated_name')
    assert put_response.json.get('success')

    get_id_response = client.get('/item/1')
    assert get_id_response.json.get('data')
    assert get_id_response.json.get('data')[0]['name'] == 'updated_name'

    delete_id_response = client.delete('/item/3')
    assert delete_id_response.json.get('success')

    get_response = client.get('/item')
    assert len(get_response.json.get('data')) == 2
