from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 

from model import connect_to_db, db, User, Project, Status, Image
# import datetime
import tracker
import api
import requests
import os
from seed import sync_projects
import datetime
from sqlalchemy.sql.functions import func

app = Flask(__name__)

JS_TESTING_MODE = False

# Required to use Flask sessions and the debug toolbar
app.secret_key = "secret"

# Raise error if undefine Jinja variable
app.jinja_env.undefined = StrictUndefined

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE


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


@app.route('/user/update', methods=["POST"])
def update():

    # Update the database
    user = User.query.get(int(session['user']))

    user.phone_num = str(request.form.get('phone'))
    user.update_time = int(request.form.get('frequency'))
    user.subscribed = bool(request.form.get('subscribed'))

    db.session.commit()

    return "User Successfuly Updated!"


@app.route('/logout')
def logout():
    """ log out user from the session """

    # remove any users from the session
    session.clear()

    # redirect back to login
    return redirect('/login')


# @app.route('/login', methods=['GET'])
# def login():
#     """ show the login form """

#     return render_template("login.html")


# @app.route('/login', methods=['POST'])
# def check_user():
#     """ log the user in """

#     # get the user name from the post form
#     user = request.form.get("username")
#     password = request.form.get("password")

#     route = tracker.check_login(user, password)

#     return redirect(route)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = tracker.check_login(username, password)        
        if user:
            login_user(user)
            return redirect('/user')
        else:
            return redirect('/login')
    else:

@app.route('/projects')
def view_projects():
    """ View the current users projects """

    # check if there is a current user
    if 'user' not in session:
        return redirect("/login")

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

    # get project update time
    freq = db.session.query(User.update_time).filter(
        User.user_id == session['user']).one()[0]

    # sort the in progress projects into 2 groups based on update needs
    need_update, updated = tracker.sort_projects_by_update(wip_projects, freq)

    projects_by_type = {"finished": fin_projects,
                        "hibernate": hib_projects,
                        "frogged": frog_projects,
                        "need update": need_update,
                        "updated": updated}

    counts = {k: len(v) for k, v in projects_by_type.items()}

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

    wip_dict = {
                "labels": ["WIP"],
                "datasets": [
                    {
                        "label": "Need Update",
                        "data": [counts['need update']],
                        "backgroundColor": [
                            "#B56357"
                        ],
                        "hoverBackgroundColor": [

                            "#FF6F59"
                        ],
                        "hoverBackgroundColor": [
                            "#FF6F59"
                        ]
                    },
                    {
                        "label": "Updated",
                        "data": [counts['updated']],
                        "backgroundColor": [

                            "#B4DBC0"
                        ],
                        "hoverBackgroundColor": [
                            "#B4DBC0"

                            "#43AA8B"
                        ],
                        "hoverBackgroundColor": [
                            "#43AA8B"

                        ]
                    }]}

    return render_template("projects.html",
                           finished=fin_projects,
                           hibernate=hib_projects,
                           frogged=frog_projects,
                           needUpdate=need_update,
                           updated=updated,
                           counts=counts,
                           dict=data_dict,
                           wip=wip_dict,
                           freq=freq)


@app.route('/projects/<projectid>', methods=['GET'])
def view_details(projectid):
    """ Show the project details and update form for a given project"""

    # get the project for that project id
    project_images = Project.query.options(db.joinedload('images'), db.joinedload('status')).filter(
        Project.project_id == projectid).one()

    project = project_images
    images = project.images

    # get username
    username = db.session.query(User.username).filter(User.user_id == session['user']).one()[0]

    # show the project details page
    return render_template('project_details.html',
                           project=project,
                           images=images,
                           username=username)


@app.route('/projects/<projectid>', methods=['POST'])
def update_project(projectid):
    """ Update the database with form inputs """

    up_notes = request.form.get('notes')
    up_status = request.form.get('status')
    up_image = request.form.get('img-url')
    up_progress = request.form.get('progress')

    # get the project for that project id
    project = Project.query.get(int(projectid))

    # get the current user's user object
    user = User.query.get(session['user'])

    # update the db
    tracker.post_project_db_update(project, up_notes,
                                   up_status, up_image,
                                   user, up_progress)

    # update api/ ravelry project page
    api.post_project_api_update(project, up_notes, up_status, up_progress, user)
    api.post_add_image(project, user, up_image)

    # flash message about update
    flash("Update Successful")

    # go to the project page
    return redirect("/projects/%s" % (projectid))


@app.route('/sync')
def sync():

    user = request.args.get('user')
    print user

    return sync_projects(user)


@app.route('/projects-react')
def react_page():

    # check if there is a current user
    if 'user' not in session:
        return redirect("/login")

    # get project update time
    freq = db.session.query(User.update_time).filter(
           User.user_id == session['user']).one()[0]

    NOW = datetime.datetime.now()

    # Get finished projects
    fin_projects = db.session.query(func.count(Project.project_id)).join(Status).filter(
               Project.user_id == session['user'],
               Status.status == "Finished").first()[0]

    # Get hibernating projects
    hib_projects = db.session.query(func.count(Project.project_id)).join(Status).filter(
               Project.user_id == session['user'],
               Status.status == "Hibernating").first()[0]

    # Get frogged projects
    frog_projects = db.session.query(func.count(Project.project_id)).join(Status).filter(
               Project.user_id == session['user'],
               Status.status == "Frogged").first()[0]

    # Get the projects for the current user and are in progress
    need_update = db.session.query(func.count(Project.project_id)).join(Status).filter(
               Project.user_id == session['user'],
               Project.updated_at < (NOW - datetime.timedelta(days = freq)),
               Status.status == "In progress").first()[0]

    updated = db.session.query(func.count(Project.project_id)).join(Status).filter(
               Project.user_id == session['user'],
               Project.updated_at > (NOW - datetime.timedelta(days = freq)),
               Status.status == "In progress").first()[0]

    counts = {"finished": int(fin_projects),
                        "hibernate": int(hib_projects),
                        "frogged": int(frog_projects),
                        "need update": int(need_update),
                        "updated": int(updated)}

    # counts = {k: len(v) for k,v in projects_by_type.items()}

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

    wip_dict = {
                "labels": ["WIP"],
                "datasets": [
                    {
                        "label": "Need Update",
                        "data": [counts['need update']],
                        "backgroundColor": [
                            "blue"
                        ],
                        "hoverBackgroundColor": [
                            "#B56357"
                        ]
                    },
                    {
                        "label": "Updated",
                        "data": [counts['updated']],
                        "backgroundColor": [
                            "green"
                        ],
                        "hoverBackgroundColor": [
                            "#B4DBC0"
                        ]
                    }] }

    return render_template("react-projects.html",
                            finished=fin_projects,
                            hibernate=hib_projects,
                            frogged=frog_projects,
                            needUpdate= need_update,
                            updated=updated,
                            counts=counts,
                            dict=data_dict,
                            wip=wip_dict,
                            freq=freq)

@app.route('/projects-json/<status>')
def project_list(status):

    
    # # Get the projects for the current user and are in progress
    # wip_projects = db.session.query(Project).join(Status).filter(
    #            Project.user_id == session['user'],
    #            Status.status == "In progress").order_by(Project.updated_at).all()

    # # get project update time
    # freq = db.session.query(User.update_time).filter(
    #        User.user_id == session['user']).one()[0]

    # # sort the in progress projects into 2 groups based on update needs
    # need_update, updated = tracker.sort_projects_by_update(wip_projects, freq)
    session['user'] = 463097
    NOW = datetime.datetime.now()
    if str(status) == "Need Update":
        status = 'In progress'
        freq = db.session.query(User.update_time).filter(
               User.user_id == session['user']).one()[0]
        projects = db.session.query(Project.name, Project.project_id).join(Status).filter(
            Project.user_id == session['user'],
            Project.updated_at < (NOW - datetime.timedelta(days = freq)),
            Status.status == status).all()

    elif str(status) == 'Updated':
        status = u'In progress'
        freq = db.session.query(User.update_time).filter(
               User.user_id == session['user']).one()[0]
        projects = db.session.query(Project.name, Project.project_id).join(Status).filter(
            Project.user_id == session['user'],
            Project.updated_at > (NOW - datetime.timedelta(days = freq)),
            Status.status == status).all()
    else:
        projects = db.session.query(Project.name, Project.project_id).join(Status).filter(
            Project.user_id == session['user'],
            Status.status == status).all()
    return jsonify(projects=projects)

if __name__ == "__main__":
    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True

    # set up debug toolbar
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    # run the app
    app.run(port=5000, host='0.0.0.0')
