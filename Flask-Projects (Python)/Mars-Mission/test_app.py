"""
Unit tests for the Mars Mission Flask application.
"""
import os
import pytest
from app import app, init_db, clear_test_data

DB_PATH = "data/test_db.sqlite3"

@pytest.fixture
def test_client():
    """Fixture for Flask test client."""
    app.config['TESTING'] = True
    app.config['DB_PATH'] = DB_PATH

    if not os.path.exists("data"):
        os.makedirs("data")

    init_db(testing=True)

    # clear previous test data
    clear_test_data()

    with app.test_client() as client:
        yield client

def test_add_user(test_client): # pylint: disable=redefined-outer-name
    """Test adding a new user."""
    response = test_client.post('/add', json={'name': 'Test User', 'age': 30, 'test_data': True})
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_edit_user(test_client): # pylint: disable=redefined-outer-name
    """Test editing an existing user."""
    test_client.post('/add', json={'name': 'Test User', 'age': 25, 'test_data': True})
    response = test_client.post('/edit', json={'id': 1, 'name': 'Edited Test User', 'age': 26})
    assert response.status_code == 200

def test_delete_user(test_client): # pylint: disable=redefined-outer-name
    """Test deleting a user."""
    test_client.post('/add', json={'name': 'Test User', 'age': 30, 'test_data': True})
    response = test_client.post('/delete', json={'id': 1})
    assert response.status_code == 200

def test_index_page(test_client): # pylint: disable=redefined-outer-name
    """Test the index page."""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Resource Management" in response.data

def test_api_users(test_client): # pylint: disable=redefined-outer-name
    """Test retrieving all users."""
    test_client.post('/add', json={'name': 'Test User', 'age': 30, 'test_data': True})
    response = test_client.get('/apitest/users')
    users = response.json
    assert response.status_code == 200
    assert len(users) == 1  # Only one user should be present
    assert users[0]['name'] == 'Test User'

def test_add_user_invalid_data(test_client): # pylint: disable=redefined-outer-name
    """Test adding a user with invalid data."""
    response = test_client.post('/add', json={'name': '', 'age': ''})
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid data'

def test_edit_user_invalid_data(test_client): # pylint: disable=redefined-outer-name
    """Test editing a user with invalid data."""
    response = test_client.post('/edit', json={'id': '', 'name': '', 'age': ''})
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid data'

def test_delete_user_invalid_data(test_client): # pylint: disable=redefined-outer-name
    """Test deleting a user with invalid data."""
    response = test_client.post('/delete', json={'id': ''})
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid data'
