import codecs
import urllib2

from flask import render_template, request, send_file

from webapp import app
from utils.file_manager import FileManager
from utils.json_converter import JsonConverter


__author__ = 'Borja'

API_ENDPOINT = 'http://127.0.0.1:5000'

fileManager = FileManager()
jsonConverter = JsonConverter()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def manage_uploaded_file():
    # Get the name of the uploaded file
    sent_file = request.files['file']

    if sent_file:
        file_path = fileManager.save_file(sent_file)

        # Open the uploaded file in utf-8 format and validate it
        with codecs.open(file_path, encoding='utf-8') as file_utf8:
            document_content = file_utf8.readlines()

            json_document = jsonConverter.parse_object(document_content)
        req = urllib2.Request(API_ENDPOINT + '/document/validation')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json_document)

        document = response.read().document

        with open('CWROutput.V21', "w") as output_file:
            for record in sorted(document.extract_records(), key=lambda item: item.number):
                output_file.write((record.record + "\n").encode('utf-8'))
                for message in record.messages:
                    print str(message)
                    output_file.write(str(message) + "\n")

        return send_file('CWROutput.V21')

