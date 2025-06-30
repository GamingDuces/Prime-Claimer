# Prime Claimer Backend

## Setup

1. `pip install -r requirements.txt`
2. `.env.example` kopieren zu `.env`
3. `python -m playwright install`
4. `gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --workers 4`
