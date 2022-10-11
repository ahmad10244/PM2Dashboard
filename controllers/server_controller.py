from cmath import log
import logging
import requests
from enum import Enum
from datetime import datetime
from flask_login import login_required, current_user
from flask import flash, request, render_template, url_for, redirect

from models.server import Server


class Routes(Enum):
    PM2_LIST = "/process/list"


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


@login_required
def show_server_pm2_processes():
    refresh_interval = request.args.get("refresh_interval", None)
    server_id = request.args.get("id")
    server_url = Server.find_by_id(server_id).url
    server_name = Server.find_by_id(server_id).name

    try:
        pm2_process_list = get_server_process_list(server_url)
        # Convert uptime timestamp to human readable string
        list(map(lambda x: x['pm2_env'].update({
            "pm_uptime": human_delta(datetime.now() - datetime.fromtimestamp(x['pm2_env']['pm_uptime']/1000)) if x['pm2_env']['status'] == 'online' else 0
        }), pm2_process_list))

        return render_template(
            'server.html',
            pm2_process_list=pm2_process_list,
            server_id=server_id,
            server_name=server_name,
            refresh_interval=refresh_interval,
            lastUpdate=datetime.now().strftime("%Y-%m-%d %H:%m:%S")
        )
    except Exception as ex:
        logging.exception(ex)
        flash("An Error occurred.", 'error')
        return redirect(url_for("home"))


def reload_server_pm2_processes():
    """
     Reload function to use for htmx refresh process list table
    """

    if not current_user.is_authenticated:
        return "", 204

    server_id = request.args.get("id")
    server_url = Server.find_by_id(server_id).url

    try:
        pm2_process_list = get_server_process_list(server_url)
        # Convert uptime timestamp to human readable string
        list(map(lambda x: x['pm2_env'].update({
            "pm_uptime": human_delta(datetime.now() - datetime.fromtimestamp(x['pm2_env']['pm_uptime']/1000)) if x['pm2_env']['status'] == 'online' else 0
        }), pm2_process_list))


        # Return lastUpdate span and table rows html string to use in htmx 
        ret_html = f"""
        <span class="d-block m-t-5" id="lastUpdate">Last Update: {datetime.now().strftime("%Y-%m-%d %H:%m:%S")} </span>
        <table>
        <tbody id="pm2ListTbody"> 
        """
        for process in pm2_process_list:
            ret_html += f"""
            <tr>
                <td>{ process.get('pm_id', '') }</td>
                <td>{ process.get('name', '') }</td>
                <td>{ process['pm2_env'].get('namespace', '') }</td>
                <td>{ process['pm2_env'].get('version', '') }</td>
                <td>{ process['pm2_env'].get('exec_mode', '') }</td>
                <td>{ process.get('pid', '') }</td>
                <td>{ process['pm2_env'].get('pm_uptime', '') }</td>
                <td>{ process['pm2_env'].get('restart_time', '') }</td>
                <td>
                    <h5><span class="badge badge-{'success' if process['pm2_env'].get('status', '') == 'online' else 'danger'}">{process['pm2_env'].get('status', '') }</span></h5>
                </td>
                <td>{ process['pm2_env'].get('username', '') }</td>
                <td>{ process['pm2_env'].get('watch', '') }</td>
            </tr>
            """
        ret_html += "</tbody></table>"

        return ret_html
    except Exception as ex:
        logging.exception(ex)
        return ""
