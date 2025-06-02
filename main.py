from io import BytesIO

import requests
from flask import Flask, render_template, request, redirect, url_for, send_file
from t import generate
app = Flask(__name__)

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
if __name__ == '__main__':
    app.run(debug=True)