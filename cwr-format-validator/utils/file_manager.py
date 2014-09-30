import os

from werkzeug.utils import secure_filename

from app.uploads import __uploads__

__author__ = 'Borja'


class FileManager(object):

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ['V21']

    def save_file(self, sent_file):
        uploads_path = __uploads__.path()

        if sent_file and self.allowed_file(sent_file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(sent_file.filename)

            file_path = os.path.join(uploads_path, filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            sent_file.save(file_path)

            return file_path
