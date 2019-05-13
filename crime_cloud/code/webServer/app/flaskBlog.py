#!/usr/bin/env python3

from flask import Flask, render_template
app = Flask(__name__)
tasks = [
    {
        'name': 'Gabby lol',
        'title': 'chutiya'
    },
    {
        'name' : 'Mayank du!',
        'title': 'damn!'
    }
]
@app.route("/")
def home():
    return render_template('home.html', tasks=tasks)

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0',port=50000)
