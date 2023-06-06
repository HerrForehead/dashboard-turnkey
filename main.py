import os
import threading
import docker
from flask import Flask, render_template, request, redirect

# Create the app
app = Flask(__name__)

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
    app.run()
