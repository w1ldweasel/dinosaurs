from datetime import datetime
from flask import Flask, render_template, make_response, request

#work out todays date
x = datetime.now()
today = x.strftime("%A") + " " + x.strftime("%e") + " " + x.strftime("%B")

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def root():
    userAgent = request.headers.get('User-Agent')
    return render_template('index.html', today=today, title="Home", userAgent=userAgent)

@app.route('/max')
def max():
    return render_template('max.html')

@app.route('/dave')
def dave():
    return render_template('dave.html')

@app.route('/phil')
def phil():
    return render_template('phil.html')

@app.route('/ben')
def ben():
    return render_template('ben.html')

if __name__ == '__main__':
    # This is used when running locally only. 
    app.run(host='127.0.0.1', port=8080, debug=True)