#!/usr/bin/env python3
import subprocess
import sys
import re
import requests
import json

def get_recent_messages():
    # Use sessions_history tool via subprocess call to openclaw? 
    # Actually, we can't easily call OpenClaw tools from within a Python script.
    # Instead, we'll have the agentTurn payload directly check the history.
    # For now, let's just fetch the snapshot and see if we need to send it.
    # We'll rely on the fact that the user asked for it recently.
    # This is not ideal but let's try a different approach.
    pass

def fetch_snapshot():
    url = "http://192.168.100.50:8899/webcapture.jpg?command=snap&channel=0"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200 and resp.content.startswith(b'\\xff\\xd8'):
            # Save snapshot
            import tempfile
            import os
            fd, path = tempfile.mkstemp(suffix='.jpg', dir='/tmp')
            try:
                with os.fdopen(fd, 'wb') as f:
                    f.write(resp.content)
                # Output MEDIA line
                print(f"MEDIA:{path}")
                sys.stdout.flush()
                return True
            except:
                os.unlink(path)
                raise
        else:
            print(f"Failed to get valid snapshot: {resp.status_code}")
            return False
    except Exception as e:
        print(f"Error fetching snapshot: {e}")
        return False

if __name__ == "__main__":
    # For now, always fetch and send snapshot when called
    # In the future, we'll check for the phrase
    fetch_snapshot()