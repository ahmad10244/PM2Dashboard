from flask import Blueprint

from controllers.auth_controller import login, logout, register


auth_bp = Blueprint('auth_bp', __name__)


auth_bp.route("/login", methods=["GET", "POST"])(login)
auth_bp.route("/logout", methods=["GET", "POST"])(logout)
auth_bp.route("/register", methods=["GET", "POST"])(register)
# auth_bp.errorhandler(403)(login)
