import json
import os
import subprocess
import sys

import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, _):
    print("========== Connected ========== ", sid)


# Start / Stop music
@sio.event
def start_face(_):
    global process
    print("========== Started music ==========")
    with open("running.stat", "w") as f:
        f.write("Face")


@sio.event
def stop_face(_):
    print("========== Stopped music ==========")
    with open("running.stat", "w") as f:
        f.write("False")
    with open("score.stat", "r") as f:
        score = f.read()
        sio.emit("score", score)


# Send/receive plan
@sio.event
def get_plans(_):
    print("========== Get plans ==========")
    with open("res/plan.json", "r") as f:
        content = json.load(f)
        sio.emit("receivePlans", json.dumps(content))


@sio.event
def save_plans(_, plans):
    print("========== Save plans =========")

    loaded_plans = json.loads(plans)
    with open("res/plan.json", "w") as f:
        json.dump(loaded_plans, f, indent=4)


@sio.event
def start_barcode(_):
    print("========== Start scanning barcode ==========")

    with open("running.stat", "w") as f:
        f.write("Barcode")
    
    
@sio.event
def stop_barcode(_):
    print("========== Stop scanning barcode ==========")

    with open("running.stat", "w"):
        f.write("False")


@sio.event
def disconnect(sid):
    print("========== Disconnected ========== ", sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 8000)), app)
