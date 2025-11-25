#!/usr/bin/env bash
# remote_deploy.sh - run on the server to update and restart app
set -e

# ensure python3.12-venv is installed
sudo apt update -y
sudo apt install -y python3.12-venv

APP_DIR="$1" # e.g. /home/azureuser/flask-weather-app
VENV_DIR="$APP_DIR/venv"

if [ -z "$APP_DIR" ]; then
    echo "Usage: $0 /path/to/app"
    exit 2
fi

cd "$APP_DIR"

# If not present, create venv
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv venv
fi

# check if gunicorn is installed, if not install it
source "$VENV_DIR/bin/activate"
if ! pip show gunicorn > /dev/null 2>&1; then
    pip install gunicorn
fi

# activate and install requirements
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

# ensure .env is present; CI should copy it or set variables in systemd
# Restart the systemd service if exists else do a background run (example)
if systemctl --user --quiet status flask-weather.service; then
    systemctl --user restart flask-weather.service
    echo "Restarted flask-weather.service (user systemd)."
else
    # fallback: kill existing and launch with nohup (simple)
    pkill -f "gunicorn" || true
    nohup venv/bin/gunicorn --bind 0.0.0.0:5000 "run:app" > gunicorn.log 2>&1 &
    echo "Launched gunicorn in background."
fi
