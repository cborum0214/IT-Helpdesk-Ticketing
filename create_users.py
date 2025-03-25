from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

# Create tables
db.create_all()

# Create users
tech = User(username='cborum', role='technician')
tech.set_password('0d8pwDfO')

user = User(username='student', role='user')
user.set_password('student')

db.session.add_all([tech, user])
db.session.commit()

print("Sample users created!")
