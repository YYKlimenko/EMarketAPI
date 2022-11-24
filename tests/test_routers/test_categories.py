from tests.client import client
from tests.fixtures import get_admin_header, get_user_header, set_test_environment  # noqa: F401


"""TEST GET REQUESTS"""


def test_get_categories(set_test_environment):  # noqa: F811
    response = client.get('/categories/')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'name': 'Test category 1'},
        {'id': 2, 'name': 'Test category 2'},
    ]


def test_get_categories_by_name(set_test_environment):  # noqa: F811
    response = client.get('/categories/?name=Test category 1')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1,
         'name': 'Test category 1'
         },
    ]


def test_get_categories_by_wrong_name(set_test_environment):  # noqa: F811
    response = client.get('/categories/?name=3242342')
    assert response.status_code == 200

    response = response.json()
    assert response == []


"""TEST POST REQUESTS"""


def test_post_category(get_admin_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/categories/',
        json={'name': 'Test category 3'},
        headers={'Authorization': get_admin_header}
    )

    assert response.status_code == 201
    assert response.json() is None

    response = client.get("/categories/3/", headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() == {
        'id': 3,
        'name': 'Test category 3'
    }


def test_post_category_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/categories/',
        json={'name': 'Test category 3'},
        headers={'Authorization': get_user_header}
    )
    assert response.status_code == 401


def test_post_category_with_invalid_data(get_admin_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/categories/',
        json={'username': 213123},
        headers={'Authorization': get_admin_header}
    )
    assert response.status_code == 422


"""TEST PUT REQUESTS"""


def test_put_category_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.put(
        '/categories/3/',
        json={'name': 'Test category 3 updated'},
        headers={'Authorization': get_admin_header}
    )

    assert response.status_code == 202
    assert response.json() is None

    response = client.get("/categories/3/", headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() == {
        'id': 3,
        'name': 'Test category 3 updated',
    }


def test_put_category_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.put(
        '/categories/2/',
        json={'username': 'user_3_updated_again'},
        headers={'Authorization': get_user_header}
    )

    assert response.status_code == 401


def test_put_category_with_invalid_data(get_admin_header, set_test_environment):  # noqa: F811
    response = client.put(
        '/categories/2/',
        json={'number': '88000965599'},
        headers={'Authorization': get_admin_header}
    )

    assert response.status_code == 422


"""TEST DELETE REQUESTS"""


def test_delete_category_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.delete('/categories/3/', headers={'Authorization': get_admin_header})

    assert response.status_code == 202
    assert response.json() is None

    response = client.get('/categories/3/', headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() is None


def test_delete_category_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.delete('/categories/3/', headers={'Authorization': get_user_header})
    assert response.status_code == 401
