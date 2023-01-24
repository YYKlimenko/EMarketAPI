from tests.client import client
from tests.fixtures import (get_admin_header, get_user_header,  # noqa: F401
                            set_test_environment)

"""TEST GET REQUESTS"""


def test_get_orders(get_admin_header, set_test_environment):  # noqa: F811
    response = client.get('/orders/', headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1,
         'user_id': 1,
         'products': [
            {'id': 1,
             'name': 'Product 1',
             'description': 'Description of Product 1',
             'constitution': 'Constitution of Product 1',
             'price': 99.99,
             'category_id': 1,
             'images': []}
         ]}
    ]


def test_get_orders_by_user_id(get_admin_header, set_test_environment):  # noqa: F811
    response = client.get('/orders/?user_id=1', headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1,
         'user_id': 1,
         'products': [
            {'id': 1,
             'name': 'Product 1',
             'description': 'Description of Product 1',
             'constitution': 'Constitution of Product 1',
             'price': 99.99,
             'category_id': 1,
             'images': []}
         ]}
    ]

    response = client.get('/orders/?user_id=2', headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() == []


def test_get_orders_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.get('/orders/', headers={'Authorization': get_user_header})
    assert response.status_code == 401


"""TEST POST REQUESTS"""


def test_post_order(get_admin_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/orders/',
        json={'user_id': 1,
              'products': [1]},
        headers={'Authorization': get_admin_header}
    )

    assert response.status_code == 201
    assert response.json() is None

    response = client.get('/orders/2/', headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() == {'id': 2,
                               'products': [
                                    {'id': 1,
                                     'name': 'Product 1',
                                     'description': 'Description of Product 1',
                                     'constitution': 'Constitution of Product 1',
                                     'price': 99.99,
                                     'category_id': 1,
                                     'images': []}
                               ],
                               'user_id': 1,
                               }


def test_post_order_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/orders/',
        json={'user_id': 1,
              'products': [1]},
        headers={'Authorization': get_user_header}
    )
    assert response.status_code == 401


def test_post_order_with_invalid_data(get_admin_header, set_test_environment):  # noqa: F811
    response = client.post(
        '/orders/',
        json={'username': 213123},
        headers={'Authorization': get_admin_header}
    )
    assert response.status_code == 422


"""TEST DELETE REQUESTS"""


def test_delete_order_by_admin(get_admin_header, set_test_environment):  # noqa: F811
    response = client.delete('/orders/2/', headers={'Authorization': get_admin_header})

    assert response.status_code == 202
    assert response.json() is None

    response = client.get('/orders/2/', headers={'Authorization': get_admin_header})

    assert response.status_code == 200
    assert response.json() is None


def test_delete_order_by_user(get_user_header, set_test_environment):  # noqa: F811
    response = client.delete('/orders/1/', headers={'Authorization': get_user_header})
    assert response.status_code == 401


def test_delete_order_by_with_invalid_id(get_admin_header, set_test_environment):  # noqa: F811
    response = client.delete('/orders/3/', headers={'Authorization': get_admin_header})

    assert response.status_code == 202
    assert response.json() is None
