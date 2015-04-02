# coding:utf-8

import time
import pytest
import requests
from firewood import fw

fw.autoloads.append('app')
fw.session_key = 'sessionkey'
fw.build()
fw.run(background=True)
time.sleep(1)


@pytest.mark.parametrize('method', ['get', 'post', 'put', 'delete',
                                    'head', 'options', 'patch'])
def test_basics(method):
    assert requests.get('http://localhost:5000').status_code == 200


def test_exc_in_exchandler():
    r = requests.get('http://localhost:5000/typeerror')
    assert r.status_code == 500
    assert r.text == ''


def test_config():
    assert fw.config.stage_value == 100


def test_thread():
    assert fw.thread.thread_value == 100


def test_session():
    url = 'http://localhost:5000/session'

    sess = requests.Session()
    assert sess.post(url).status_code == 200

    r = sess.get(url)
    assert r.status_code == 200
    assert r.json() == {'id': 1}

    assert sess.delete(url).status_code == 200

    r = sess.get(url)
    assert r.status_code == 401


def test_exc():
    baseurl = 'http://localhost:5000'

    assert requests.get(baseurl + '/not_found').status_code == 404
    assert requests.post(baseurl + '/typeerror').status_code == 405
    assert requests.get(baseurl + '/insufficient').status_code == 400
    assert requests.get(baseurl + '/validation',
                        params={'a': 'x'}).status_code == 400
    assert requests.get(baseurl + '/error').status_code == 400
    assert requests.get(baseurl + '/valueerror').status_code == 500
