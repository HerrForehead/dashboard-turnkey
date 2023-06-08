import os
import threading
from flask import Flask, render_template, request, redirect
from flask_sslify import SSLify

# Create the app
app = Flask(__name__)
sslify = SSLify(app)

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
