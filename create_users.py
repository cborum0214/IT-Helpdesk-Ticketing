from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

# Create tables
db.create_all()

# Create users
tech = User(username='tech1', role='technician')
tech.set_password('pass123')

user = User(username='user1', role='user')
user.set_password('pass123')

db.session.add_all([tech, user])
db.session.commit()

print("Sample users created!")
