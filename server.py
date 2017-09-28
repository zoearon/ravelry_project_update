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

    session['user'] = 463097
    return render_template("homepage.html")

@app.route('/projects')
def view_projects():
    """ View the current users projects """

    # Get the projects for the current user and are in progress
    projects = db.session.query(Project).join(Status).filter(
               Project.user_id == session['user'],
               Status.status == "In progress").all()

    # sort the in progress projects into 2 groups based on update needs
    need_update, updated = tracker.sort_projects_by_update(projects)

    return render_template("projects.html",
                            needUpdate= need_update,
                            updated=updated)

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

    now = tracker.NOW
    project.notes = up_notes
    project.status_id = int(up_status)
    project.updated_at = now
    if up_image:
        image = Image(url=up_image, project_id=projectid)
        db.session.add(image)
    db.session.commit()

    data = {"notes": up_notes, "project_status_id": up_status}

    user = User.query.get(session['user'])
    response = requests.post("https://api.ravelry.com/projects/" +
                              user.username + "/" + projectid + ".json",
                              data,
                              auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                    os.environ['RAVELRY_PERSONAL_KEY']))

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