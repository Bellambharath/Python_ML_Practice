from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

student = [{
    "name": "Bharath",
    "rollno": 1,
    "section": "A"
}, {
    "name": "abcd",
    "rollno": 2,
    "section": "B"
}]

class StudentList(Resource):
    @swag_from({
        'parameters': [
            {
                'name': 'name',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Name of the student'
            },
            {
                'name': 'rollno',
                'in': 'query',
                'type': 'integer',
                'required': True,
                'description': 'Roll number of the student'
            },
            {
                'name': 'section',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Section of the student'
            }
        ],
        'responses': {
            200: {
                'description': 'A list of students matching the query parameters',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'std': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'name': {'type': 'string'},
                                    'rollno': {'type': 'integer'},
                                    'section': {'type': 'string'}
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
        name = request.args.get('name')
        rollno = request.args.get('rollno')
        section = request.args.get('section')

        if not name or not rollno or not section:
            return {"message": "Missing required query parameters"}, 400

        rollno = int(rollno)  # Convert rollno to integer

        result = [stu for stu in student if stu['name'] == name and stu['rollno'] == rollno and stu['section'] == section]
        return jsonify({"std": result})


class Withparams(Resource):
    @swag_from({
        'parameters':[
            {
                'name': 'rollno',
                'in': 'query',
                'type': 'integer',
                'required': True,
                'description': 'rollno of the student'
            },
           
        ],
        'responses':{
            200:{
                'description':'list of student with roll no',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'std': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'name': {'type': 'string'},
                                    'rollno': {'type': 'integer'},
                                    'section': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            },
            400:{
                'description': 'Invalid input'
            }
        }
    })
    def get(self):
        rollno = request.args.get('rollno')
        if not rollno:
            return {"message":"please provide input"},400
        rollno = int(rollno)
        st = [stud for stud in student if stud['rollno'] == rollno]
        return jsonify({'student':st})


api.add_resource(StudentList, '/getstudent')
api.add_resource(Withparams , '/get')

if __name__ == '__main__':
    app.run(debug=True)
