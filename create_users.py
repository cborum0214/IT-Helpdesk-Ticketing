from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

# Create tables
db.create_all()

# Create users
admin = User(username='tech1', role='technician')
admin.set_password('pass123')

user = User(username='user1', role='user')
user.set_password('pass123')

db.session.add(admin)
db.session.add(user)
db.session.commit()

print("Users created!")
