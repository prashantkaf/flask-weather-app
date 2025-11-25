def test_index_get(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Flask Weather" in res.data


def test_post_empty_city(client):
    res = client.post('/', data={'city': ''}, follow_redirects=True)
    assert res.status_code == 200
    assert b"Please enter a city name." in res.data
