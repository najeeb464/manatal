# Manatal Test
- School and student  are the two models use in studentcms app.
- All the GET api are open any one can access them
- POST,PUT,PATCH and DELTE method endpoints wil work only for autheticated user.
### Stack
- Django
- Django REST framework
- Postgres Database
- Git 
- Heroku (Deployment)
## Project url:
https://manatalcms.herokuapp.com/
For Admin dasboard
https://manatalcms.herokuapp.com/admin./

### Initial Setup
Install the dependencies and devDependencies and start the server.
```sh
 pip install --user pipenv
 pipenv shell
 clone git repo
 pipenv run pip install -r requirements.txt
 git clone https://github.com/najeeb464/manatal.git
 cd  studentcms
```
create .env file in the root directory (where manage.py file is present) and assign value to the variable listed below
```sh
SECRET_KEY
DEBUG
DATABASE_NAME
DATABASE_USER
DATABASE_PASS
DATABASE_HOST
DATABASE_PORT
```
```sh
python manage.py migrate
 python manage.py initial_data
 python manage.py runserver
 ```
 when you run initial_data along with school and student dummy data user data also created.use can login in your admin pannel or deployed site admin pannel using bellow mentioned credentials 
 - Username : test
 - Email:     test@gmail.com
 - Password:  123456

## EndPoints
### School
##### List and Create
##
### Api
Local environment:
```sh
GET || POST 
127.0.0.1:8000/school/
```
Production environment:
```sh
GET || POST
https://manatalcms.herokuapp.com/schools/
```

| Parameter | Type   | GET | POST (required)  |Filter(GET)|
| ------ | ------ |----| ---- |---|
| id | integer |&check;|  &check;| |
| name | string |&check;|&check;|&check;|
|  max_student_limit |Positive Integer |&check;|&check;|&check;|
| city | string |&check;||&check;|
| state | string | &check;||&check;|
| zip_code | string|&check;| |&check;|
| address | string |&check;||&check;|
| phone | string |&check;||&check;|
| fax | string |&check;||&check;|
```sh
Allowed Methods
GET || PUT || PATCH || DELTE
https://manatalcms.herokuapp.com/schools/:pk/
```
- pk(primary key ) is required in url pattern 
- In below listings table 
- For GET request the listed parameter return
- For PUT, PATCH, DELETE request the checked parameter require and blank and crossed parameter are not required

# 

| Parameter | Type   | GET | PUT |PATCH|DELETE|
| ------ | ------ |----| ---- |---|---|
| id | integer |&check;| | |&cross;|
| name | string |&check;|&check;||&cross;|
|  max_student_limit |Positive Integer |&check;|&check;||&cross;|
| city | string |&check;||||&cross;|
| state | string | &check;|||&cross;|
| zip_code | string|&check;| ||&cross;|
| address | string |&check;|||&cross;|
| phone | string |&check;|||&cross;|
| fax | string |&check;|||&cross;|

# Student
API
List and create 
Local environment:
```sh
GET || POST 
http://127.0.0.1:8000/school/1/student/
```
Production environment:
```sh
GET || POST
http://127.0.0.1:8000/schools/:id/students/

https://manatalcms.herokuapp.com/schools/<school_pk>/students/
```
| Parameter | Type   | GET | POST (required)  |Filter(GET)|
| ------ | ------ |----| ---- |---|
| id | integer |&check;|  &check;| |
| first_name | string |&check;|&check;|&check;|
|  last_name |string |&check;|&check;|&check;|
| dob | date |&check;|&check;|&check;|
|  gender |string (choice fields) |&check;||&check;|
| auto_gen_identification | bool |&check;|[NoteA]|&check;|
|  identification |string |&check;|[NOTE A]|&check;|
| city | string |&check;||&check;|
| state | string | &check;||&check;|
| zip_code | string|&check;| |&check;|
| address | string |&check;||&check;|
| phone | string |&check;||&check;|
| fax | string |&check;||&check;|

###### NOTE A:
- If user select auto_gen_identification student registration number is genereated -  automatically and identification fields is not required in this case
- If auto_gen_identification is not selected then identification fields is required.
### Detail Apis
using this end point you can get detail of particular student ,update and delete student instance
```sh
Allowed Methods
GET || PUT || PATCH || DELTE
127.0.0.1:8000/schools/:school_pk/students/:pk/
```
Production
```sh
Allowed Methods
GET || PUT || PATCH || DELTE
https://manatalcms.herokuapp.com/schools/<school_pk>/students/:pk/
```

| Parameter | Type   | GET | PUT |PATCH  | DELETE|
| ------ | ------ |----| ---- |---|--|
| id | integer |&check;| | |
| first_name | string |&check;|&check;|
|  last_name |string |&check;|&check;|
| dob | date |&check;|&check;||
|  gender |string (choice fields) |&check;|||
| auto_gen_identification | bool |&check;|readonly||
|  identification |string |&check;|readonly ||
| city | string |&check;|||
| state | string | &check;|||
| zip_code | string|&check;| ||
| address | string |&check;|||
| phone | string |&check;|||
| fax | string |&check;|||


# Task Expectation 


|--- | Expected | Done | Remaining|
|---| ------ | ------ |----|
|Model Serializer|&check;|&check;||
|Nested Router|&check;|&check;||
|ModelViewSet|&check;|&check;|
|Heroku Deployment|&check;|&check;||
|Filters|&check;|&check;||
|Pagination|&check;|&check;|
|Factory Boy ( faker) |&check;|&check;|
|Factory Boy ( faker) |&check;|&check;|
|Postgre DB|&check;|&check;|
|Pipenv|&check;|&check;|
|.env|&check;|&check;|
|Api Test Cases|||Partially done
|Custimized Admin Pannel (added search and add custum student form)||&check;| 
|Command to load initial data||&check;




