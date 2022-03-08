from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

def PredictRouteClient():
    pass

def trainRouteClient():
    pass


if __name__ == '__main__':
    app.run(debug=True)
