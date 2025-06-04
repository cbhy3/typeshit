from io import BytesIO
#todo try and fix the thing where sometimes therell. be an erorr when doing from album, or at least just loop out the exception
import requests
from flask import session,Flask, render_template, request, redirect, url_for, send_file
from t import *
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") 


@app.route('/', methods=['GET', 'POST'])
def form():
    selected_options = []
    result = None
    if request.method == 'POST':
        selected_options = request.form.getlist('options')
        result = generate(selected_options)

    return render_template("main.html", selected_options=selected_options, result=result)
@app.route('/image')
def proxy():
    image_url = request.args.get('url')
    if not image_url:
        return "Missing image URL", 400

    response = requests.get(image_url)
    return send_file(BytesIO(response.content), mimetype='image/jpeg')

@app.route('/album', methods = ['GET', 'POST'])
def from_album():
    link = None
    result = None
    if request.method == 'POST':
        link = request.form.get('link')
        result = find_similiar(link)

    return render_template('from_album.html', link=link, result = result )

if __name__ == '__main__':
    app.run(debug=True)
