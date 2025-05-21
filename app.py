from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        area = float(request.form['area'])
        bedrooms = int(request.form['bedrooms'])
        bathrooms = int(request.form['bathrooms'])
        floors = int(request.form['floors'])
        location = int(request.form['location'])  # 1 = Big City, 2 = Village, 3 = Suburban
        parking = int(request.form['parking'])
        age = int(request.form['age'])

        input_data = np.array([[area, bedrooms, bathrooms, floors, location, parking, age]])

        prediction = model.predict(input_data)[0]
        predicted_price = round(prediction *15)  # 💰 Adjusted multiplier

        return render_template('index.html', price="₹{:,.2f}".format(predicted_price))
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
