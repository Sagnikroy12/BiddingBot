from flask import Flask, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app=Flask(__name__)

model = joblib.load('random_forest_model.pkl')

label_encoder = LabelEncoder()
file_path = 'Final_Dataset.xlsx'
df = pd.read_excel(file_path,engine='openpyxl')
df['Destination'] = label_encoder.fit_transform(df['Destination'])

def map_destination(destination_name):
    destination_mapping = {name: code for code, name in enumerate(label_encoder.classes_)}
    return destination_mapping[destination_name]

@app.route('/predict', methods=['GET'])
def predict():
    data = request.get_json()
    destination = data['destination'].upper()
    order_quantity = data['order_quantity']

    try:
        destination_code = map_destination(destination)
        input_data = pd.DataFrame([[destination_code,order_quantity]], columns=['Destination','Order Quantity'])
        prediction = model.predict(input_data)
        predicted_difference = int(prediction[0])
        return jsonify({'difference': predicted_difference})
    except ValueError as e:
        return jsonify({'error':str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)