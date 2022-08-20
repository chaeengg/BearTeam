import requests

def test_get_img(url, **queries):
    res = requests.get('http://localhost:8000/test/img', params=queries)
    
    assert res.state_code == 200
    # Some others...

    return True