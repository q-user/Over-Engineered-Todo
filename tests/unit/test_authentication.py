import pytest

from app.config import get_settings
from app.models.User import User
from app.routers.authentication import hash_password, create_access_token


from tests.config.stubbed_user_entries import USER_TESTING_ENTRIES


@pytest.fixture(scope="function", autouse=True)
def setup_db(db_session):
    """
    Fixture to set up the db with some test data
    """
    for entry in USER_TESTING_ENTRIES:
        db_obj = User(**entry)
        db_session.add(db_obj)
    db_session.commit()
    yield
    db_session.query(User).delete()
    db_session.commit()


def test_hash_password():
    hashed_password = hash_password("test_password")
    assert hashed_password != "test_password"


def test_create_access_token():
    from datetime import timedelta
    settings = get_settings()
    access_token = create_access_token(
        data={"sub": "test_user"},
        expires_delta=timedelta(minutes=settings.jwt_expiration_time))
    assert access_token is not None


def test_duplicate_username(client):
    new_user = {"username": "test_user_1", "password": "test_password"}
    resp = client.post("/users", json=new_user)
    assert resp.status_code == 400


def test_create_user(client):
    new_user = {"username": "test_user_3", "password": "test_password"}
    resp = client.post("/users", json=new_user)
    assert resp.status_code == 201


def test_token_invalid_user(client):
    new_user = {"username": "test_user_3", "password": "test_password"}
    resp = client.post("/users", json=new_user)
    assert resp.status_code == 201

    new_user = {"username": "test_user_3", "password": "invalid"}
    resp = client.post("/token", data=new_user)
    assert resp.status_code == 401

    new_user = {"username": "invalid_username", "password": "test_password"}
    resp = client.post("/token", data=new_user)
    assert resp.status_code == 401


def test_valid_token_endpoint(client):
    new_user = {"username": "test_user_3", "password": "test_password"}
    resp = client.post("/users", json=new_user)
    assert resp.status_code == 201

    resp = client.post("/token", data=new_user)
    assert resp.status_code == 200
    assert resp.json()["access_token"] is not None
    assert resp.json()["token_type"] == "bearer"
