[![Build Status](https://travis-ci.org/reuseman/GoOutSafe.svg?branch=main)](https://travis-ci.org/reuseman/GoOutSafe) [![Coverage Status](https://coveralls.io/repos/github/reuseman/GoOutSafe/badge.svg?branch=main)](https://coveralls.io/github/reuseman/GoOutSafe?branch=main) [![Requirements Status](https://requires.io/github/reuseman/GoOutSafe/requirements.svg?branch=main)](https://requires.io/github/reuseman/GoOutSafe/requirements/?branch=main)

# Getting started

## Development
### Local
    # Install Dependencies
    pip install -r requirements/dev.txt

    # Start Server mail
    python -m smtpd -n -c DebuggingServer localhost:8025
    # Start Redis
    docker run --name redis -p 6379:6379 redis
    # Start Celery
    celery -A gooutsafe.celery worker -l DEBUG -E -B
    
    # Deploy
    flask deploy

    # Run Flask
    export FLASK_APP="monolith:create_app('development')" 
    FLASK_ENV=development
    flask run

### Generate mock data
    flask shell
    mock.everything()

### Tests with coverage
Inside GoOutSafe run (it will automatically use the configuration in pyproject.toml):

    pytest

If you want to see an interactive report run:

    coverage html

## Production (beta)
### Docker
    docker build -t gooutsafe:latest . 

To run with settings

    docker run --name gooutsafe -d -p 8000:5000 --rm -e SECRET_KEY=my-secret-key \
        -e MAIL_SERVER=smtp.gmail.com -e MAIL_PORT=587 -e MAIL_USE_TLS=1 \
        -e MAIL_USERNAME=<your-gmail-username> -e MAIL_PASSWORD=<your-gmail-password> \ gooutsafe:latest

To run without settings

    docker run --name gooutsafe -d -p 8000:5000 --rm gooutsafe:latest

Go to

    http://127.0.0.1:5000


## Documentation
### User stories
![](docs/user-stories.png)

### E-R Diagram in PlantUML
![](docs/plantUML-er.png)