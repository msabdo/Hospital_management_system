# Hospital_management_system
This project is a simple Hospital management system . 

This project use auth0 to make login and authorization process.
You can use this like to make login and get the token for three 
different users accounts:
###### Admin, Doctor, Patient
You can use this link to login and sign up:
```
https://eng-auth.us.auth0.com/authorize?
  response_type=token&
  audience=Hospital_API&
  client_id=9qEgXjlryoHlWQDtIRHgLNTRbRvzPtfh&
  redirect_uri=http://localhost:5000/&
  state=STATE
```
You can use this link to logout:   

     https://eng-auth.us.auth0.com/v2/logout?federated

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── auth.py *** the file containt the authorization process ***
  ├── models.py *** the file contain the postgres model***
  ├── test_app.py *** the file containt the test operations by unit-test lib ***
  ```

###End points
- Get '/patients'
- Get '/patient/<int:id>'
- Post '/patient'
- Put '/patient/<int:id>'
- Delete '/patient\<int:id>'
- Get '/doctors'
- Get '/doctor/<int:id>'
- Post '/doctor'
- Put '/doctor/<int:id>'
- Delete '/doctor/<int:id>'

#####Get '/patients'
 - Fetch all patients data 
 - returns
 ````
 {
    "patients": [
        {
            "address": "Cairo-Egypt",
            "age": 50,
            "doctor": {
                "email": "doctor2@example.com",
                "name": "doctor2"
            },
            "email": "patient60@example.com",
            "examine_report": "cancer ",
            "id": 45,
            "name": "patient60"
        }
    ],
    "success": true
}
````

#####Get '/patient/<int:id>'
 - Fetch patient data by id
 - returns:
 ````
 {
            "address": "Cairo-Egypt",
            "age": 50,
            "doctor": {
                "email": "doctor2@example.com",
                "name": "doctor2"
            },
            "email": "patient60@example.com",
            "examine_report": "cancer ",
            "id": 45,
            "name": "patient60"
        }
````
#####Post '/patient'
- Create new patient
- request:
````
{
    "name": "patient3",
    "age": 50,
    "address": "Cairo-Egypt",
    "email": "patient3@example.com",
    "examine_report": "cancer ",
    "doctor_id": 8
}
````
#####Put '/patient/<int:id>'
- Update patient data
- request:
````
{

    "name": "patient3",
    "age": 50,
    "address": "Cairo-Egypt",
    "email": "patient3@example.com",
    "examine_report": "cancer ",
    "doctor_id": 8
}
````
##### Delete '/patient\<int:id>'
- Delete patient data


##### Get '/doctors'
 -Fetch all doctors data 
 - returns:
 ````
{
    "doctors": [
        {
            "address": "Cairo-Egypt",
            "email": "doctor2@example.com",
            "id": 8,
            "name": "doctor2",
            "salary": 2000
        },
        {
            "address": "Alex-Egypt",
            "email": "doctor3@example.com",
            "id": 9,
            "name": "doctor3",
            "salary": 3000
        },
    ],
    "success": true
}
````
  
#####Get '/doctor/<int:id>'
- Fetch doctor data by id
- returns:
````
{
    {
        "address": "Alex-Egypt",
        "email": "doctor3@example.com",
        "id": 9,
        "name": "doctor3",
        "salary": 3000
    },
    "success": true
}
````
#####Post '/doctor'
- Create new doctor 
- request:
````
{
    "address": "Alex-Egypt",
    "email": "doctor3@example.com",
    "name": "doctor3",
    "salary": 3000
}
````
#####Put '/doctor/<int:id>'
- Update doctor data
- request:
````
{
    "address": "Alex-Egypt",
    "email": "doctor3@example.com",
    "name": "doctor3",
    "salary": 3000
}
````

#####Delete '/doctor/<int:id>'
- Delete doctor