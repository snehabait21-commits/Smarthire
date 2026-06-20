# application.py — SmartHire Application CRUD Routes

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Application
from datetime import datetime
from functools import wraps

applications = Blueprint('applications', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ── Add Application ───────────────────────────────────────
@applications.route('/application/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        company         = request.form.get('company', '').strip()
        role            = request.form.get('role', '').strip()
        status          = request.form.get('status', 'Applied')
        date_applied    = request.form.get('date_applied', '')
        job_description = request.form.get('job_description', '').strip()
        notes           = request.form.get('notes', '').strip()

        if not company or not role:
            flash('Company and Role are required.', 'error')
            return render_template('add_application.html')

        # Limit input length
        if len(company) > 150 or len(role) > 150:
            flash('Company and Role must be under 150 characters.', 'error')
            return render_template('add_application.html')

        if status not in ['Applied', 'Interview', 'Offer', 'Rejected']:
            status = 'Applied'

        new_app = Application(
            user_id         = session['user_id'],
            company         = company,
            role            = role,
            status          = status,
            date_applied    = datetime.strptime(date_applied, '%Y-%m-%d').date() if date_applied else datetime.utcnow().date(),
            job_description = job_description,
            notes           = notes
        )
        db.session.add(new_app)
        db.session.commit()

        flash(f'Application to {company} added successfully!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('add_application.html')


# ── Edit Application ──────────────────────────────────────
@applications.route('/application/edit/<int:app_id>', methods=['GET', 'POST'])
@login_required
def edit(app_id):
    app = Application.query.filter_by(id=app_id, user_id=session['user_id']).first_or_404()

    if request.method == 'POST':
        company  = request.form.get('company', '').strip()
        role     = request.form.get('role', '').strip()
        status   = request.form.get('status', 'Applied')

        if not company or not role:
            flash('Company and Role are required.', 'error')
            return render_template('add_application.html', app=app)

        if len(company) > 150 or len(role) > 150:
            flash('Company and Role must be under 150 characters.', 'error')
            return render_template('add_application.html', app=app)

        if status not in ['Applied', 'Interview', 'Offer', 'Rejected']:
            status = 'Applied'

        app.company         = company
        app.role            = role
        app.status          = status
        app.job_description = request.form.get('job_description', '').strip()
        app.notes           = request.form.get('notes', '').strip()
        date_applied        = request.form.get('date_applied', '')

        if date_applied:
            app.date_applied = datetime.strptime(date_applied, '%Y-%m-%d').date()

        db.session.commit()
        flash('Application updated successfully!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('add_application.html', app=app)


# ── Delete Application ────────────────────────────────────
@applications.route('/application/delete/<int:app_id>')
@login_required
def delete(app_id):
    app = Application.query.filter_by(id=app_id, user_id=session['user_id']).first_or_404()
    db.session.delete(app)
    db.session.commit()
    flash('Application deleted.', 'success')
    return redirect(url_for('dashboard.index'))