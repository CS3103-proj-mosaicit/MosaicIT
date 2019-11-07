from flask import Flask, render_template
from flask import request, redirect
import os  # for image upload

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "/mnt/c/wsl/projects/pythonise/tutorials/flask_series/app/app/static/img/uploads"


@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html')

@app.route('/gallery')
def gallery():
	return render_template('gallery.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	# if request.method == 'POST':
 #        postdata = request.form
 #        file_name = postdata['filename']
 #        print("file name: ====================== {}".format(file_name))
 #        file = str(file_name)
 #        path = ".\\static\\" + file
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image))
            print("Image saved")
            return redirect(request.url)

    return render_template('upload.html')



if __name__ == '__main__':
    app.run()