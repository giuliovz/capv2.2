from painel.webapp import app


def test_endpoint_tom_ia_get_e_post():
    with app.test_client() as client:
        r_get = client.get('/api/ia/tom')
        assert r_get.status_code == 200
        payload = r_get.get_json()
        assert payload['tom'] in {'conservador', 'equilibrado', 'agressivo'}

        r_post = client.post('/api/ia/tom', json={'tom': 'agressivo'})
        assert r_post.status_code == 200
        payload_post = r_post.get_json()
        assert payload_post['ok'] is True
        assert payload_post['tom'] == 'agressivo'

        r_get2 = client.get('/api/ia/tom')
        assert r_get2.status_code == 200
        assert r_get2.get_json()['tom'] == 'agressivo'


def test_endpoint_tom_ia_invalido():
    with app.test_client() as client:
        r = client.post('/api/ia/tom', json={'tom': 'xpto'})
        assert r.status_code == 400
        assert r.get_json()['ok'] is False
