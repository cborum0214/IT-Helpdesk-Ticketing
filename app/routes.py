from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('routes', __name__)

@bp.route('/')
@login_required
def dashboard():
    if current_user.role == 'technician':
        return render_template('technician_dashboard.html')
    else:
        return render_template('user_dashboard.html')