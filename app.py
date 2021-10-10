from flask import Flask, send_from_directory, request
from game import create_tasks
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'images'


@app.route('/', methods=['GET'])
def root():
    return create_tasks(request.args.get('case'))


@app.route('/<path:filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=filename)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
