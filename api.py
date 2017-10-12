from model import db, User, Image
import requests
import os
from PIL import Image as pilImage

auth=(os.environ['RAVELRY_ACCESS_KEY'], os.environ['RAVELRY_PERSONAL_KEY'])
access_key=os.environ['RAVELRY_ACCESS_KEY']
api_url = "https://api.ravelry.com/"

def projects(user, headers_input = {}):
    """Load projects for a user from Ravelry api into database"""

    projects_response = requests.get('https://api.ravelry.com/projects/' + user +
                                '/list.json',
                                auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                os.environ['RAVELRY_PERSONAL_KEY']),
                                headers=headers_input)

    return projects_response

def project_details(user, project_id):
    """ Get the details for a project from the api """

    details = requests.get('https://api.ravelry.com/projects/%s/%s.json' % (
                            user, project_id),
                            auth=(os.environ['RAVELRY_ACCESS_KEY'],
                            os.environ['RAVELRY_PERSONAL_KEY']))
    tag = details.headers['ETag']

    return details.json(), tag


def post_project_api_update(project,notes, status, user):
    """ Update the api project page """

    data = {"notes": notes, "project_status_id": status}

    response = requests.post("https://api.ravelry.com/projects/%s/%s.json" %
                              (user.username, project.project_id),
                              data,
                              auth=auth)


def post_add_image(project, user, photo):
    """ add an image to the api project page """

    # change the image to a png for the api
    response_image = requests.get(photo, stream=True)
    photo = pilImage.open(response_image.raw)
    photo.save('photo.png')

    # get an upload token from api
    upload_token_json = requests.post(api_url + "upload/request_token.json",
                                    auth=auth).json()
    upload_token = upload_token_json['upload_token']

    # set up to files for a multipart file upload
    files = [('file0', ('photo.png', open('photo.png', 'rb'), 'image/png'))]
    data = {"upload_token": upload_token, "access_key":access_key}
    
    # upload the photo to the api
    upload_res = requests.post(api_url + "upload/image.json",
                               files=files,
                               data=data).json()
    image_id = upload_res['uploads']['file0']['image_id']

    # delete photo now that it is uploaded
    os.remove('photo.png')
    
    # assign the image to the project page in the api
    data = {"image_id": image_id}
    resp = requests.post("%sprojects/%s/%s/create_photo.json" %
                              (api_url, user.username, project.project_id),
                              data,
                              auth=auth)
