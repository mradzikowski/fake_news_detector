import json

from src.api.models import News


def test_add_news(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/news',
        data=json.dumps({
            'title': 'Coronavirus cases has been lowered down.',
            'url': 'https://www.tvp.info/54707513/tusk-pytany-przez-tvp-info-'
                   'o-nowak-az-sie-zatrzymal-szokujaca-odpowiedz-szefa-po',
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


def test_single_news(test_app, test_database, add_news):
    news = add_news(title="Coronavirus", url="coronavirus.com", credibility=9.0)
    client = test_app.test_client()
    resp = client.get(f'/news/{news.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Coronavirus' in data['title']
    assert 'coronavirus.com' in data['url']


def test_single_news_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/news/999')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'News 999 does not exist' in data['message']


def test_all_news(test_app, test_database, add_news):
    test_database.session.query(News).delete()
    add_news(title="Coronavirus", url="coronavirus.com", credibility=9.0)
    add_news(title="Payrise", url="payrise.com", credibility=7.0)
    client = test_app.test_client()
    resp = client.get('/news')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'Coronavirus' in data[0]['title']
    assert 'coronavirus.com' in data[0]['url']
    assert 9.0 == data[0]['credibility']

    assert 'Payrise' in data[1]['title']
    assert 'payrise.com' in data[1]['url']
    assert 7.0 == data[1]['credibility']
