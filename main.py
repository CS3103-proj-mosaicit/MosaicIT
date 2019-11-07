from flask import Flask, render_template
import os  # for image upload

app = Flask(__name__)

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
 #        # return redirect(url_for('index'))
 #        return
    return render_template('upload.html')


if __name__ == '__main__':
    app.run()