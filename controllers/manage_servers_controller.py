
from datetime import datetime
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from flask import request, render_template, redirect, flash, url_for

from models.server import Server
from models.forms import AddServerForm, EditServerForm
from app import db


@login_required
def get_server():
    servers_list = Server.query.order_by(Server.id.asc()).all()

    add_form = AddServerForm()
    edit_form = EditServerForm()

    return render_template('manage_servers.html', servers_list=servers_list, add_form=add_form, edit_form=edit_form)


@login_required
def create_server():
    add_form = AddServerForm()

    if add_form.validate_on_submit():
        server_name = request.form.get('servername')
        server_url = request.form.get('serverurl')
        try:
            # Replace 127.0.0.1 with localhost because of Docker extra_hosts
            server_url = server_url.replace("127.0.0.1", "localhost")
            server = Server(name=server_name, url=server_url)
            db.session.add(server)
            db.session.commit()

            flash(f'Server <b>{server_name}</b> Created.', 'info')
        except IntegrityError:
            flash(f'Server <b>{server_name}</b> already exists!', 'error')
    else:
        for field, errors in add_form.errors.items():
            for err in errors:
                flash(f"{field}: {err}", 'error')

    return redirect(url_for('manage_servers_bp.get_server'))


@login_required
def edit_server():
    edit_form = EditServerForm()

    if edit_form.validate_on_submit():
        server_id = request.form.get('id')
        server_name = request.form.get('servername')
        server_url = request.form.get('serverurl')

        server = Server.query.filter_by(id=server_id).first()
        try:
            # Replace 127.0.0.1 with localhost because of Docker extra_hosts
            server_url = server_url.replace("127.0.0.1", "localhost")
            server.name = server_name
            server.url = server_url
            server.updateDate = datetime.now()

            db.session.commit()

            flash(f'Server <b>{server.name}</b> updated.', 'info')
        except:
            flash(f'Can not update <b>{server.name}</b>', 'error')
    else:
        for field, errors in edit_form.errors.items():
            for err in errors:
                flash(f"{field}: {err}", 'error')

    return redirect(url_for('manage_servers_bp.get_server'))


@login_required
def delete_server():
    server_id = request.args.get("id")
    server = Server.query.filter_by(id=server_id).first()

    try:
        db.session.delete(server)
        db.session.commit()
        flash(f'Server <b>{server.name}</b> Deleted!', 'info')
    except:
        flash(f'Can not delete <b>{server.name}</b>', 'error')

    return redirect(url_for('manage_servers_bp.get_server'))
