from flask import Flask, render_template,request
from RecommendationPredictor import RecommendationPredictor
from db import Database

import pandas as pd
app = Flask(__name__)
m = RecommendationPredictor()
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitted',methods=['post'])
def prediction():
    df = dict()
    df['airline'] = [request.form.get('Airline')]
    df['overall'] = [request.form.get('overall_rating')]
    df['author'] = [request.form.get('user_name')]
    df['customer_review'] = [request.form.get('review')]
    df['traveller_type'] = [request.form.get('traveller_type')]
    df['cabin'] = [request.form.get('cabin')]
    if request.form.get('via'):
        df['route'] = [request.form.get('Source') + " to " + request.form.get('Destination') + " via " + request.form.get('via')]
    else:
        df['route'] = [request.form.get('Source') + " to " + request.form.get('Destination')]
    df['date_flown'] = [request.form.get('date_flown')]
    df['seat_comfort'] = [request.form.get('seat_comfort')]
    df['cabin_service'] = [request.form.get('cabin_service')]
    df['food_bev'] = [request.form.get('food_bev')]
    df['entertainment'] = [request.form.get('entertainment')]
    df['ground_service'] = [request.form.get('ground_Service')]
    df['value_for_money'] = [request.form.get('value_for_money')]
    df['user_email'] = [request.form.get('user_email')]

    pred_df = pd.DataFrame(df)
    model_df = pred_df[['overall', 'cabin', 'seat_comfort', 'cabin_service', 'food_bev', 'entertainment', 'value_for_money','customer_review']]
    pred = m.predict(model_df)
    rec = dict()
    rec['Email'] = df['user_email'][0]
    rec['Name'] = df['author'][0]
    rec['Date'] = df['date_flown'][0]
    rec['Route'] = df['route'][0]
    rec['Airline'] = df['airline'][0]
    rec['Recommend'] = pred
    response = db.insert(rec)
    if response == 0:
        message = "Thank you ! Your review has been already recorded"
    if response == 1:
        message = "Thank You! For your review"
    return render_template('submitted.html',message =message)

if __name__ == "__main__":
    app.run(debug=True)