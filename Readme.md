# My First Flask APP from scratch 

## Consideration 

The project is not very much flasky, because I have just maintain a flask project some months ago. So, I just put my best foot forward to layout a greate structure with places for improvement and also be more flasky. 

## TODO
There are some todo commands showing my perspective for project shortcommings, consider this is not very clean project.

## Permissions in Project 

The permission handling should be completely changed in the project but I just get it running and working correctly. 


## New starter 

This project needs some time and effort to be a starter-kit for flask project. 

## Why not Django 

Using django serializers and the greate generic views allows handling this project in less than a day, however, I prefer to take some challenges and start it from scratch. 

# Run 
 Prepare a python environment and install requirements/base.txt
 
 To run the project first you need the migrations:
 ```
 flask db init 
 flask db migrate -m "Initial Migration"
 flask db upgrade 
 ```
 To run the project:
 ```
 python -m flask run 
 ```
 
To test users views:
```
pytest apps/users/tests.py
```

## Documentation 
There is a postman json in the project root, import and enjoy.