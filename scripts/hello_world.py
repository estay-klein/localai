#!/usr/bin/env python3
"""
Example script for Supervisord.
This script runs indefinitely, printing a heartbeat every 10 seconds.
"""

import time
import sys
import os

def main():
    script_name = os.path.basename(__file__)
    pid = os.getpid()
    print(f"[{script_name}] Started with PID {pid}", flush=True)
    
    counter = 0
    try:
        while True:
            print(f"[{script_name}] Heartbeat #{counter} at {time.ctime()}", flush=True)
            counter += 1
            time.sleep(10)
    except KeyboardInterrupt:
        print(f"[{script_name}] Interrupted, shutting down", flush=True)
        sys.exit(0)

if __name__ == "__main__":
    main()