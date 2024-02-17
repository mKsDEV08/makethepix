import json
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
from helpers import Alerts, TextToSpeech, db, create_message

app = Flask(__name__)
io = SocketIO(app)

@app.route('/alerts/<alert_id>', methods=['GET', 'POST'])
def index(alert_id):
    if request.method == 'GET':
        db.execute("SELECT * FROM users WHERE alert_id = %s", (alert_id,))
        if db.fetchall() == []:
            return Response("404. Alert_id not found!", status=404)

        io.on_namespace(Alerts(f"/alerts/{alert_id}"))
        return render_template("scripts.html", alert_id = alert_id)

    elif request.method == 'POST':
        db.execute("SELECT * FROM users WHERE alert_id = %s", (alert_id,))
        if db.fetchall() == []:
            return Response("404. Alert_id not found!", status=404)
        
        request_json = request.data
        request_json = json.loads(request_json.decode('UTF-8'))

        message_id = request_json.get("message_id")
        validation_hash = request_json.get("validation_hash")

        if not message_id:
            return Response("400. Bad request!", status=400)
        
        if not validation_hash:
            return Response("400. Bad request!", status=400)

        db.execute("SELECT password_hash FROM users WHERE alert_id = %s", (alert_id,))
        if db.fetchall()[0][0] != validation_hash:
            return Response("401. UNAUTHORIZED!", status=401)
        
        data = create_message(db, message_id, alert_id)

        io.on_namespace(Alerts(f"/alerts/{alert_id}"))
        emit('new_message', data, broadcast=True, namespace=f'/alerts/{alert_id}')
        return Response("200. OK message sent!", status=200)

if __name__ == '__main__':
    io.run(debug=True, app=app, host='0.0.0.0')