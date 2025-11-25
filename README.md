# Flask Weather Application (Glassmorphism UI)

## Summary
A small Flask web app that fetches current weather from OpenWeatherMap. The project demonstrates CI/CD: GitHub Actions builds, tests, and deploys to an Azure VM via SSH.

## Quick start (development)
1. Clone:
```bash
git clone <repo-url>
cd flask-weather-app
```

2. Create virtualenv & install:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set `OPENWEATHER_API_KEY`:
```sh
cp .env.example .env
```
edit .env and set OPENWEATHER_API_KEY


4. Run:

```sh
export FLASK_APP=run.py
flask run
```
or
```sh
python run.py
```

5. Open http://127.0.0.1:5000

## Tests
Run tests:

```sh
pytest -q 
```


## CI/CD
- GitHub Actions workflow is in `.github/workflows/ci-cd-deploy.yml`.
- The deployment step uses SSH and requires GitHub secrets:
  - `AZURE_HOST` (vm ip/hostname)
  - `AZURE_USER`
  - `AZURE_SSH_KEY` (private key)
  - `AZURE_DEPLOY_PATH` (e.g. `/home/azureuser/flask-weather-app`)
  - `OPENWEATHER_API_KEY` (for runtime)
- The Actions workflow will rsync the repository to the VM, ensure virtualenv & deps, and run `deploy/remote_deploy.sh`.

## Notes
- DO NOT commit real API keys to git. Use `.env` for local development and GitHub secrets for CI.



