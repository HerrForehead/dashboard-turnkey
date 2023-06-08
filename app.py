import os
import threading
from flask import Flask, render_template, request, redirect

# Create the app
app = Flask(__name__)

# Force redirect to HTTPS
@app.before_request
def force_https():
    if request.endpoint in app.view_functions and not request.is_secure:
        return redirect(request.url.replace('http://', 'https://'))


# Renders the home page
@app.route('/')
def start():
    return render_template("index.html")

# Renders the home page
@app.route('/home')
def home():
    return render_template("index.html")

# Grabs the data upon clicking the submit button and puts it in a dictionary
@app.route("/result", methods=['POST', "GET"])
def result():
    output = request.form.to_dict()
    print(output)
    
    # Any code we want to run goes here

    return render_template("index.html")

# This code will be unused
@app.route("/remove", methods=['POST', "GET"])
def remove():
    output = request.form.to_dict()
    print(output)

    return redirect("/")

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=('/home/student/dashboard-turn-key/cert.pem', '/home/student/dashboard-turn-key/key.pem'))
