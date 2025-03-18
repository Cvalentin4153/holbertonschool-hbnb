from app.__init__ import create_app
from extensions import db
from flask_migrate import upgrade

app = create_app()

with app.app_context():
    # Apply any pending migrations
    upgrade()

if __name__ == '__main__':
    app.run(debug=True, port=5001)