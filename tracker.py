
import datetime

NOW = datetime.datetime.now()

def time_difference_now(time):
    """ Find how much time has passed since a datetime in hours"""


    diff = NOW - time

    day_seconds = diff.days * 24 * 60 *60

    seconds = day_seconds + diff.seconds

    hours = (seconds/60.0)/60.00

    days = hours/24.00

    return days

def sort_projects_by_update(projects):
    """ sort a list of project objects into 2 lists based on update """

    need_update = []
    update = []

    for project in projects:
        since_update = time_difference_now(project.updated_at)
        if since_update > 14:
            need_update.append((project, since_update))
        else:
            update.append((project, since_update))

    return need_update, update

