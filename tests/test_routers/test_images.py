from os import path

from tests.client import client
from tests.fixtures import (get_admin_header, get_user_header,  # noqa: F401
                            set_test_environment)

"""TEST POST REQUESTS"""


def test_post_image_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    with open('./tests/media/image.jpg', 'rb') as file:
        image_file = file.read()
    response = client.post(
        '/images/',
        data={'product_id': 1},
        files={'file': ('test.jpg', image_file, 'image/jpeg')},
        headers={'Authorization': get_admin_header}
    )
    assert response.status_code == 201


def test_post_image_by_user(get_user_header, set_test_environment):  # noqa: F811
    with open('./tests/media/image.jpg', 'rb') as file:
        image_file = file.read()
    response = client.post(
        '/images/',
        data={'product_id': 1},
        files={'file': ('test.jpg', image_file, 'image/jpeg')},
        headers={'Authorization': get_user_header}
    )
    assert response.status_code == 401


def test_post_image_with_invalid_data(get_admin_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/images/',
        data={'product_id': 1},
        headers={'Authorization': get_admin_header}
    )
    assert response.status_code == 422


"""TEST GET REQUESTS"""


def test_get_images(set_test_environment):  # noqa: F811
    response = client.get('/images/')
    response_json = response.json()
    for image in response_json:
        image.pop('url')

    assert response.status_code == 200
    assert response_json == [{'id': 1, 'product_id': 1}]


def test_get_images_by_product_id(set_test_environment):  # noqa: F811
    response = client.get('/images/?product_id=1')
    response_json = response.json()
    for image in response_json:
        image.pop('url')

    assert response.status_code == 200
    assert response_json == [{'id': 1, 'product_id': 1}]


def test_get_image(set_test_environment):  # noqa: F811
    response = client.get('/images/1/')
    response_json = response.json()
    url = response_json.pop('url')
    assert path.exists(f'./tests/media/{url}')
    assert response.status_code == 200
    assert response_json == {'id': 1, 'product_id': 1}


"""TEST DELETE REQUESTS"""


def test_delete_image_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.delete('/images/1/', headers={'Authorization': get_user_header})
    assert response.status_code == 401


def test_delete_image_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.get('/images/1/')
    url = response.json()['url']
    response = client.delete('/images/1/', headers={'Authorization': get_admin_header})

    assert response.status_code == 202
    assert response.json() is None

    response = client.get('/images/1/', headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() is None

    assert not path.exists(f'./tests/media/{url}')


def test_delete_image_with_invalid_id(get_admin_header, set_test_environment):  # noqa: F811
    response = client.delete('/images/1/', headers={'Authorization': get_admin_header})

    assert response.status_code == 202
    assert response.json() is None
