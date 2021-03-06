from flask import Flask, render_template, redirect, url_for, session, request, g
from functools import wraps
from sawo import verifyToken
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ['secret_key']
sawo_key = os.environ['sawo_key']
map_key = os.environ['map_key']
geoip_key = os.environ['geoip_key']

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index'))

    return wrap

@app.before_request
def before_request():
    g.user = None

    if 'logged_in' in session:
        user = session['logged_in']
        g.user = user

@app.route('/')
def index():
    return render_template('login.html', sawo_key=sawo_key, map_key=map_key, geoip_key=geoip_key)


@app.route('/login', methods=['GET','POST'] )
def loginfunc():
    if request.method == 'POST':
        data = request.get_json()
        if(verifyToken(data)):
            #do something
            session['logged_in'] = data['user_id']
            return 'OK', 200
        else:
            return 'Error', 200
        
    
@app.route('/dashboard')
def dashboard():
    if not g.user:
        return redirect(url_for('index'))

    return render_template('dashboard.html', map_key=map_key, geoip_key=geoip_key)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=False)