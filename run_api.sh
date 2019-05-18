# source myappenv/bin/activate
gunicorn api:app --bind 0.0.0.0:8080 --access-logfile logging/access.log --error-logfile logging/error.log --timeout 30 --workers=1