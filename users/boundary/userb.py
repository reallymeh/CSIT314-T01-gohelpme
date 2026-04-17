from users.entity.user import User
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

# flask integration
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/homepage') # url will be .../user/homepage
def homepage():
    return render_template('HomePage.html')