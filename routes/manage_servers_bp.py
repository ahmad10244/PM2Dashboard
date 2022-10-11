from flask import Blueprint

from controllers.manage_servers_controller import create_server, edit_server, delete_server, get_server


manage_servers_bp = Blueprint("manage_servers_bp", __name__)

manage_servers_bp.route("/create", methods=["POST"])(create_server)
manage_servers_bp.route("/delete", methods=["GET"])(delete_server)
manage_servers_bp.route("/edit", methods=["POST"])(edit_server)
manage_servers_bp.route("/get", methods=["GET"])(get_server)
