[![Build Status](https://travis-ci.com/PaulinhoNdegwa/Store-Manager-API.svg?branch=develop)](https://travis-ci.com/PaulinhoNdegwa/Store-Manager-API)
[![Coverage Status](https://coveralls.io/repos/github/PaulinhoNdegwa/Store-Manager-API/badge.svg?branch=develop)](https://coveralls.io/github/PaulinhoNdegwa/Store-Manager-API?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/8cfedb70e884468b7496/maintainability)](https://codeclimate.com/github/PaulinhoNdegwa/Store-Manager-API/maintainability)

# Store-Manager-API

One Paragraph of project description goes here

## Getting Started

This project involves building a Store Manager app that is a RESTful API that will help a store owner and store attendants manage their store

### Features Included:

1. Store admin can create other app users
2. Store owner/admin can signin/signout
3. Store admin can create, update and delete products
4. Store attendant can add sales
5. Store owner/attendant can view single users
6. Store attendant can view all sales
7. Store owner can view all users

### Installing

Clone the repository [```here```](https://github.com/PaulinhoNdegwa/Store-Manager-API) or 

```$ git clone https://github.com/PaulinhoNdegwa/Store-Manager-API.git ```

cd into Store-Manager-API

Create a virtual environment

```$ virtualenv venv -p python3 ```

Activate Virtual Environment

```$ source venv/bin/activate ```

Install project dependencies 


```$ pip install -r requirements.txt```

#### Running the application

```$ python run.py ```



#### Testing

```$  pytest --cov=app ```


## Authors

* **Paul Gichuki** - *Initial work* - [PaulinhoNdegwa](https://github.com/PaulinhoNdegwa)


## Acknowledgments

* Thanks to everyone who helped in the development of this project
