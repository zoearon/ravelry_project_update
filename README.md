

Loose Threads is an app to promote and prompt users to update their knitting project pages. The user's projects are collected from the popular knitting site, Ravelry. The user is alerted upon returning to the site about how many projects have not been updated in a given number of days. They can then get details on their projects and update the project. Their updates are saved in both loose threads and on the corresponding Ravelry page. Users also can subscribe to text alerts reminding them weekly about how many projects need to be updated.

## Table of Contents

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [To-Do](#future)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML, Javascript, jQuery, Chart.js, Bootstrap, CSS <br/>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy, Pillow, schedule,  <br/>
__APIs:__ Ravelry, Twilio <br/>

## <a name="features"></a>Features 📽

Log in to see your current projects.

![Log In](/static/img/_readme-img/LoginPage.jpeg)
![User Information](/static/img/_readme-img/user.png)
<br/><br/><br/>
Sort projects by status and see how many projects need to be updated
  
![Projects](/static/img/_readme-img/projectsPage.jpeg)
<br/><br/><br/>
View the details of a project and update the project page
  
![Project Details](/static/img/_readme-img/projectDetails.jpg)
![Update Project](/static/img/_readme-img/updateProjects.jpeg)
<br/><br/><br/>
Subscribe to reminders for your projects
  
![Schedule Reminder](/static/img/_readme-img/userOptions.png)

## <a name="installation"></a>Setup/Installation ⌨️

####Requirements:

- PostgreSQL
- Python 2.7
- Ravelry and Twilio API keys

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/zoearon/ravelry_project_update.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install requirements🔗:
```
$ pip install -r requirements.txt
```
Get your own secret keys for [Ravelry](https://www.ravelry.com/groups/ravelry-api) and [Twilio](https://www.twilio.com/doers). Save them to a file `secrets.sh`. Your file should look something like this:
```
export APP_KEY = 'xyz'
export RAVELRY_SECRET_KEY = 'abc'
export RAVELRY_PERSONAL_KEY = 'abc'
export TWILIO_SID = 'abc'
export TWILIO_TOKEN = 'abc'
```
Create database 'projects'.
```
$ createdb projects
```
Create your database tables and seed🌱 example data.
```
$ python model.py
$ python seed.py
```
Run the app from the command line.
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i model.py
```

## <a name="future"></a>TODO✨
* Refactor with REACT
* Add OAuth for more users
* Add more ways to remind users
* more encryption on the user data

