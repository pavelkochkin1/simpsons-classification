import os

from flask import Flask
from flask import request
from flask import render_template

from model.model import MobNetSimpsons


app = Flask(__name__)
UPLOAD_FOLDER = "static/"

@app.route('/', methods=['GET', 'POST'])
def upload_predict():
    if request.method == "POST":
        image_file = request.files["image"]
        image_location = os.path.join(
            UPLOAD_FOLDER,
            image_file.filename
        )
        if image_file:
            image_file.save(image_location)
            pred = model.predict(image_location)
            return render_template(
                "index.html", 
                prediction=pred[0],
                proba=round(pred[1], 2),
                image_loc=image_file.filename
            )
    return render_template("index.html", prediction=0, image_loc=None)

if __name__ == "__main__":
    model = MobNetSimpsons()
    app.run(port=8888, debug=True, host='0.0.0.0')
