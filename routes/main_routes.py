from flask import Blueprint, render_template, url_for
from config import Config

main_bp = Blueprint('main', __name__)

# Default ERD filename for display
erd_filename = "default_erd.png"

@main_bp.route("/")
def home():
    """Home page route - redirect to login if not authenticated"""
    return render_template("login.html")

@main_bp.route("/search")
def search():
    """ERD search page (original functionality)"""
    return render_template("index.html", erd_image=url_for('static', filename=f'image/{erd_filename}'))

@main_bp.route("/login")
def login():
    """Login page"""
    return render_template("login.html")

@main_bp.route("/register")
def register():
    """Register page"""
    return render_template("register.html")

@main_bp.route("/user-dashboard")
def user_dashboard():
    """User dashboard"""
    return render_template("user_dashboard.html")

@main_bp.route("/advisor-dashboard")
def advisor_dashboard():
    """Advisor dashboard"""
    return render_template("advisor_dashboard.html")

@main_bp.route("/admin-dashboard")
def admin_dashboard():
    """Admin dashboard"""
    return render_template("admin_dashboard.html")
