from io import BytesIO

import requests
from flask import session,Flask, render_template, request, redirect, url_for, send_file
from t import *
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") 

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("https://findmusictypeshit.onrender.com/callback")
SCOPE = "user-library-read"

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)

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

@app.route("/callback")
def callback():
    code = request.args.get('code')
    if code:
        token_info = sp_oauth.get_access_token(code, as_dict=True)
        session['token_info'] = token_info
        return redirect("/album")  
    else:
        return "Authorization failed.", 400
if __name__ == '__main__':
    app.run(debug=True)
