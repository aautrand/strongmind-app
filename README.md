# Alan's Pizza Place
## Strongmind App
This is a python application using the flask framework to handle both backend and server side rendering of the ui. Both, the Postgres database and the application itself, are hosted in heroku.


### Running locally
To run the application locally follow these steps:
1. add database uri to SQLALCHEMY_DATABASE_URI environment variable:
   1. e.g.: export SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host:port/db
2. pip install -r requirements.txt
3. run the 'make run' command

### Running Tests
Tests can be run locally via:
1. make tests
2. pytest .

Backend testing can also be done via Postman by following either of these two options: 
1. https://red-crescent-714490.postman.co/workspace/strongmind~2be69919-fc14-424d-ab98-fd8bf968786a/collection/7146013-828bacfd-3d5a-467b-8aa7-caf82840c746?action=share&creator=7146013
2. using the postman collection json file included in this repository. 
   1. local environment variable host = 120.0.0.1:5000
   2. production environment variable host = https://strongmind-test-07-11-761945a49865.herokuapp.com

Due to time constraints I couldn't set up FE testing using selenium.

### Deploy Application
To deploy the application use:

_**make deploy**_

Note:
To deploy the application, one must first have the following items configured
* heroku cli 
* a repository 
* a database

This post has good instructions on for the steps above: 
https://blog.back4app.com/deploying-a-flask-app-on-heroku/

-----
## Requirements

* It should describe steps required for building and running locally
* It should describe how to run tests locally

### Manage Toppings

As a pizza store owner I should be able to manage toppings available for my pizza chefs.
* It should allow me to see a list of available toppings
* It should allow me to add a new topping
* It should allow me to delete an existing topping
* It should allow me to update an existing topping
* It should not allow me to enter duplicate toppings

### Manage Pizzas

As a pizza chef I should be able to create new pizza masterpieces
* It should allow me to see a list of existing pizzas and their toppings
* It should allow me to create a new pizza and add toppings to it
* It should allow me to delete an existing pizza
* It should allow me to update an existing pizza
* It should allow me to update toppings on an existing pizza
* It should not allow me to enter duplicate pizzas
