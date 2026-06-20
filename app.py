from flask import Flask, render_template
from config import Config
from models import db
from auth import auth
from dashboard import dashboard
from application import applications

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(applications)

@app.route('/')
def home():
    return "SmartHire backend is running! 🚀"

# ── Error handlers ────────────────────────────────────────
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)