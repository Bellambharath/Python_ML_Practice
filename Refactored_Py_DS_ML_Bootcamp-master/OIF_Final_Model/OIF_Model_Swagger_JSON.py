from flask import Flask, jsonify, request, send_file, url_for
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
import pandas as pd
import io
import os
import uuid
from OIF_Final_Model_Python import OIF
import warnings

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

data = pd.read_excel('ML_forecast_results_EMEA_.xlsx')  
Regions = ['All', 'DAO', 'EMEA', 'APJ']
Model_Names = ['All', 'DecisionTree', 'RandomForest', 'GBM', 'SVM']
Future_Prediction_SampleCount = [50, 100, 150, 200]

class OIF_Model(Resource):
    @swag_from({
        'parameters': [
            {
                'name': 'region',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Name of the region. If "All" is selected, Model_Name will be set to "All" and Future_Prediction will be set to 167.',
                'enum': Regions
            },
            {
                'name': 'Model_Name',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Name of the Model. Default is "All" if region is "All".',
                'enum': Model_Names
            },
            {
                'name': 'Future_Prediction',
                'in': 'query',
                'type': 'integer',
                'required': True,
                'description': 'Number of Samples needed. Default is 167 if region is "All".',
                'enum': Future_Prediction_SampleCount
            }
        ],
        'responses': {
            200: {
                'description': 'Data in JSON format and a download URL for the Excel file',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'data': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object'
                                    }
                                },
                                'download_url': {
                                    'type': 'string',
                                    'format': 'uri'
                                }
                            }
                        }
                    }
                }
            },
            400: {
                'description': 'Invalid input'
            }
        }
    })
    def get(self):
        try:
            region = request.args.get('region').upper()
            model_name = request.args.get('Model_Name')
            future_prediction = int(request.args.get('Future_Prediction'))

            if region == "ALL":
                model_name = "ALL"
                future_prediction = 167
                filename = 'ML_forecast_results_ALL.xlsx'
                output_data = OIF(region=region, model_name=model_name, noOfSamples=future_prediction)
            else:
                output_data = OIF(region=region, model_name=model_name, noOfSamples=future_prediction)

            temp_dir = os.path.join(os.getcwd(), 'tmp')
            os.makedirs(temp_dir, exist_ok=True)
            
            temp_filename = f"{uuid.uuid4()}.xlsx"
            temp_path = os.path.join(temp_dir, temp_filename)
            writer = pd.ExcelWriter(temp_path, engine='xlsxwriter')
            output_data.to_excel(writer, index=False, sheet_name='Sheet1')
            writer.close()

            download_url = url_for('download_file', filename=temp_filename, _external=True)

            return jsonify({
                'data': output_data.to_dict(orient='records'),
                'download_url': download_url
            })
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'error': str(e)}), 400

@app.route('/download/<filename>')
def download_file(filename):
    temp_dir = os.path.join(os.getcwd(), 'tmp')
    return send_file(os.path.join(temp_dir, filename), as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

api.add_resource(OIF_Model, '/getdata')

if __name__ == '__main__':
    app.run(debug=True)
