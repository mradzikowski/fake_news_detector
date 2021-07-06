import json


def test_add_news(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/news',
        data=json.dumps({
            'title': 'Coronavirus cases has been lowered down.',
            'url': 'https://www.tvp.info/54707513/tusk-pytany-przez-tvp-info-o-nowak-az-sie-zatrzymal-szokujaca-odpowiedz-szefa-po',
            'credibility': 10
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'Coronavirus cases has been lowered down. was added!' in data['message']


def test_add_news_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/news',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_news_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/news',
        data=json.dumps({
            "title": "Coronavirus Delta!!!"
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_news_duplicate_title(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/news',
        data=json.dumps({
            'title': 'Coronavirus cases has been lowered down.',
            'url': 'https://www.tvp.info/54707513/tusk-pytany-przez-tvp-info-o-nowak-az-sie-zatrzymal-szokujaca-odpowiedz-szefa-po',
            'credibility': 10
        }),
        content_type='application/json',
    )
    resp = client.post(
        '/news',
        data=json.dumps({
            'title': 'Coronavirus cases has been lowered down.',
            'url': 'https://www.tvp.info/54707513/tusk-pytany-przez-tvp-info-o-nowak-az-sie-zatrzymal-szokujaca-odpowiedz-szefa-po',
            'credibility': 10
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That title already exists' in data['message']