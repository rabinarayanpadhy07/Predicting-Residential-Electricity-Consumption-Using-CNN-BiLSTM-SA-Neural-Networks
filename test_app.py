from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/AdminLogin')
def admin_login():
    return render_template('AdminLogin.html')

@app.route('/AdminScreen')
def admin_screen():
    return render_template('AdminScreen.html', msg='Login successful!')

@app.route('/Predict')
def predict():
    return render_template('Predict.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
