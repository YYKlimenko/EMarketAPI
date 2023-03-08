from tests.client import client
from tests.fixtures import set_test_environment

"""TEST GET REQUESTS"""


def test_get_orders(set_test_environment):  # noqa: F811
    response = client.get('/orders/')

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
             'category_id': 1}
         ]}
    ]


def test_get_orders_by_user_id(set_test_environment):  # noqa: F811
    response = client.get('/orders/?user_id=1')

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
             'category_id': 1}
         ]}
    ]

    response = client.get('/orders/?user_id=2')

    assert response.status_code == 200
    assert response.json() == []


# def test_get_orders_by_user(set_test_environment):  # noqa: F811
#     response = client.get('/orders/')
#     assert response.status_code == 401


"""TEST POST REQUESTS"""


def test_post_order(set_test_environment):  # noqa: F811
    response = client.post(
        '/orders/',
        json={'user_id': 1,
              'products': [1]},
        # headers={'Authorization': get_admin_header}
    )

    assert response.status_code == 201
    assert response.json() is None

    response = client.get('/orders/2/')

    assert response.status_code == 200
    assert response.json() == {'id': 2,
                               'products': [
                                    {'id': 1,
                                     'name': 'Product 1',
                                     'description': 'Description of Product 1',
                                     'constitution': 'Constitution of Product 1',
                                     'price': 99.99,
                                     'category_id': 1}
                               ],
                               'user_id': 1,
                               }


# def test_post_order_by_user(set_test_environment):  # noqa: F811
#     response = client.post(
#         '/orders/',
#         json={'user_id': 1,
#               'products': [1]},
#         # headers={'Authorization': get_user_header}
#     )
#     assert response.status_code == 401


def test_post_order_with_invalid_data(set_test_environment):  # noqa: F811
    response = client.post(
        '/orders/',
        json={'username': 213123},
        # headers={'Authorization': get_admin_header}
    )
    assert response.status_code == 422


"""TEST DELETE REQUESTS"""


def test_delete_order_by_admin(set_test_environment):  # noqa: F811
    response = client.delete('/orders/2/')

    assert response.status_code == 202
    assert response.json() is None

    response = client.get('/orders/2/')

    assert response.status_code == 200
    assert response.json() is None


# def test_delete_order_by_user(set_test_environment):  # noqa: F811
#     response = client.delete('/orders/1/')
#     assert response.status_code == 401


def test_delete_order_by_with_invalid_id(set_test_environment):  # noqa: F811
    response = client.delete('/orders/3/')

    assert response.status_code == 202
    assert response.json() is None
