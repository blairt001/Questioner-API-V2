[![Build Status](https://travis-ci.org/blairt001/Questioner-API-V2.svg?branch=develop)](https://travis-ci.org/blairt001/Questioner-API-V2)
[![Coverage Status](https://coveralls.io/repos/github/blairt001/Questioner-API-V2/badge.svg?branch=develop)](https://coveralls.io/github/blairt001/Questioner-API-V2?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/f8860af9cd43ffc71066/maintainability)](https://codeclimate.com/github/blairt001/Questioner-API-V2/maintainability)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Questioner-API-V2

Questioner is a crowd-source questions for a meetup. It helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or to the bottom of the log.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Git
* Python 3.6.7
* Virtualenv

### Quick Start

1. Clone the repository

```
$ git clone https://github.com/blairt001/Questioner-API-V2.git
$ cd into the created folder
```
  
2. Initialize and activate a virtualenv

```
$ virtualenv --no-site-packages venv
$ source venv/bin/activate
```

3. Install the dependencies

```
$ pip install -r requirements.txt
```

4. Initialize environment variables

```
$ export SECRET_KEY=<SECRET KEY>
$ export TESTING_DATABASE_URI=<URI>
$ export DEVELOPMENT_DATABASE_URI=<URI>
```

5. Run the development server

```
$ python manage.py
```

5. Navigate to [http://localhost:5000](http://localhost:5000)

At the / endpoint you should see Welcome to Questioner-API-V2 displayed in your browser.

## Endpoints

Here is a list of all endpoints in the Questioner-API-V2

| **HTTP METHOD** | **URI ** | **ACTION** |
| --- | --- | --- |
| **POST** | `/api/v2/auth/login` | Login a user |
| **POST** | `/api/v2/auth/Signup` | Sign Up a user |
| **POST** | `/api/v2/auth/logout` | Logout a user |
| **GET** | `/api/v2/profile` | View user profile |
| **POST** | `/api/v2/meetups` | Create a meetup record |
| **DELETE** | `/api/v2/meetups/<int:meetup_id>` | Delete a meetup record |
| **POST** | `/api/v2/questions` | Post a question to a specific meetup record |
| **GET** | `/api/v2/meetups/<int:meet_id>/questions` | Get all questions on a meetup record |
| **POST** | `/api/v2/questions/<int:question_id>/comment` | Comment on a question |
| **GET** | `/api/v2/questions/<int:question_id>/comments` | Get all comments on a question |
| **GET** | `/api/v2/meetups/upcoming` | Fetch all upcoming meetups records |
| **GET** | `/api/v2/meetups/<int:meetup_id>` | Fetch a specific meetup |
| **POST** | `/api/v2/meetups/<int:meetup_id>/rsvps/<resp>` | RSVP to a meetup |
| **PATCH** | `/api/v2/questions/<int:question_id>/upvote` | Upvote a question |
| **PATCH** | `/api/v2/questions/<int:question_id>/downvote` | Downvote a question |

## Running the tests

To run the automated tests simply run

```
pytest
```

### And coding style tests

Coding styles tests are tests that ensure conformity to coding style guides. In our case, they test conformity to
PEP 8 style guides

```
pylint manage.py
```

## Deployment

Ensure you use ProductionConfig settings which have DEBUG set to False

## Built With

* HTML5
* CSS3
* Python 3.6.4
* Flask - The web framework used

## GitHub pages

https://blairt001.github.io/Questioner/UI/

## Heroku

https://questionerv2-blair-heroku.herokuapp.com/

## Sample Tasks

https://www.pivotaltracker.com/n/projects/2235680

## Versioning

Most recent version is version 2

## Authors

Tony Blair

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/blairt001/Questioner-API-V2/blob/develop/LICENSE) file for details

## Credits
[Andela Kenya](https://andela.com/)

## Acknowledgments

* Thanks to anyone who assisted in one way or the other