import os
from flask import Flask, render_template, request, url_for, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
import glob
from ml import image_accuracy

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photos.save(request.files['photo'])
        # #--label_image function here--
        percent = image_accuracy("static/img/" + str(request.files['photo'])[16:-17])
        return percent
    return render_template('index.html')
    
@app.route('/')
def login():
	return render_template('index.html')
	
	
@app.route('/burger')
def burger_page():
	return render_template('burger.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        port = int(os.getenv('PORT', 8080)),
        host = os.getenv('IP', '0.0.0.0')
    )	                                                                                                                                                                                        