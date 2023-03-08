from tests.client import client
from tests.fixtures import set_test_environment # noqa: F401

"""TEST GET REQUESTS"""


def test_get_products(set_test_environment):  # noqa: F811
    response = client.get('/products/')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1,
         'name': 'Product 1',
         'description': 'Description of Product 1',
         'constitution': 'Constitution of Product 1',
         'price': 99.99,
         'category_id': 1,
         'images': []}
    ]


def test_get_products_by_category_id(set_test_environment):  # noqa: F811
    response = client.get('/products/?category_id=1')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1,
         'name': 'Product 1',
         'description': 'Description of Product 1',
         'constitution': 'Constitution of Product 1',
         'price': 99.99,
         'category_id': 1,
         'images': []}
    ]

    response = client.get('/products/?category_id=2')

    assert response.status_code == 200
    assert response.json() == []


def test_get_products_by_price(set_test_environment):  # noqa: F811
    response = client.get('/products/?price=eq_99.99')
    assert response.status_code == 200

    assert response.json() == [
        {'id': 1,
         'name': 'Product 1',
         'description': 'Description of Product 1',
         'constitution': 'Constitution of Product 1',
         'price': 99.99,
         'category_id': 1,
         'images': []}
    ]

    response = client.get('/products/?price=lt_99.99')
    assert response.status_code == 200
    assert response.json() == []

    response = client.get('/products/?price=gt_99.99')
    assert response.status_code == 200
    assert response.json() == []

    response = client.get('/products/?price=le_99.99')
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1,
         'name': 'Product 1',
         'description': 'Description of Product 1',
         'constitution': 'Constitution of Product 1',
         'price': 99.99,
         'category_id': 1,
         'images': []}
    ]

    response = client.get('/products/?price=ge_99.99')
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1,
         'name': 'Product 1',
         'description': 'Description of Product 1',
         'constitution': 'Constitution of Product 1',
         'price': 99.99,
         'category_id': 1,
         'images': []}
    ]


def test_get_product(set_test_environment):  # noqa: F811
    response = client.get('/products/1/')

    assert response.status_code == 200
    assert response.json() == {'id': 1,
                               'name': 'Product 1',
                               'description': 'Description of Product 1',
                               'constitution': 'Constitution of Product 1',
                               'price': 99.99,
                               'category_id': 1,
                               'images': []}


"""TEST POST REQUESTS"""


def test_post_product(set_test_environment):  # noqa: F811
    response = client.post(
        '/products/',
        json={'name': 'Product 2',
              'description': 'Description of Product 2',
              'constitution': 'Constitution of Product 2',
              'price': 99.99,
              'category_id': 2},
        # headers={'Authorization': get_admin_header}
    )

    assert response.status_code == 201
    assert response.json() is None

    response = client.get('/products/2/')

    assert response.status_code == 200
    assert response.json() == {'id': 2,
                               'name': 'Product 2',
                               'description': 'Description of Product 2',
                               'constitution': 'Constitution of Product 2',
                               'price': 99.99,
                               'category_id': 2,
                               'images': []}


def test_post_product_with_invalid_data(set_test_environment):  # noqa: F811
    response = client.post(
        '/products/',
        json={'username': 213123},
        # headers={'Authorization': get_admin_header}
    )

    assert response.status_code == 422


# def test_post_product_by_user(set_test_environment):  # noqa: F811
#     response = client.post(
#         '/products/',
#         json={'name': 'Product 2',
#               'description': 'Description of Product 2',
#               'constitution': 'Constitution of Product 2',
#               'price': 199.99,
#               'category_id': 2},
#         # headers={'Authorization': get_user_header}
#     )
#
#     assert response.status_code == 401


"""TEST PUT REQUESTS"""


def test_put_product_by_admin(set_test_environment):  # noqa: F811
    response = client.put(
        '/products/2/',
        json={'name': 'Product 2 updated'},
        # headers={'Authorization': get_admin_header}
    )

    assert response.status_code == 202
    assert response.json() is None

    response = client.get("/products/2/")

    assert response.status_code == 200
    assert response.json() == {'id': 2,
                               'name': 'Product 2 updated',
                               'description': 'Description of Product 2',
                               'constitution': 'Constitution of Product 2',
                               'price': 99.99,
                               'category_id': 2,
                               'images': []}


# def test_put_product_by_user(set_test_environment):  # noqa: F811
#     response = client.put(
#         '/products/2/',
#         json={'name': 'Product 2 updated'},
#         # headers={'Authorization': get_user_header}
#     )
#     assert response.status_code == 401
#
#
def test_put_product_with_invalid_data(set_test_environment):  # noqa: F811
    response = client.put(
        '/products/2/',
        json={'number': '88000965599'},
        # headers={'Authorization': get_admin_header}
    )
    assert response.status_code == 422


"""TEST DELETE REQUESTS"""


def test_delete_product(set_test_environment):  # noqa: F811
    response = client.delete('/products/2/')

    assert response.status_code == 202
    assert response.json() is None

    response = client.get('/products/2/')

    assert response.status_code == 200
    assert response.json() is None


# def test_delete_product_by_user(set_test_environment):  # noqa: F811
#     response = client.delete('/products/1/')
#     assert response.status_code == 401
#
#
# def test_delete_product_by_with_invalid_id(set_test_environment):  # noqa: F811
#     response = client.delete('/products/3/')
#
#     assert response.status_code == 202
#     assert response.json() is None
