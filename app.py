import os
from flask import Flask, render_template, request, url_for, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from ml import image_accuracy
import food

app = Flask(__name__)

def time2Burn(calFromFood, excercise):
    if excercise == "biking":
        MET = 4.0
        
    elif excercise == "swimming":
        MET = 6.0
       
    elif excercise == "running":
        MET = 8.0

    energyExpenditure = .0175 * MET * 64.5
    
    time = int(calFromFood) / energyExpenditure
    
    roundTime = time - int(time)
    
    if roundTime > .49:
        roundTime = 1 - roundTime
        time += roundTime
        
    else:
    	time -= roundTime
    
    return time

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload/<item>')
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photos.save(request.files['photo'])
	picture = "static/img/" + str(request.files['photo'])[16:-17]
	item, score = image_accuracy(picture)
	cal = str(food.food[item]['Calories'])
	name = item.replace('_',' ').title()
	sodium = food.food[item]['Sodium']
	carbs = food.food[item]['Carbohydrates']
	sugar = food.food[item]['Total Sugar']
	protein = food.food[item]['Protein']
	fat = food.food[item]['Total Fat']
	s_fat = food.food[item]['Saturated Fat']
	t_fat = food.food[item]['Trans Fat']
	chol = food.food[item]['Cholesterol']
	
	runningCal = time2Burn(cal, "running")
	swimmingCal = time2Burn(cal, "swimming")
	bikingCal = time2Burn(cal, "biking")
	
	if score > .9:
		return render_template("food.html", item=item, cal=cal, name=name, sodium=sodium, 
    							carbs=carbs, sugar=sugar, protein=protein, fat=fat, 
    							s_fat=s_fat, t_fat=t_fat, chol=chol, picture=picture, 
    							runningCal=runningCal,swimmingCal=swimmingCal, bikingCal=bikingCal)
    return render_template("item_not_found.html")
    							
    							
@app.route('/')
def login():
	return render_template('index.html')
	

if __name__ == '__main__':
    app.run(
        debug=True,
        port = int(os.getenv('PORT', 8080)),
        host = os.getenv('IP', '0.0.0.0')
    )
