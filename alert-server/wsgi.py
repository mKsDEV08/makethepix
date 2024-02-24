import sys
sys.path.append("../")

import json
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit

from helpers import Alerts, create_message
from connector import User, session

app = Flask(__name__)
io = SocketIO(app)

@app.route('/alerts/<alert_id>', methods=['GET', 'POST'])
def index(alert_id):
    if request.method == 'GET':
        results = session.query(User).filter(User.alert_id == alert_id)
        list_users = []
        for r in results:
            list_users.append(r)

        if list_users == []:
            return Response("404. Alert_id not found!", status=404)

        io.on_namespace(Alerts(f"/alerts/{alert_id}"))
        return render_template("scripts.html", alert_id = alert_id)

    elif request.method == 'POST':
        results = session.query(User).filter(User.alert_id == alert_id)
        list_users = []
        for r in results:
            list_users.append(r)

        if list_users == []:
            return Response("404. Alert_id not found!", status=404)
        
        request_json = request.data
        request_json = json.loads(request_json.decode('UTF-8'))

        message_id = request_json.get("message_id")
        validation_hash = request_json.get("validation_hash")

        if not message_id:
            return Response("400. Bad request!", status=400)
        
        if not validation_hash:
            return Response("400. Bad request!", status=400)

        psw_hash = session.query(User.password_hash).filter(User.alert_id == alert_id)
        if psw_hash[0][0] != validation_hash:
            return Response("401. UNAUTHORIZED!", status=401)
        
        data = create_message(message_id, alert_id)

        io.on_namespace(Alerts(f"/alerts/{alert_id}"))
        emit('new_message', data, broadcast=True, namespace=f'/alerts/{alert_id}')
        return Response("200. OK message sent!", status=200)

if __name__ == '__main__':
    io.run(debug=True, app=app, host='0.0.0.0')