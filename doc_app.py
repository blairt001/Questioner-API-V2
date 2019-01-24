"""Contain interactive documentation to help one get started using the API
"""
import os

from flasgger import Swagger

from app import create_app


app = create_app('config.ProductionConfig')
swagger = Swagger(app)


{
  "swagger": "2.0",
  "info": {
    "version": "1.0",
    "title": "Questioner-API-V2 Docs",
    "description": "Questioner is a crowd-source questions for a meetup. It helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or to the bottom of the log.",
    "contact": {}
  },
  "host": "127.0.0.1:5000",
  "basePath": "/api/v2",
  "schemes": [
    "http"
  ],
  "consumes": [
    "application/json"
  ],
  "produces": [
    "application/json"
  ],
  "paths": {
    "/meetups/": {
      "post": {
        "description": "Create Meetups",
        "summary": "http://127.0.0.1:5000/api/v2/meetups",
        "tags": [
          "meetups"
        ],
        "operationId": "MeetupsPost",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "Content-Type",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "Body",
            "in": "body",
            "required": true,
            "description": "",
            "schema": {
              "$ref": "#/definitions/http:~1~1127.0.0.1:5000~1api~1v2~1meetupsRequest"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/meetups/upcoming": {
      "get": {
        "description": "Get all meetups",
        "summary": "http://127.0.0.1:5000/api/v2/meetups/upcoming",
        "tags": [
          "meetups"
        ],
        "operationId": "MeetupsUpcomingGet",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/meetups/3": {
      "get": {
        "description": "Get specific meetup",
        "summary": "http://127.0.0.1:5000/api/v2/meetups/3",
        "tags": [
          "meetups"
        ],
        "operationId": "Meetups3Get",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/meetups/4": {
      "delete": {
        "description": "Admin Delete Meetup",
        "summary": "http://127.0.0.1:5000/api/v2/meetups/4",
        "tags": [
          "meetups"
        ],
        "operationId": "Meetups4Delete",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/meetups/3/rsvps/yes": {
      "post": {
        "description": "User rsvp to a meetup",
        "summary": "http://127.0.0.1:5000/api/v2/meetups/3/rsvps/yes",
        "tags": [
          "meetups"
        ],
        "operationId": "Meetups3RsvpsYesPost",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "Content-Type",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "Body",
            "in": "body",
            "required": true,
            "description": "",
            "schema": {
              "type": "array",
              "items": {
                "$ref": "#/definitions/http:~1~1127.0.0.1:5000~1api~1v2~1meetups~13~1rsvps~1yesRequest"
              }
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/meetups/3/questions": {
      "post": {
        "description": "Post a question to a meetup record",
        "summary": "http://127.0.0.1:5000/api/v2/meetups/3/questions",
        "tags": [
          "questions"
        ],
        "operationId": "Meetups3QuestionsPost",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "Content-Type",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "Body",
            "in": "body",
            "required": true,
            "description": "",
            "schema": {
              "$ref": "#/definitions/http:~1~1127.0.0.1:5000~1api~1v2~1meetups~13~1questionsRequest"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      },
      "get": {
        "description": "Get all questions",
        "summary": "http://127.0.0.1:5000/api/v2/meetups/3/questions",
        "tags": [
          "questions"
        ],
        "operationId": "Meetups3QuestionsGet",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/questions/1/comment": {
      "post": {
        "description": "User Comment on a Question",
        "summary": "http://127.0.0.1:5000/api/v2/questions/1/comment",
        "tags": [
          "questions"
        ],
        "operationId": "Questions1CommentPost",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "Content-Type",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "Body",
            "in": "body",
            "required": true,
            "description": "",
            "schema": {
              "$ref": "#/definitions/http:~1~1127.0.0.1:5000~1api~1v2~1questions~11~1commentRequest"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/questions/1/comments": {
      "get": {
        "description": "User Get all comments",
        "summary": "http://127.0.0.1:5000/api/v2/questions/1/comments",
        "tags": [
          "questions"
        ],
        "operationId": "Questions1CommentsGet",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/questions/1/upvote": {
      "patch": {
        "description": "User Upvote A Question",
        "summary": "http://127.0.0.1:5000/api/v2/questions/1/upvote",
        "tags": [
          "questions"
        ],
        "operationId": "Questions1UpvotePatch",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/questions/2/downvote/": {
      "patch": {
        "description": "User Downvote a question",
        "summary": "http://127.0.0.1:5000/api/v2/questions/2/downvote/",
        "tags": [
          "questions"
        ],
        "operationId": "Questions2DownvotePatch",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/auth/signup": {
      "post": {
        "description": "Sign up user",
        "summary": "http://127.0.0.1:5000/api/v2/auth/signup",
        "tags": [
          "users"
        ],
        "operationId": "AuthSignupPost",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "Content-Type",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "Body",
            "in": "body",
            "required": true,
            "description": "",
            "schema": {
              "$ref": "#/definitions/http:~1~1127.0.0.1:5000~1api~1v2~1auth~1signupRequest"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/auth/login": {
      "post": {
        "description": "Log in user",
        "summary": "http://127.0.0.1:5000/api/v2/auth/login",
        "tags": [
          "users"
        ],
        "operationId": "AuthLoginPost",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "Content-Type",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "Body",
            "in": "body",
            "required": true,
            "description": "",
            "schema": {
              "$ref": "#/definitions/http:~1~1127.0.0.1:5000~1api~1v2~1auth~1loginRequest"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    },
    "/auth/logout": {
      "post": {
        "description": "User Logout",
        "summary": "http://127.0.0.1:5000/api/v2/auth/logout?x-access-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZha2VhZG1pbiJ9.3JCgD2AMcZTKUsKWrwAq--gomRcsh2is-HbtVHa6HTs",
        "tags": [
          "users"
        ],
        "operationId": "AuthLogoutPost",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "x-access-token",
            "in": "query",
            "required": true,
            "type": "string",
            "description": ""
          },
          {
            "name": "x-access-token",
            "in": "header",
            "required": true,
            "type": "string",
            "description": ""
          }
        ],
        "responses": {
          "200": {
            "description": "",
            "headers": {}
          }
        }
      }
    }
  },
  "definitions": {
    "http://127.0.0.1:5000/api/v2/meetupsRequest": {
      "title": "http://127.0.0.1:5000/api/v2/meetupsRequest",
      "example": {
        "topic": "Scrum",
        "happenningon": "14/02/2019",
        "location": "Thika",
        "images": "blair.png",
        "tags": "Tech"
      },
      "type": "object",
      "properties": {
        "topic": {
          "type": "string"
        },
        "happenningon": {
          "type": "string"
        },
        "location": {
          "type": "string"
        },
        "images": {
          "type": "string"
        },
        "tags": {
          "type": "string"
        }
      },
      "required": [
        "topic",
        "happenningon",
        "location",
        "images",
        "tags"
      ]
    },
    "http://127.0.0.1:5000/api/v2/meetups/Request1": {
      "title": "http://127.0.0.1:5000/api/v2/meetups/Request1",
      "example": {
        "topic": "Miguel Miguel",
        "happenningon": "16/02/2019",
        "location": "Nairobi",
        "images": "Miguel.png",
        "tags": [
          "Tech"
        ]
      },
      "type": "object",
      "properties": {
        "topic": {
          "type": "string"
        },
        "happenningon": {
          "type": "string"
        },
        "location": {
          "type": "string"
        },
        "images": {
          "type": "string"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "required": [
        "topic",
        "happenningon",
        "location",
        "images",
        "tags"
      ]
    },
    "http://127.0.0.1:5000/api/v2/meetups/3/rsvps/yesRequest": {
      "title": "http://127.0.0.1:5000/api/v2/meetups/3/rsvps/yesRequest",
      "example": {
        "Attending": "yes",
        "meetup": 1,
        "topic": "Scrum"
      },
      "type": "object",
      "properties": {
        "Attending": {
          "example": "yes",
          "type": "string"
        },
        "meetup": {
          "example": 1,
          "type": "integer",
          "format": "int32"
        },
        "topic": {
          "example": "Scrum",
          "type": "string"
        }
      },
      "required": [
        "Attending",
        "meetup",
        "topic"
      ]
    },
    "http://127.0.0.1:5000/api/v2/meetups/3/questionsRequest": {
      "title": "http://127.0.0.1:5000/api/v2/meetups/3/questionsRequest",
      "example": {
        "title": "What is Dev?",
        "body": "I really like how people talk about Tonys Dev"
      },
      "type": "object",
      "properties": {
        "title": {
          "type": "string"
        },
        "body": {
          "type": "string"
        }
      },
      "required": [
        "title",
        "body"
      ]
    },
    "http://127.0.0.1:5000/api/v2/questions/1/commentRequest": {
      "title": "http://127.0.0.1:5000/api/v2/questions/1/commentRequest",
      "example": {
        "comment": "Wow, I love every topic on Dev"
      },
      "type": "object",
      "properties": {
        "comment": {
          "type": "string"
        }
      },
      "required": [
        "comment"
      ]
    },
    "http://127.0.0.1:5000/api/v2/auth/signupRequest": {
      "title": "http://127.0.0.1:5000/api/v2/auth/signupRequest",
      "example": {
        "firstname": "Tony",
        "lastname": "Andela",
        "phoneNumber": "0713403687",
        "username": "fakeadmin",
        "email": "blairtdev@gmail.com",
        "password": "Blairman1234",
        "confirm_password": "Blairman1234"
      },
      "type": "object",
      "properties": {
        "firstname": {
          "type": "string"
        },
        "lastname": {
          "type": "string"
        },
        "phoneNumber": {
          "type": "string"
        },
        "username": {
          "type": "string"
        },
        "email": {
          "type": "string"
        },
        "password": {
          "type": "string"
        },
        "confirm_password": {
          "type": "string"
        }
      },
      "required": [
        "firstname",
        "lastname",
        "phoneNumber",
        "username",
        "email",
        "password",
        "confirm_password"
      ]
    },
    "http://127.0.0.1:5000/api/v2/auth/loginRequest": {
      "title": "http://127.0.0.1:5000/api/v2/auth/loginRequest",
      "example": {
        "username": "fakeadmin",
        "password": "Blairman1234"
      },
      "type": "object",
      "properties": {
        "username": {
          "type": "string"
        },
        "password": {
          "type": "string"
        }
      },
      "required": [
        "username",
        "password"
      ]
    }
  },
  "tags": [
    {
      "name": "meetups",
      "description": "Contains all meetups API Endpoints"
    },
    {
      "name": "questions",
      "description": "Contain all questions API Endpoints"
    },
    {
      "name": "comments",
      "description": "Contain all comments API Endpoints"
    },
    {
      "name": "users",
      "description": "contain all users API Endpoints"
    }
  ]
}