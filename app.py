from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Getting form values
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        cp = int(request.form['cp'])
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        thalach = int(request.form['thalach'])
        exang = int(request.form['exang'])

        # Dummy logic — Replace this with your ML model
        if age > 50 and chol > 240:
            prediction = "⚠️ High cardiovascular risk"
        else:
            prediction = "✅ Low cardiovascular risk"

        return render_template('index.html', prediction_text=prediction)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Flask is working ✅</h1>"

if __name__ == '__main__':
    app.run(debug=True)