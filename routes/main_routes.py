from flask import Blueprint, render_template, url_for
from config import Config

main_bp = Blueprint('main', __name__)

# Default ERD filename for display
erd_filename = "default_erd.png"

@main_bp.route("/")
def home():
    """Home page route"""
    return render_template("index.html", erd_image=url_for('static', filename=erd_filename))