from flask import Flask, jsonify, request, send_file
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
import pandas as pd
import io
from OIF_Final_Model_Python import OIF
import warnings

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
 
Regions = ['All','DAO', 'EMEA', 'APJ']
Model_Names = ['All','DecisionTree','RandomForest','GBM','SVM']
Future_Prediction_SampleCount = [50,100,150,200]

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
                'description': 'Excel file with the query results',
                'content': {
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': {
                        'schema': {
                            'type': 'string',
                            'format': 'binary'
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
            region = request.args.get('region')
            model_name = request.args.get('Model_Name')
            future_prediction = request.args.get('Future_Prediction')
            region =region.upper()
            future_prediction = int(future_prediction)
            

            if region == "ALL":
                model_name = "ALL"
                future_prediction = 167
                filename='ML_forecast_results_ALL.xlsx'
                regions = ['DAO', 'EMEA', 'APJ']
                output = OIF(region=region,model_name=model_name,noOfSamples=future_prediction)

               
                with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as excel_writer:
                    for df, reg in zip(output, regions):
                     
                        df.to_excel(excel_writer, sheet_name=reg, index=True)
                output = filename
            else:
                filename = 'ML_forecast_results_'+ region+'.xlsx'
                filtered_data = OIF(region=region,model_name=model_name,noOfSamples=future_prediction)
                output = io.BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                filtered_data.to_excel(writer, index=True, sheet_name='Sheet1')
                writer.close()  
                output.seek(0)

            return send_file(output, download_name=filename, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'error': str(e)}), 400
api.add_resource(OIF_Model, '/getdata')

if __name__ == '__main__':
    app.run(debug=True)
