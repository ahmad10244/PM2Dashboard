import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask_login import login_required, current_user

from config import Development, Production


app = Flask(__name__)
app.config.from_object(Development if os.getenv("FLASK_DEBUG") == '1' else Production)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.user import User
from models.server import Server

from routes.server_bp import server_bp
from routes.manage_servers_bp import manage_servers_bp
from routes.auth_bp import auth_bp


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(manage_servers_bp, url_prefix="/manage/servers")
app.register_blueprint(server_bp, url_prefix="/server")


@app.before_first_request
def admin_register():
    if len(User.query.all()) == 0:
        app.config["FIRST_STARTUP"] = True


@app.route("/")
@login_required
def home():
    servers_list = Server.query.order_by(Server.id.asc()).all()
    return render_template('index.html', current_user=current_user, servers_list=servers_list)
