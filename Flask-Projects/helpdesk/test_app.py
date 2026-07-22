import pytest
from app import app, db, Resource

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 🧩 Βάση στη μνήμη για tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_resource(client):
    response = client.post('/resources', json={'name': 'Oxygen', 'quantity': 10})
    assert response.status_code == 201  # ✅ Ελέγχει αν η δημιουργία ήταν επιτυχής
