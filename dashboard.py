# dashboard.py — SmartHire Dashboard Routes

from flask import Blueprint, render_template, session, redirect, url_for
from models import db, Application
from functools import wraps

dashboard = Blueprint('dashboard', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@dashboard.route('/dashboard')
@login_required
def index():
    user_id = session['user_id']
    applications = Application.query.filter_by(user_id=user_id).order_by(Application.created_at.desc()).all()

    stats = {
        'total':     len(applications),
        'applied':   sum(1 for a in applications if a.status == 'Applied'),
        'interview': sum(1 for a in applications if a.status == 'Interview'),
        'offer':     sum(1 for a in applications if a.status == 'Offer'),
        'rejected':  sum(1 for a in applications if a.status == 'Rejected'),
    }

    return render_template('dashboard.html',
                           applications=applications,
                           stats=stats,
                           user_name=session.get('user_name', 'there'))

@dashboard.route('/keyword-matcher/<int:app_id>')
@login_required
def keyword_matcher(app_id):
    app = Application.query.filter_by(id=app_id, user_id=session['user_id']).first_or_404()
    return render_template('keyword_matcher.html', app=app)