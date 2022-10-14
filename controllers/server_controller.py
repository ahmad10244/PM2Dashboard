import time
import logging
import requests
from enum import Enum
from datetime import datetime
from flask_login import login_required, current_user
from jinja2 import Environment, PackageLoader, select_autoescape
from flask import flash, request, render_template, url_for, redirect

from models.server import Server


class Routes(Enum):
    PM2_LIST = "/process/list"
    PM2_ACTION = "/process/{action}"


def human_delta(tdelta):
    d = dict(days=tdelta.days)
    d['hrs'], rem = divmod(tdelta.seconds, 3600)
    d['min'], d['sec'] = divmod(rem, 60)

    fmt = ''
    if d['days'] != 0:
        fmt += '{days} day '
    if d['hrs'] != 0:
        fmt += '{hrs} hr '
    if d['min'] != 0:
        fmt += '{min} min '
    if d['sec'] != 0 and d['min'] == 0:
        fmt += '{sec} sec'

    return fmt.format(**d)


def get_server_process_list(url: str) -> list:
    re = requests.get(url + Routes.PM2_LIST.value)

    if re.status_code != 200:
        raise Exception(f"Status Code: {re.status_code}")

    return re.json()


def pm2_process_action(server_url: str, action: str, process_name: str):
    """

    """
    if action == "start":
        re = requests.post(server_url + Routes.PM2_ACTION.value.format(action=action),
                           json={"name": process_name})
    elif action == "delete":
        re = requests.delete(server_url + Routes.PM2_ACTION.value.format(action=action),
                          params={"processName": process_name})
    else:
        re = requests.put(server_url + Routes.PM2_ACTION.value.format(action=action),
                          params={"processName": process_name})

    if re.status_code != 200:
        raise Exception(f"Status Code: {re.status_code}")


def create_pm2_processes_list_html_table(server_id: int) -> str:
    """
        Create html table from pm2 process list got from api.
        The output is used to refresh server pm2 process list table using htmx (https://htmx.org/).

        :param pm2_process_list: Server processes list
        :return: PM2 processes list html table string
    """
    server_url = Server.find_by_id(server_id).url
    pm2_process_list = get_server_process_list(server_url)

    # Convert uptime timestamp to human readable string
    list(map(lambda x: x['pm2_env'].update({
        "pm_uptime": human_delta(datetime.now() - datetime.fromtimestamp(x['pm2_env']['pm_uptime']/1000)) if x['pm2_env']['status'] == 'online' else 0
    }), pm2_process_list))

    # Return pm2 processes html table card string to use in htmx
    env = Environment(
        loader=PackageLoader("app"),
        autoescape=select_autoescape()
    )
    template = env.get_template("pm2_processes_table.html")
    action_url = url_for('server_bp.server_pm2_process_action', id=server_id)
    ret_html = template.render(last_update=datetime.now().strftime("%Y-%m-%d %H:%m:%S"),
                               pm2_process_list=pm2_process_list,
                               action_url=action_url)

    return ret_html


@login_required
def show_server_pm2_processes():
    refresh_interval = request.args.get("refresh_interval", None)
    server_id = request.args.get("id")

    try:
        server_url = Server.find_by_id(server_id).url
        server_name = Server.find_by_id(server_id).name

        pm2_process_list = get_server_process_list(server_url)
        action_url = url_for('server_bp.server_pm2_process_action', id=server_id)

        # Convert uptime timestamp to human readable string
        list(map(lambda x: x['pm2_env'].update({
            "pm_uptime": human_delta(datetime.now() - datetime.fromtimestamp(x['pm2_env']['pm_uptime']/1000)) if x['pm2_env']['status'] == 'online' else 0
        }), pm2_process_list))

        return render_template(
            'server.html',
            **{
                "pm2_process_list": pm2_process_list,
                "server_id": server_id,
                "server_name": server_name,
                "refresh_interval": refresh_interval,
                "lastUpdate": datetime.now().strftime("%Y-%m-%d %H:%m:%S"),
                "action_url": action_url
            }
        )
    except Exception as ex:
        logging.exception(ex)
        flash("An Error occurred.", 'error')
        return redirect(url_for("home"))


def reload_server_pm2_processes():
    """
        Reload function to use for htmx (https://htmx.org/) to refresh pm2 processes list table.
    """

    if not current_user.is_authenticated:
        return "", 204

    server_id = request.args.get("id")
    try:
        time.sleep(1)
        return create_pm2_processes_list_html_table(server_id)
    except Exception as ex:
        logging.exception(ex)
        return ""


@login_required
def server_pm2_process_action():
    server_id = request.args.get("id")
    action = request.args.get("action")
    process_name = request.args.get("pname")
    try:
        server_url = Server.find_by_id(server_id).url
        pm2_process_action(server_url, action, process_name)
        
        time.sleep(1)
        return create_pm2_processes_list_html_table(server_id)
    except Exception as ex:
        logging.exception(ex)
        flash(f"Failed to {action} <b>{process_name}</b>", 'error')
        return ""
