from jinja2 import StrictUndefined

from flask import Flask, jsonify,render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Project, Status, Image
import datetime
import tracker
import requests
import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "secret"

# Raise error if undefine Jinja variable
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ View homepage """

    # session['user'] = 463097
    return render_template("homepage.html")

@app.route('/user')
def view_profile():
    """ view user profile page """

    # check if there is a current user
    if 'user' not in session:
        return redirect("/login")

    # query for current user
    user = User.query.get(int(session['user']))

    return render_template("user.html", user=user)


@app.route('/logout')
def logout():
    """ log out user from the session """

    # remove any users from the session
    session.clear()

    # redirect back to login
    return redirect('/login')

@app.route('/login', methods=['GET'])
def login():
    """ show the login form """

    # render login page
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def check_user():
    """ log the user in """

    # get the user name from the post form
    user = request.form.get("username")
    # tracker.check_username(user)

    # query for any users with that username
    active_user = User.query.filter_by(username = user).first()

    # if there is a matching user
    if active_user:
        flash( "Login Successful")
        session['user'] = active_user.user_id
        return redirect('/user')
    # if there is not a user with that username
    else:
        flash("Login Failed")
        return redirect('/login')

    

@app.route('/projects')
def view_projects():
    """ View the current users projects """

    # Get finished projects
    fin_projects = db.session.query(Project).join(Status).filter(
               Project.user_id == session['user'],
               Status.status == "Finished").all()

    # Get hibernating projects
    hib_projects = db.session.query(Project).join(Status).filter(
               Project.user_id == session['user'],
               Status.status == "Hibernating").all()

    # Get frogged projects
    frog_projects = db.session.query(Project).join(Status).filter(
               Project.user_id == session['user'],
               Status.status == "Frogged").all()

    # Get the projects for the current user and are in progress
    wip_projects = db.session.query(Project).join(Status).filter(
               Project.user_id == session['user'],
               Status.status == "In progress").order_by(Project.updated_at).all()

    # sort the in progress projects into 2 groups based on update needs
    need_update, updated = tracker.sort_projects_by_update(wip_projects)

    projects_by_type = {"finished": fin_projects,
                        "hibernate": hib_projects,
                        "frogged": frog_projects,
                        "need update": need_update,
                        "updated": updated}

    counts = {k: len(v) for k,v in projects_by_type.items()}

    data_dict = {
                "labels": [k for k in sorted(counts.keys())],
                "datasets": [
                    {
                        "data": [v for k, v in sorted(counts.items())],
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                            "red",
                            "blue",
                            "green",
                        ],
                        "hoverBackgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                        ]
                    }]
            }

    # data_dict = jsonify(data_dict)

    return render_template("projects.html",
                            finished=fin_projects,
                            hibernate=hib_projects,
                            frogged=frog_projects,
                            needUpdate= need_update,
                            updated=updated,
                            counts=counts,
                            dict=data_dict)


@app.route('/projects/<projectid>', methods=['GET'])
def view_details(projectid):
    """ Show the project details and update form for a given project"""

    # get the project for that project id
    project = Project.query.get(int(projectid))

    # get the images associated with the project
    images = Image.query.filter_by(project_id = projectid).all()

    # show the project details page
    return render_template('project_details.html',
                           project=project,
                           images=images)

@app.route('/projects/<projectid>', methods=['POST'])
def update_project(projectid):
    """ Update the database with form inputs """

    up_notes =request.form.get('notes')
    up_status = request.form.get('status')
    up_image = request.form.get('img-url')

    # get the project for that project id
    project = Project.query.get(int(projectid))

    # get the current user's user object
    user = User.query.get(session['user'])

    # update the db and ravelry page
    tracker.post_project_update(project, up_notes, up_status, up_image, user)

    # go to the project page
    return redirect("/projects/%s" % (projectid))


if __name__ == "__main__":
    # set up debug toolbar
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # run the app
    app.run(port=5000, host='0.0.0.0')