from app import create_app
from app.services import facade
from config import config

app = create_app(config['development'])

with app.app_context():
    # Create admin user
    try:
        admin = facade.create_user(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="admin123",
            is_admin=True
        )
        print(f"Admin user created successfully with ID: {admin.id}")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}") 