import os
from flask import request
from werkzeug.utils import secure_filename

class CSVUploader:
    def __init__(self, app, file_identifier, default_file_path=None):
        self.default_file_path = default_file_path
        self.file_identifier = file_identifier
        self.app = app
        self.UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)
        self.app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER

    def upload(self):
        if self.file_identifier in request.files:
            file = request.files[self.file_identifier]
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                return file_path
        return self.default_file_path
