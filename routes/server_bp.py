from flask import Blueprint

from controllers.server_controller import show_server_pm2_processes, reload_server_pm2_processes


server_bp = Blueprint("server_bp", __name__)

server_bp.route("/show", methods=["GET"])(show_server_pm2_processes)
server_bp.route("/reload", methods=["GET"])(reload_server_pm2_processes)
