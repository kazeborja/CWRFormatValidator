import codecs

from flask.ext.restful import Api, Resource, abort

from api import app
from flask import render_template, request, Response
from utils.file_manager import FileManager
from validator import Validator
import json
import datetime

__author__ = 'Borja'

api = Api(app)
fileManager = FileManager()
validator = Validator()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')


class ValidateDocumentRegexAPI(Resource):
    @staticmethod
    def post():

        # Get the name of the uploaded file
        sent_file = request.files['file']

        if sent_file:
            file_path = fileManager.save_file(sent_file)

            # Open the uploaded file in utf-8 format and validate it
            with codecs.open(file_path, encoding='utf-8') as file_utf8:
                document_content = file_utf8.readlines()

                valid_records, invalid_records = validator.validate_document_format(document_content)
        elif request.json is not None:
            # Get json document from the request
            json_document = request.json

            # Validate the regex
            valid_records, invalid_records = validator.validate_document_format(json_document)
        else:
            abort(404)

        result = {
            'success': True,
            'valid_records': valid_records,
            'invalid_records': invalid_records
        }

        return response_json_item(result)

api.add_resource(ValidateDocumentRegexAPI, '/document/validation/regex', endpoint='regex_validation')

dt_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else obj.__dict__)


def response_json_list(app_request, collection):
    """
    Return response with the content in the format requested
    :type app_request: object
    Available formats:
    * JSON

    :param app_request: the request object
    :param collection: the collection to be converted
    :return: response in the requested format
    """

    def return_json():
        return Response(json.dumps(collection, default=dt_handler), mimetype='application/json')

    functions = {
        'json': return_json,
    }

    functions_accept = {
        'application/json': return_json,
    }

    if request.args.get('format') in functions.keys():
        return functions[app_request.args.get('format')]()
    else:
        return (functions_accept[app_request.headers.get('Accept')]
                if request.headers.get('Accept') in functions_accept.keys() else functions['json'])()


def response_json_item(item):
    return Response(json.dumps(item, default=dt_handler), mimetype='application/json')