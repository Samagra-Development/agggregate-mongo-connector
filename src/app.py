"""
Create Flask Application and Initialize Database
"""
import os
import json
import pymongo
from pymongo import MongoClient
from bson import json_util
from flask import Flask
from flask import request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = MongoClient(os.environ.get("MONGO_HOST"), os.environ.get("MONGO_PORT"))#host uri
db_name = os.environ.get("DB_NAME")
db = client.db_name #Select the database

@app.route("/save", methods=['POST'])
def save_data():
    """
    :param request in json format then save its data in mongo database
    """
    # Converting unicodes to str and then str to dict.
    req_data = json.loads(json.dumps(request.json))
    # Getting the form ID to distinguish between various template document and mapping sheet
    form_id = req_data['formId']
    new_req_data = req_data['data'][0]  # Getting the data : [{values}]

    new_req_data = json.loads(json.dumps(new_req_data))  # Getting the new data
    form_submission_date = new_req_data[
        '*meta-submission-date*']  # Correcting the submission date and removing the time
    end_index = form_submission_date.find(str('T'))
    form_submission_date = form_submission_date[:end_index]
    # Saving the corrected date in the json
    new_req_data['*meta-submission-date*'] = form_submission_date
    new_req_data['form_id'] = form_id
    data_requests = db[form_id]
    data_requests.insert_one(new_req_data)

    return {"success":True}

@app.route("/get-data", methods=['GET'])
def get_data():
    """
    fetch data of particular user
    :param user_name:string user whose data we want to access
    :param form_id: string form whose data we want to access
    :param sortBy: string field on the basis of which we want to sort data
    """
    sort_field = request.values.get("sortBy")
    user_name = request.values.get("user_name")
    form_id = request.values.get("form_id")
    cond = {'username':user_name}
    all_data = dict()
    i = 0
    data_requests = db[form_id]
    for data_request in data_requests.find(cond).sort([(sort_field, pymongo.DESCENDING)]):
        #pprint.pprint(data_request)
        all_data[i] = data_request
        i += 1
    return json.loads(json_util.dumps(all_data))

if __name__ == "__main__":

    app.run()
