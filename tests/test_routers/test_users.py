from tests.client import client
from tests.fixtures import get_admin_header, get_user_header, set_test_environment  # noqa: F401


"""TEST GET REQUESTS"""


def test_get_users_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.get('/users/', headers={'Authorization': get_admin_header})
    assert response.status_code == 200

    response = response.json()

    for user in response:
        user.pop('date_registration')

    assert response == [
        {'id': 1,
         'username': 'admin',
         'number': '88888888888',
         'is_admin': True
         },
        {'id': 2,
         'username': 'user',
         'number': '99999999999',
         'is_admin': False
         }
    ]


def test_get_admin_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.get('/users/1/', headers={'Authorization': get_admin_header})
    assert response.status_code == 200

    response = response.json()
    response.pop('date_registration')

    assert response == {
        'id': 1,
        'username': 'admin',
        'number': '88888888888',
        'is_admin': True
    }


def test_get_user_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.get('/users/2/', headers={'Authorization': get_admin_header})
    assert response.status_code == 200

    response = response.json()
    response.pop('date_registration')

    assert response == {
        'id': 2,
        'username': 'user',
        'number': '99999999999',
        'is_admin': False
    }


def test_get_users_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.get('/users/', headers={'Authorization': get_user_header})
    assert response.status_code == 401


def test_get_user_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.get('/users/2/', headers={'Authorization': get_user_header})
    assert response.status_code == 200

    response = response.json()
    response.pop('date_registration')

    assert response == {
        'id': 2,
        'username': 'user',
        'number': '99999999999',
        'is_admin': False
    }


def test_get_another_user_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.get('/users/1/', headers={'Authorization': get_user_header})
    assert response.status_code == 401


def test_get_nonexistent_user(get_admin_header, set_test_environment):  # noqa: F811
    response = client.get('/users/3/', headers={'Authorization': get_admin_header})
    assert response.status_code == 200
    assert response.json() is None


"""TEST POST REQUESTS"""


def test_post_user(get_admin_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/users/registration/',
        json={
            'username': 'user_3',
            'password': 'password',
            'password2': 'password',
            'number': '88888888889'
        }
    )
    assert response.status_code == 201
    assert response.json() is None

    response = client.get("/users/3/", headers={'Authorization': get_admin_header})
    assert response.status_code == 200

    response = response.json()
    response.pop('date_registration')

    assert response == {
        'id': 3,
        'username': 'user_3',
        'number': '88888888889',
        'is_admin': False
    }


def test_post_user_with_invalid_data(get_admin_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/users/registration/',
        json={
            'username': 'user_3',
            'password': 'password',
            'password2': 'password',
            'number': '88888888888'
        }
    )
    assert response.status_code == 422


"""TEST PUT REQUESTS"""


def test_put_user_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.put(
        '/users/3/',
        json={'username': 'user_3_updated'},
        headers={'Authorization': get_admin_header}
    )
    assert response.status_code == 202
    assert response.json() is None

    response = client.get("/users/3/", headers={'Authorization': get_admin_header})
    assert response.status_code == 200

    response = response.json()
    response.pop('date_registration')

    assert response == {
        'id': 3,
        'username': 'user_3_updated',
        'number': '88888888889',
        'is_admin': False
    }


def test_put_user_by_another_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.put(
        '/users/3/',
        json={'username': 'user_3_updated_again'},
        headers={'Authorization': get_user_header}
    )
    assert response.status_code == 401


def test_put_user_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.put(
        '/users/2/',
        json={'username': 'user_2_updated'},
        headers={'Authorization': get_user_header}
    )
    assert response.status_code == 202
    assert response.json() is None

    response = client.get('/users/2/', headers={'Authorization': get_user_header})
    assert response.status_code == 200

    response = response.json()
    response.pop('date_registration')

    assert response == {
        'id': 2,
        'username': 'user_2_updated',
        'number': '99999999999',
        'is_admin': False
    }


def test_put_user_with_invalid_data(get_admin_header, set_test_environment):  # noqa: F811
    response = client.put(
        '/users/3/',
        json={'number': '99999999999'},
        headers={'Authorization': get_admin_header}
    )
    assert response.status_code == 422


"""TEST PUT REQUESTS"""


def test_delete_user_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.delete('/users/3/', headers={'Authorization': get_admin_header})
    assert response.status_code == 202
    assert response.json() is None

    response = client.get('/users/3/', headers={'Authorization': get_admin_header})
    assert response.status_code == 200

    assert response.json() is None


def test_delete_user_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.delete('/users/2/', headers={'Authorization': get_user_header})
    assert response.status_code == 202
    assert response.json() is None

    response = client.get('/users/2/', headers={'Authorization': get_user_header})
    assert response.status_code == 200

    assert response.json() is None


def test_delete_user_by_another_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.delete('/users/1/', headers={'Authorization': get_user_header})
    assert response.status_code == 401
