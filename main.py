from flask import Flask, render_template
from flask import request, redirect
from flask import send_from_directory, send_file
from flask import flash, session, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import uuid
import os  # for path

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
        
        # rename the photo
        filename = random_filename(f.filename)

        # save the photo
        path_to_save = os.path.join(app.config['UPLOAD_PATH'], filename)
        f.save(path_to_save)

        # perform logic to do mosaic - to be modified
        mosaic_file_name = filename

        # save the final image name to display to session
        session['filenames'] = [mosaic_file_name]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form = form)

if __name__ == '__main__':
    app.run(port=5000, debug=False)