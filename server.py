from jinja2 import StrictUndefined

from flask import Flask, jsonify,render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Project, Status, Image
import datetime
import tracker

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "secret"

# Raise error if undefine Jinja variable
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ View homepage """

    session['user'] = 463097
    return render_template("homepage.html")

@app.route('/projects')
def view_projects():
    """ View the current users projects """

    projects = db.session.query(Project).join(Status).filter(Status.status == 
               "In progress").all()

    need_update, updated = tracker.sort_projects_by_update(projects)

    return render_template("projects.html",
                            needUpdate= need_update,
                            updated=updated)

@app.route('/projects/<projectid>', methods=['GET'])
def view_details(projectid):
    """ Show the project details and update form for a given project"""

    project = Project.query.get(int(projectid))

    images = Image.query.filter_by(project_id = projectid).all()

    return render_template('project_details.html',
                           project=project,
                           images=images)

@app.route('/projects/<projectid>', methods=['POST'])
def update_project(projectid):
    """ Update the database with form inputs """

    return redirect("/projects/%s" % (projectid))


if __name__ == "__main__":
    # set up debug toolbar
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # run the app
    app.run(port=5000, host='0.0.0.0')