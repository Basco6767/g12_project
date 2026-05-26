from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = datetime.datetime.today()
    return render_template("hello.html", data = data )
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()