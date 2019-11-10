
import uuid
import os
import json
from flask import Flask, render_template
from flask import request, redirect, jsonify
from flask import send_from_directory, send_file
from flask import flash, session, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

app = Flask(__name__)
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField()

def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html')

@app.route('/gallery')
def gallery():
	return render_template('gallery.html')

@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/download/<path:filename>')
def downloadFile(filename):
    path = os.path.join(app.config['UPLOAD_PATH'], filename)
    return send_file(path, as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        path_to_save = os.path.join(app.config['UPLOAD_PATH'], filename)
        f.save(path_to_save)

        mosaic_file_name = filename
        session['filenames'] = [mosaic_file_name]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form = form)


@app.route("/api/crawler_status.json", methods=["GET","POST"])
def crawler_status():
    with open('crawler/status.json', 'r', encoding='utf-8') as f:
        data = f.read()
    return jsonify(json.loads(data))

@app.route("/api/puzzle_status.json", methods=["GET","POST"])
def puzzle_status():
    with open('puzzle/status.json', 'r', encoding='utf-8') as f:
        data = f.read()
    return jsonify(json.loads(data))

@app.route("/api/create_puzzle", methods=["GET","POST"])
def create_puzzle():
    input_filename = request.args.get("input")
    output_filename = request.args.get("input")
    cmd = "python3 puzzle/puzzle.py -i {} -o {} -d crawler/image/  -t puzzle/output/".format(input_filename, output_filename)
    print(cmd)
    os.system(cmd)
    data = {
        "input": input_filename,
        "output": output_filename
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)