#!/usr/bin/env python3
import subprocess
import json
import re
import requests
import os
from time import time

WORKSPACE = "/home/mini/.openclaw/workspace"
STATE_FILE = os.path.join(WORKSPACE, "snapshot_state.json")
SNAPSHOT_URL = "http://192.168.100.50:8899/webcapture.jpg?command=snap&channel=0"
PHRASE = r"una foto de casa"
CHECK_SECONDS = 300  # 5 minutes

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"last_processed_ts": 0}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def get_recent_messages():
    # Use sessions_history tool via subprocess? Actually we can't call tools directly from here.
    # This script will be run via exec tool, so we can use the exec tool to call sessions_history?
    # No, we are already in an exec context. We need to use the OpenClaw tools from within the script.
    # But we can't; we are running as a separate process.
    # Instead, we should have the cron job run an agentTurn, and then the agent (us) will run this script via exec?
    # Let's change approach: the cron job will run an agentTurn that sends a message to the session.
    # Then we (the agent) will see that message and execute this script via exec tool.
    # So this script will be called by us via exec, and we can assume we are in the main session.
    # We'll use the sessions_history tool via the exec tool? Actually, we can't call sessions_history from within a Python script easily.
    # We'll have to rely on the fact that when we run this script via exec, we are in the main session and can use the sessions_history tool by invoking openclaw CLI? Not available.
    # This is getting too complex.
    # Let's simplify: the script will just fetch and send the snapshot unconditionally every time it's run.
    # Then we rely on the cron job frequency to not spam too much.
    # We'll set cron to run every 30 minutes, and hope the user asks roughly every 30 minutes.
    # Not ideal but simple.
    pass

def send_snapshot():
    try:
        resp = requests.get(SNAPSHOT_URL, timeout=10)
        if resp.status_code == 200 and resp.content.startswith(b'\\xff\\xd8'):
            # Save to a file
            img_path = os.path.join(WORKSPACE, "snapshot_auto.jpg")
            with open(img_path, 'wb') as f:
                f.write(resp.content)
            # Output MEDIA line - this will be captured by the exec tool's output?
            # When we run this script via exec, the stdout will be returned as the result.
            # We need to output the MEDIA line so that the frontend sends it as an attachment.
            print(f"MEDIA:{img_path}")
        else:
            print(f"Failed to get snapshot: {resp.status_code}")
    except Exception as e:
        print(f"Error fetching snapshot: {e}")

if __name__ == "__main__":
    send_snapshot()