import requests
import jsonschema
from utils import load_schema


BASE_URL = 'https://reqres.in'


def test_get_single_user_status_not_ok():
    response = requests.get(url=f'{BASE_URL}/api/users/23')
    assert (response.status_code == 404)


def test_get_list_status_ok():
    response = requests.get(url=f'{BASE_URL}/api/unknown')
    assert (response.status_code == 200)


def test_param_get_delayed_response_status_ok():
    response = requests.get(url=f'{BASE_URL}/api/users', params={"delay": 3})
    assert (response.status_code == 200)


def test_param_get_users_data_check():
    response = requests.get(url=f'{BASE_URL}/api/users', params={"per_page": 2})
    assert(len(response.json()['data']) == 2)


def test_param_get_users_page_check():
    response = requests.get(url=f'{BASE_URL}/api/users', params={"page":1})
    assert(response.json()['page']) == 1


def test_post_register_successful():
    schema = load_schema('post_register.json')
    response = requests.post(
        url=f'{BASE_URL}/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
    })
    assert response.status_code == 200
    assert response.json()['id'] == 4
    assert response.json()['token'] == "QpwL5tke4Pnpja7X4"
    jsonschema.validate(response.json(), schema)


def test_delete_users():
    response = requests.delete(url=f'{BASE_URL}/api/users/2')
    assert(response.status_code == 204)


def test_post_create_user_successfull():
    schema = load_schema('post_create_user.json')
    response = requests.post(
        url=f'{BASE_URL}/api/users',
        json = {
            "name": "morpheus",
            "job": "leader"
    })
    jsonschema.validate(response.json(), schema)
    assert response.status_code == 201
    assert response.json()['job'] == 'leader'


def test_put_update_user():
    schema = load_schema('put_update_user.json')
    response = requests.put(
        url=f'{BASE_URL}/api/users/2',
        json = {
            "name": "zverundel",
            "job": "QA"
    })
    jsonschema.validate(response.json(), schema)
    assert response.status_code == 200
    assert response.json()['name'] == 'zverundel'


def test_patch_update_user():
    schema = load_schema('patch_update_user.json')
    response = requests.patch(
        url=f'{BASE_URL}/api/users/2',
        json = {
            "name": "zverundel",
            "job": "QA"
    })
    jsonschema.validate(response.json(), schema)
    assert response.status_code == 200
    assert response.json()['job'] == 'QA'


def test_get_list_users():
    response = requests.get(
        url=f'{BASE_URL}/api/users',
        params={"page": 2}
    )
    assert response.status_code == 200
    assert response.json()["page"] == 2


def test_get_single_existing_user():
    response = requests.get(url=f'{BASE_URL}/api/users/2')
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2


def test_get_user_not_found():
    response = requests.get(url=f'{BASE_URL}/api/users/23')
    assert response.status_code == 404


def test_get_user_schema_validation():
    schema = load_schema('get_users.json')
    response = requests.get(url=f'{BASE_URL}/api/users/2')
    assert response.status_code == 200
    jsonschema.validate(response.json(), schema)