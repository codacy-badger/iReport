[![Maintainability](https://api.codeclimate.com/v1/badges/3082a200ffdd74f93384/maintainability)](https://codeclimate.com/github/natalie-abbie/iReport/maintainability)
# IReporter

The iReporter api enables users to register and login to the platform with their correct creditials inorder to report a redf flag or an intervention in line with corruption

## Built with

To get started for the coding you will need to 
* install Flask as our major dependence, 
* pep8 for neat and professional codes,
* pylint to help you around with a few of the errors. 
* python 3.6 as the version to be used. 

### Installation

Here is how to go about installing of the requirements that will be need 
* We shall need to work in a virtual environment so lets go ahead and;
Create a virtual environment for linux users
```
 virtualenv "name of the virtual environment eg venv" (virtualenv venv)
 ```
Then when the virtual environmemt is created, Activate the environment

```
    source "name of the virtual environment eg venv/bin/activate" (source venv/bin/activate)
 ```
 In your Vscode you therefore get to realise its in brackets eg (venv)nataline.......... and when all this is done get to your application directorty if already pushed to github by cloning the repo 
 
 ```
 git clone https://github.com/natalie-abbie/iReport.git 
 cd to the application directory eg cd iReport
 incase its in the branch git checkout branchname
 ```
 After all the dependences are installed in your virtualenv therefore run the command to put the depences in the in the requirements.txt file 
 ```
 pip install >requirements.txt 
 and to install the dependences again run the below command in your terminal to install all the dependences
 pip install -r rewuirements.txt
 ```
 Run the application with:
 ```
 python app/app.py
 ```

## Running the tests

For running the tests you can either use;
```
pytest
Nose2
test_filename
```

### URL ENDPOINTS for v1 api

| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `api/v1/redflag/<flag_id>` | `GET` | Retrieves a specific redflag by id 
| `/api/v1/redflag'` | `GET` | Gets all the red flags created by the users
| `api/v1/users` | `GET` | Retrieve all users |
| `api/v1/register | `POST` |  registers a new User |
| `api/v1/login` | `POST` |  Logs in a registered user |
| `api/v1/redflag/<flag_id>/location`|`PUT`| Changes the location of a specific  user
| `api/v1/redflag/<flag_id>/description` | `PUT` | changes the description of a specific user |
| `api/v1/redflag/<flag_id>`|`DELETE`| deletes the red of a specific user|
| `api/v1/logout` | `POST` |  Logs out a user |

### USER
An example of how its posted in postman
```
{
     'user_id':uuid.uuid1(),
      "firstname": "firstname",
      "lastname": "lastname",
      "othernames": "othernames",
      "email": "email",
      password": "password"
}
```
### CREATE REDFLAGS
An example of how its posted in postman
```
{
       "flag_id":uuid.uuid4(),
        "location": "location",
        "type": "type",
        "description": "description",
        "image": "image",
        "video" : "video",
        str(dt.utcnow()) : "created_on",
        "created_by" : "created_by"
       }
```
### RESULT IN POSTMAN 
```
[
    "'status': 201",
    {
        "data": [
            {
                "2018-12-21 23:39:04.922320": "Fri, 21 Dec 2018 23:39:04 GMT",
                "created_by": "opio",
                "description": "a mummy carried out child violence",
                "flag_id": "bc0e0bdd-c01e-4d88-8d0c-75b4cf64b7b7",
                "image": "image",
                "location": "kisaasi",
                "type": "violence",
                "video": "video"
            }
        ],
        "message": "redflag created"
    }
]
```

## Versioning
```
/api/v1/.....
```

## Authors
Natalie Abbie 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

