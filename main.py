import os
import threading
import docker
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def start():
    return render_template("index.html")


@app.route('/home')
def home():
    return render_template("index.html")


@app.route("/result", methods=['POST', "GET"])
def result():
    output = request.form.to_dict()
    print(output)

    return render_template("index.html")


@app.route("/remove", methods=['POST', "GET"])
def remove():
    output = request.form.to_dict()
    print(output)

    return redirect("/")


if __name__ == '__main__':
    app.run()
