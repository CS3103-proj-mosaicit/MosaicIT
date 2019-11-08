from flask import Flask, render_template
from flask import request, redirect
from flask import send_from_directory
from flask import flash, session, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import uuid
import os  # for image upload

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


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	# if request.method == 'POST':
 #        postdata = request.form
 #        file_name = postdata['filename']
 #        print("file name: ====================== {}".format(file_name))
 #        file = str(file_name)
 #        path = ".\\static\\" + file
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename =random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success.')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form = form)
    # if request.method == "POST":
    #     if request.files:
    #         image = request.files["image"]
    #         image.save(os.path.join(app.config["IMAGE_UPLOADS"], image))
    #         print("Image saved")
    #         return redirect(request.url)

    # return render_template('upload.html')

if __name__ == '__main__':
    app.run()