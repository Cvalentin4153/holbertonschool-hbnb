from app.services import facade

def test_create_user():
    """Test creating a user via facade."""
    user = facade.create_user("Alice", "Johnson", "alice@example.com")
    assert user.first_name == "Alice"

    print("✅ Facade user creation test passed!")

def test_create_place():
    """Test creating a place via facade."""
    user = facade.create_user("Bob", "Smith", "bob@example.com")
    place = facade.create_place("Beach House", "A house near the beach", 200, 35.6895, 139.6917, user.id)

    assert place.title == "Beach House"
    assert place.owner == user

    print("✅ Facade place creation test passed!")

# Run tests
test_create_user()
test_create_place()
