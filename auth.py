# auth.py — SmartHire Authentication Routes
 
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
 
auth = Blueprint('auth', __name__)
 
 
# ── Signup ────────────────────────────────────────────────
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name     = request.form.get('first_name', '').strip()
        last_name      = request.form.get('last_name', '').strip()
        email          = request.form.get('email', '').strip().lower()
        password       = request.form.get('password', '')
        confirm_pw     = request.form.get('confirm_password', '')
 
        # ── Basic validation ───────────────────────────────
        if not all([first_name, last_name, email, password]):
            flash('All fields are required.', 'error')
            return render_template('signup.html')
 
        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('signup.html')
 
        if password != confirm_pw:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')
 
        # ── Check duplicate email ──────────────────────────
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('An account with that email already exists.', 'error')
            return render_template('signup.html')
 
        # ── Create user ────────────────────────────────────
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
 
        flash('Account created! Please sign in.', 'success')
        return redirect(url_for('auth.login'))
 
    return render_template('signup.html')
 
 
# ── Login ─────────────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
 
        user = User.query.filter_by(email=email).first()
 
        if not user or not check_password_hash(user.password_hash, password):
            flash('Incorrect email or password.', 'error')
            return render_template('login.html')
 
        # ── Store session ──────────────────────────────────
        session.permanent = remember
        session['user_id']   = user.id
        session['user_name'] = user.first_name
 
        return redirect(url_for('dashboard.index'))
 
    return render_template('login.html')
 
 
# ── Logout ────────────────────────────────────────────────
@auth.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out.", 'success')
    return redirect(url_for('auth.login'))