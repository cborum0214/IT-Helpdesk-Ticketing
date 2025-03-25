from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import TicketForm
from app.models import db, Ticket, Comment, User
from datetime import datetime

bp = Blueprint('routes', __name__)

# Dashboard redirect
@bp.route('/')
@login_required
def dashboard():
    if current_user.role == 'technician':
        status = request.args.get('status')
        assigned_to = request.args.get('assigned_to')
        sort = request.args.get('sort', 'desc')

        query = Ticket.query

        if status:
            query = query.filter_by(status=status)

        if assigned_to:
            if assigned_to == 'unassigned':
                query = query.filter_by(technician_id=None)
            else:
                query = query.filter_by(technician_id=int(assigned_to))

        if sort == 'asc':
            query = query.order_by(Ticket.updated_at.asc())
        else:
            query = query.order_by(Ticket.updated_at.desc())

        tickets = query.all()
        technicians = User.query.filter_by(role='technician').all()

        return render_template('technician_dashboard.html', tickets=tickets, technicians=technicians)

    else:
        # User dashboard
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.created_at.desc()).all()
        return render_template('user_dashboard.html', tickets=tickets)

# Submit ticket (users only)
@bp.route('/ticket/new', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if current_user.role != 'user':
        flash("Only users can submit tickets.")
        return redirect(url_for('routes.dashboard'))

    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket submitted successfully.")
        return redirect(url_for('routes.dashboard'))
    
    return render_template('create_ticket.html', form=form)

# View ticket details
@bp.route('/ticket/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role == 'user' and ticket.user_id != current_user.id:
        flash("You don't have permission to view this ticket.")
        return redirect(url_for('routes.dashboard'))

    comments = ticket.comments.order_by(Comment.created_at).all()

    # Get all technicians for the assign dropdown
    technicians = User.query.filter_by(role='technician').all()

    return render_template('ticket_detail.html', ticket=ticket, comments=comments, technicians=technicians)

# Update ticket status (technicians only)
@bp.route('/ticket/<int:ticket_id>/update', methods=['POST'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if current_user.role != 'technician':
        flash("Only technicians can update tickets.")
        return redirect(url_for('routes.dashboard'))

    # Get status from form
    new_status = request.form.get("status")
    new_tech_id = request.form.get("technician_id")

    if new_status:
        ticket.status = new_status

    if new_tech_id:
        ticket.technician_id = int(new_tech_id)

    db.session.commit()
    flash("Ticket updated.")
    return redirect(url_for('routes.view_ticket', ticket_id=ticket.id))

# Add comment
@bp.route('/ticket/<int:ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # Check access
    if current_user.role == 'user' and ticket.user_id != current_user.id:
        flash("You can't comment on this ticket.")
        return redirect(url_for('routes.dashboard'))

    comment_text = request.form.get("comment")
    if comment_text:
        comment = Comment(
            ticket_id=ticket.id,
            user_id=current_user.id,
            comment_text=comment_text,
            created_at=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment added.")
    
    return redirect(url_for('routes.view_ticket', ticket_id=ticket.id))
