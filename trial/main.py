"""Create me an employee registration application, where you can register a person with the following details using the UI
which will be created using HTML, CSS and JS. The backend should be in Python Flask. The details are:
EMPLOYEE ID
FIRST NAME
LAST NAME
EMAIL
PHONE NUMBER
HIRE DATE
JOB ID
EDUCATION
ADDRESS


The application should have the following functionalities:
1. Register a new employee  
2. Update an existing employee
3. Delete an existing employee
4. Get all the employees
5. Get a single employee by id
6. Get a single employee by name
7. Get a single employee by email
8. Get a single employee by phone number
9. Get a single employee by hire date

The application should have the following validations:
1. Employee id should be unique
2. Employee id should be a number
3. First name should be a string
4. Last name should be a string
5. Email should be a valid email
6. Phone number should be a valid phone number
7. Hire date should be a valid date
8. Job id should be a valid job id

The application should have the following error handling:
1. If the employee id is not unique, then return an error message saying that the employee id is not unique
2. If the employee id is not a number, then return an error message saying that the employee id is not a number
3. If the first name is not a string, then return an error message saying that the first name is not a string
4. If the last name is not a string, then return an error message saying that the last name is not a string
5. If the email is not a valid email, then return an error message saying that the email is not a valid email
6. If the phone number is not a valid phone number, then return an error message saying that the phone number is not a valid phone number
7. If the hire date is not a valid date, then return an error message saying that the hire date is not a valid date
8. If the job id is not a valid job id, then return an error message saying that the job id is not a valid job id

The application should have the following database operations:
1. Create a new employee
2. Update an existing employee
3. Delete an existing employee
4. Get all the employees
5. Get a single employee by id
6. Get a single employee by name
7. Get a single employee by email
8. Get a single employee by phone number
9. Get a single employee by hire date

The application should have the following database tables:
1. Employee
2. Employee_Education
3. Employee_Address
4. Employment_ID

The application should have the following database table columns:
1. Employee
    1. Employee ID(PRIMARY KEY)
    2. First Name
    3. Last Name
    4. Email
    5. Phone Number
    6. Gender
    
2. Employee_Education
    1. Employee ID(FOREIGN KEY)
    2. Education ID(PRIMARY KEY)
    3. Education Name
    4. Education Year
    5. MAJOR

3. Employee_Address
    1. Employee ID(FOREIGN KEY)
    2. Address ID(PRIMARY KEY)
    3. Address Line 1
    4. Address Line 2
    5. City
    6. State
    7. Zip Code
    8. Country

4. Employment_ID
    1. Employee ID(FOREIGN KEY)
    2. Employment ID(PRIMARY KEY)
    3. Company Name
    4. Start Date
    5. End Date
    6. Salary

The application should have the following database table constraints:
1. Employee
    1. Employee ID should be unique
    2. Employee ID should be a number
    3. First Name should be a string
    4. Last Name should be a string
    5. Email should be a valid email
    6. Phone Number should be a valid phone number
    7. Hire Date should be a valid date
    8. Job id should be a valid job id
    
2. Employee_Education
    1. Employee ID should be a number
    2. Education ID should be a number
    3. Education Name should be a string
    4. Education Year should be a number
    5. MAJOR should be a string
    
3. Employee_Address
    1. Employee ID should be a number
    2. Address ID should be a number
    3. Address Line 1 should be a string
    4. Address Line 2 should be a string
    5. City should be a string
    6. State should be a string
    7. Zip Code should be a number
    8. Country should be a string

4. Employment_ID
    1. Employee ID should be a number
    2. Employment ID should be a number
    3. Company Name should be a string
    4. Start Date should be a valid date
    5. End Date should be a valid date
    6. Salary should be a number

Also integrate the login functionality using JWT tokens. The login should be done using the following credentials:
1. Username: admin
2. Password: admin

The application should have the following functionalities:
1. Login
2. Logout
3. Register a new employee
4. Update an existing employee
5. Delete an existing employee
6. Get all the employees
7. Get a single employee by id
8. Get a single employee by name
9. Get a single employee by email
10. Get a single employee by phone number
11. Get a single employee by hire date
"""

# write code for the above mentioned application

# Path: main.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS
from datetime import datetime
import re
import secrets

secret_key = secrets.token_hex(16)  # Generate a random secret key


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:77278@localhost:3306/employee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.String(10), unique=True)
    hire_date = db.Column(db.Date)
    job_id = db.Column(db.Integer)
    education = db.relationship('EmployeeEducation', backref='employee', lazy=True)
    address = db.relationship('EmployeeAddress', backref='employee', lazy=True)
    employment = db.relationship('EmploymentID', backref='employee', lazy=True)

    def __init__(self, first_name, last_name, email, phone_number, hire_date, job_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.hire_date = hire_date
        self.job_id = job_id


class EmployeeEducation(db.Model):
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    education_id = db.Column(db.Integer, primary_key=True)
    education_name = db.Column(db.String(20))
    education_year = db.Column(db.Integer)
    major = db.Column(db.String(20))

    def __init__(self, employee_id, education_id, education_name, education_year, major):
        self.employee_id = employee_id
        self.education_id = education_id
        self.education_name = education_name
        self.education_year = education_year
        self.major = major


class EmployeeAddress(db.Model):
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    address_id = db.Column(db.Integer, primary_key=True)
    address_line1 = db.Column(db.String(20))
    address_line2 = db.Column(db.String(20))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.Integer)
    country = db.Column(db.String(20))

    def __init__(self, employee_id, address_id, address_line1, address_line2, city, state, zip_code, country):
        self.employee_id = employee_id
        self.address_id = address_id
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country


class EmploymentID(db.Model):
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
    employment_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    salary = db.Column(db.Integer)

    def __init__(self, employee_id, employment_id, company_name, start_date, end_date, salary):
        self.employee_id = employee_id
        self.employment_id = employment_id
        self.company_name = company_name
        self.start_date = start_date
        self.end_date = end_date
        self.salary = salary


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'job_id')


class EmployeeEducationSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'education_id', 'education_name', 'education_year', 'major')


class EmployeeAddressSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'address_id', 'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country')


class EmploymentIDSchema(ma.Schema):
    class Meta:
        fields = ('employee_id', 'employment_id', 'company_name', 'start_date', 'end_date', 'salary')

        
    
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

employee_education_schema = EmployeeEducationSchema()
employees_education_schema = EmployeeEducationSchema(many=True)

employee_address_schema = EmployeeAddressSchema()
employees_address_schema = EmployeeAddressSchema(many=True)

employment_id_schema = EmploymentIDSchema()
employments_id_schema = EmploymentIDSchema(many=True)


@app.route('/employee', methods=['POST'])
@jwt_required()
def add_employee():
    employee_id = request.json['employee_id']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    hire_date = request.json['hire_date']
    job_id = request.json['job_id']

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'message': 'Email is not valid'}), 400

    if not re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", hire_date):
        return jsonify({'message': 'Hire date is not valid'}), 400


    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if employee:
        return jsonify({'message': 'Employee id already exists'}), 400

    new_employee = Employee(first_name, last_name, email, phone_number, hire_date, job_id)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'message': 'Employee added successfully'}), 200


@app.route('/employee', methods=['GET'])
@jwt_required()
def get_all_employees():
    employees = Employee.query.all()
    result = employees_schema.dump(employees)
    return jsonify(result), 200

@app.route('/employee/<employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        return employee_schema.jsonify(employee), 200
    return jsonify({'message': 'Employee not found'}), 404

@app.route('/employee/<employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        employee.first_name = request.json['first_name']
        employee.last_name = request.json['last_name']
        employee.email = request.json['email']
        employee.phone_number = request.json['phone_number']
        employee.hire_date = request.json['hire_date']
        employee.job_id = request.json['job_id']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", employee.email):
            return jsonify({'message': 'Email is not valid'}), 400

        if not re.match(r"^[0-9]{10}$", employee.phone_number):
            return jsonify({'message': 'Phone number is not valid'}), 400

        if not re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", employee.hire_date):
            return jsonify({'message': 'Hire date is not valid'}), 400

        if not re.match(r"^[0-9]{4}$", employee.job_id):
            return jsonify({'message': 'Job id is not valid'}), 400

        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'}), 200
    return jsonify({'message': 'Employee not found'}), 404

@app.route('/employee/<employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    return jsonify({'message': 'Employee not found'}), 404


@app.route('/employee/name/<name>', methods=['GET'])
@jwt_required()
def get_employee_by_name(name):
    employee = Employee.query.filter_by(first_name=name).first()
    if employee:
        return employee_schema.jsonify(employee), 200
    return jsonify({'message': 'Employee not found'}), 404

@app.route('/employee/email/<email>', methods=['GET'])
@jwt_required()
def get_employee_by_email(email):
    employee = Employee.query.filter_by(email=email).first()
    if employee:
        return employee_schema.jsonify(employee), 200
    return jsonify({'message': 'Employee not found'}), 404


@app.route('/employee/phone/<phone_number>', methods=['GET'])
@jwt_required()
def get_employee_by_phone_number(phone_number):
    employee = Employee.query.filter_by(phone_number=phone_number).first()
    if employee:
        return employee_schema.jsonify(employee), 200
    return jsonify({'message': 'Employee not found'}), 404


@app.route('/employee/hire_date/<hire_date>', methods=['GET'])
@jwt_required()
def get_employee_by_hire_date(hire_date):
    employee = Employee.query.filter_by(hire_date=hire_date).first()
    if employee:
        return employee_schema.jsonify(employee), 200
    return jsonify({'message': 'Employee not found'}), 404


@app.route('/employee_education', methods=['POST'])
@jwt_required()
def add_employee_education():
    employee_id = request.json['employee_id']
    education_id = request.json['education_id']
    education_name = request.json['education_name']
    education_year = request.json['education_year']
    major = request.json['major']

    if not re.match(r"^[0-9]{4}$", employee_id):
        return jsonify({'message': 'Employee id is not valid'}), 400

    if not re.match(r"^[0-9]{4}$", education_id):
        return jsonify({'message': 'Education id is not valid'}), 400

    if not re.match(r"^[0-9]{4}$", education_year):
        return jsonify({'message': 'Education year is not valid'}), 400

    employee_education = EmployeeEducation.query.filter_by(employee_id=employee_id).first()
    if employee_education:
        return jsonify({'message': 'Employee id already exists'}), 400

    new_employee_education = EmployeeEducation(employee_id, education_id, education_name, education_year, major)
    db.session.add(new_employee_education)
    db.session.commit()

    return jsonify({'message': 'Employee education added successfully'}), 200


@app.route('/employee_education', methods=['GET'])
@jwt_required()
def get_all_employees_education():
    employees_education = EmployeeEducation.query.all()
    result = employees_education_schema.dump(employees_education)
    return jsonify(result), 200


@app.route('/employee_education/<employee_id>', methods=['GET'])
@jwt_required()
def get_employee_education(employee_id):
    employee_education = EmployeeEducation.query.get(employee_id)
    if employee_education:
        return employee_education_schema.jsonify(employee_education), 200
    return jsonify({'message': 'Employee education not found'}), 404

@app.route('/employee_education/<employee_id>', methods=['PUT'])
@jwt_required()
def update_employee_education(employee_id):
    employee_education = EmployeeEducation.query.get(employee_id)
    if employee_education:
        employee_education.education_name = request.json['education_name']
        employee_education.education_year = request.json['education_year']
        employee_education.major = request.json['major']

        if not re.match(r"^[0-9]{4}$", employee_education.education_year):
            return jsonify({'message': 'Education year is not valid'}), 400

        db.session.commit()
        return jsonify({'message': 'Employee education updated successfully'}), 200
    return jsonify({'message': 'Employee education not found'}), 404


@app.route('/employee_education/<employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee_education(employee_id):
    employee_education = EmployeeEducation.query.get(employee_id)
    if employee_education:
        db.session.delete(employee_education)
        db.session.commit()
        return jsonify({'message': 'Employee education deleted successfully'}), 200
    return jsonify({'message': 'Employee education not found'}), 404


@app.route('/employee_address', methods=['POST'])
@jwt_required()
def add_employee_address():
    employee_id = request.json['employee_id']
    address_id = request.json['address_id']
    address_line1 = request.json['address_line1']
    address_line2 = request.json['address_line2']
    city = request.json['city']
    state = request.json['state']
    zip_code = request.json['zip_code']
    country = request.json['country']

    if not re.match(r"^[0-9]{4}$", employee_id):
        return jsonify({'message': 'Employee id is not valid'}), 400

    if not re.match(r"^[0-9]{4}$", address_id):
        return jsonify({'message': 'Address id is not valid'}), 400

    if not re.match(r"^[0-9]{6}$", zip_code):
        return jsonify({'message': 'Zip code is not valid'}), 400

    employee_address = EmployeeAddress.query.filter_by(employee_id=employee_id).first()
    if employee_address:
        return jsonify({'message': 'Employee id already exists'}), 400

    new_employee_address = EmployeeAddress(employee_id, address_id, address_line1, address_line2, city, state, zip_code, country)
    db.session.add(new_employee_address)
    db.session.commit()

    return jsonify({'message': 'Employee address added successfully'}), 200

@app.route('/employee_address', methods=['GET'])
@jwt_required()
def get_all_employees_address():
    employees_address = EmployeeAddress.query.all()
    result = employees_address_schema.dump(employees_address)
    return jsonify(result), 200


@app.route('/employee_address/<employee_id>', methods=['GET'])
@jwt_required()
def get_employee_address(employee_id):
    employee_address = EmployeeAddress.query.get(employee_id)
    if employee_address:
        return employee_address_schema.jsonify(employee_address), 200
    return jsonify({'message': 'Employee address not found'}), 404


@app.route('/employee_address/<employee_id>', methods=['PUT'])
@jwt_required()
def update_employee_address(employee_id):
    employee_address = EmployeeAddress.query.get(employee_id)
    if employee_address:
        employee_address.address_line1 = request.json['address_line1']
        employee_address.address_line2 = request.json['address_line2']
        employee_address.city = request.json['city']
        employee_address.state = request.json['state']
        employee_address.zip_code = request.json['zip_code']
        employee_address.country = request.json['country']

        if not re.match(r"^[0-9]{6}$", employee_address.zip_code):
            return jsonify({'message': 'Zip code is not valid'}), 400

        db.session.commit()
        return jsonify({'message': 'Employee address updated successfully'}), 200
    return jsonify({'message': 'Employee address not found'}), 404

@app.route('/employee_address/<employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee_address(employee_id):
    employee_address = EmployeeAddress.query.get(employee_id)
    if employee_address:
        db.session.delete(employee_address)
        db.session.commit()
        return jsonify({'message': 'Employee address deleted successfully'}), 200
    return jsonify({'message': 'Employee address not found'}), 404


@app.route('/employment_id', methods=['POST'])
@jwt_required()
def add_employment_id():
    employee_id = request.json['employee_id']
    employment_id = request.json['employment_id']
    company_name = request.json['company_name']
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    salary = request.json['salary']

    if not re.match(r"^[0-9]{4}$", employee_id):
        return jsonify({'message': 'Employee id is not valid'}), 400

    if not re.match(r"^[0-9]{4}$", employment_id):
        return jsonify({'message': 'Employment id is not valid'}), 400

    if not re.match(r"^[0-9]{4}$", salary):
        return jsonify({'message': 'Salary is not valid'}), 400

    employment_id = EmploymentID.query.filter_by(employee_id=employee_id).first()
    if employment_id:
        return jsonify({'message': 'Employee id already exists'}), 400

    new_employment_id = EmploymentID(employee_id, employment_id, company_name, start_date, end_date, salary)
    db.session.add(new_employment_id)
    db.session.commit()

    return jsonify({'message': 'Employment id added successfully'}), 200

@app.route('/employment_id', methods=['GET'])
@jwt_required()
def get_all_employments_id():
    employments_id = EmploymentID.query.all()
    result = employments_id_schema.dump(employments_id)
    return jsonify(result), 200

@app.route('/employment_id/<employee_id>', methods=['GET'])
@jwt_required()
def get_employment_id(employee_id):
    employment_id = EmploymentID.query.get(employee_id)
    if employment_id:
        return employment_id_schema.jsonify(employment_id), 200
    return jsonify({'message': 'Employment id not found'}), 404


@app.route('/employment_id/<employee_id>', methods=['PUT'])
@jwt_required()
def update_employment_id(employee_id):
    employment_id = EmploymentID.query.get(employee_id)
    if employment_id:
        employment_id.company_name = request.json['company_name']
        employment_id.start_date = request.json['start_date']
        employment_id.end_date = request.json['end_date']
        employment_id.salary = request.json['salary']

        if not re.match(r"^[0-9]{4}$", employment_id.salary):
            return jsonify({'message': 'Salary is not valid'}), 400

        db.session.commit()
        return jsonify({'message': 'Employment id updated successfully'}), 200
    return jsonify({'message': 'Employment id not found'}), 404

@app.route('/employment_id/<employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employment_id(employee_id):
    employment_id = EmploymentID.query.get(employee_id)
    if employment_id:
        db.session.delete(employment_id)
        db.session.commit()
        return jsonify({'message': 'Employment id deleted successfully'}), 200
    return jsonify({'message': 'Employment id not found'}), 404


@app.route('/login', methods=['POST'])
def login():

    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username != 'admin' or password != 'admin':
        return jsonify({"message": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)


