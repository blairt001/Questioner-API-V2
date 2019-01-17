# Questioner-API-V2
[![Build Status](https://travis-ci.org/blairt001/Questioner-API-V2.svg?branch=develop)](https://travis-ci.org/blairt001/Questioner-API-V2)[![Coverage Status](https://coveralls.io/repos/github/blairt001/Questioner-API-V2/badge.png?branch=develop)](https://coveralls.io/github/blairt001/Questioner-API-V2?branch=develop)[![Maintainability](https://api.codeclimate.com/v1/badges/f8860af9cd43ffc71066/maintainability)](https://codeclimate.com/github/blairt001/Questioner-API-V2/maintainability)


## Heroku Hosting Link

> **[Click Here](https://questionerv2-blair-heroku.herokuapp.com/)**

#  Sample Tasks
 
 >  **[Pivotal Tracker Board Stories](https://www.pivotaltracker.com/n/projects/2235680)**

# Project Overview
Questioner is a crowd-source questions for a meetup. It helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or to the bottom of the log.

## Questioner-API-V2 Endpoints

| Method        |       Endpoint                              |         Description                           |
| ------------- |       -------------                         |         -------------                         |
| `GET`         | `/api/v2/meetups/upcoming`                  |   Gets all meetups records                    |
| `GET`         | `/api/v2/meetups/<meetup-id>`               |   Get a specific meetup record                |
| `POST`        | `/api/v2/meetups`                           |   Create a meetup record                      |
| `POST`        | `/api/v2/questions`                         |   Create a question record                    |
| `POST`        | `/api/v2/users/registration`                |   Register a user                             |
| `POST`        | `/api/v2/users/login`                       |   Sign in a User                              |
| `POST`        | `/api/v2/meetups/<meetup-id/rsvps>`         |   User respond to a meetup                    |
| `PATCH`       | `/api/v2/questions/<questions-id>/upvote`   |   vote on a meetup question                   |
| `PATCH`       | `/api/v2/questions/<questions-id/downvote`  |   vote on a meetup question                   |



# Setting up your system

Install [python](https://www.python.org/downloads/)

# Getting Started

Clone the repository :

`git clone  https://github.com/blairt001/Questioner-API-V2.git`

cd into the repository

Activate virtualenv: `source venv/bin/activate`


## Install requirements.txt

```
pip install -r requirements.txt
```

## Running the Application

Follow the following procedures:

```
export  FLASK_ENV="development"
```

```
export FLASK_APP="manage.py"
```
 
 ```
export APP_SETTINGS="development"
 ```

```
python manage.py runserver
```

## Unit Testing
 On the terminal execute `pytest`

## Testing API Endpoints:
Use [Postman](https://www.getpostman.com/downloads/)

## License
[MIT LICENSE](https://github.com/blairt001/Questioner-API-V2/blob/develop/LICENSE)

## Credits
[Andela Kenya](https://andela.com/)

## Developer
Tony B.
