from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import os


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def paint_walls(image_path, selected_walls, paint_color):
    image = cv2.imread(image_path)
    
    # Dummy function to paint selected walls with the provided color
    # In a real system, you'd use more sophisticated methods for wall detection
    for wall in selected_walls:
        cv2.rectangle(image, (wall[0], wall[1]), (wall[2], wall[3]), paint_color, -1)

    output_path = 'static/result.jpg'
    cv2.imwrite(output_path, image)
    return output_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.jpg')
        file.save(image_path)

        return redirect(url_for('customize', image_path=image_path))

    return redirect(request.url)

@app.route('/customize/<image_path>', methods=['GET', 'POST'])
def customize(image_path):
    if request.method == 'POST':
        selected_walls = request.form.getlist('walls')
        paint_color = tuple(map(int, request.form['color'].split(',')))

        result_path = paint_walls(image_path, selected_walls, paint_color)
        return render_template('customize.html', image_path=image_path, result_path=result_path)

    return render_template('customize.html', image_path=image_path)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
