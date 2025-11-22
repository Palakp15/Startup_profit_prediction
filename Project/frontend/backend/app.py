# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import traceback

MODEL_PATH = 'model.pkl'

app = Flask(__name__)
CORS(app)

model = None
# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import traceback

MODEL_PATH = 'model.pkl'

app = Flask(__name__)
CORS(app)

model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        model = None


@app.route('/')
def hello():
    return jsonify({"status": "ok", "message": "Startup Profit Prediction API"}), 200


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # expected keys: rd_spend, administration, marketing_spend, state
        rd = float(data.get('rd_spend', 0))
        admin = float(data.get('administration', 0))
        market = float(data.get('marketing_spend', 0))
        state = data.get('state', 'New York')
        if model is None:
            return jsonify({"error": "Model not available. Train model first."}), 500

        import pandas as pd
        X = pd.DataFrame([{
            'R&D Spend': rd,
            'Administration': admin,
            'Marketing Spend': market,
            'State': state
        }])
        pred = model.predict(X)[0]
        return jsonify({"prediction": float(pred)})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400


@app.route('/retrain', methods=['POST'])
def retrain():
    """
    Optional endpoint: if you upload a new CSV to backend/startup_data.csv
    you can call this endpoint to re-run training (dangerous in production).
    """
    try:
        from train_model import train_and_save
        train_and_save()
        load_model()
        return jsonify({"status": "retrained"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    load_model()
    app.run(debug=True, port=5001)


