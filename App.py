#import statement
from flask import Flask,render_template,request,url_for,redirect
from pymongo import MongoClient
from bson import ObjectId
app=Flask(__name__)
password='12345678gh'
token='agdhdjeirn26383949'
token='abcdkdfjni1234345'
token='ufdifjdknkj234678'
password='agdjtyujeg'

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['Employee_db']
collection = db['Employee_collection']
#routing 
#index page
@app.route('/')
def index():
    return render_template('Login.html')

#authentication
@app.route('/login',methods=['POST'])
def login():
    User_name=request.form['username']
    Password=request.form['password']
    if(User_name=='' and Password=='123456'):
        return redirect(url_for('Show_Employee_Records'))
    else:
        error_message="OOPS! INVALID CREDENTIALS PROVIDED.\n Ensure that the username and password are correct."
        return render_template('Login.html',data=error_message)

#display  all records
@app.route('/employee_records')
def Show_Employee_Records():
    data=list(collection.find())
    return render_template("Employee_Records.html",data=data)

#inserting new record
@app.route('/register_employee',methods=['GET'])
def Register_Employee():
    return render_template("Register_Employee.html")

#handling input from form data
@app.route('/create',methods=['POST'])
def Add_Employee_Data():
    New_Employee={
        'Employee_Id':request.form['employee_id'],
        'First_Name':request.form['first_name'],
        'Last_Name':request.form['last_name'],
        'Email':request.form['email'],
        'Phone_Number':request.form['phone_number'],
        'Date_of_Hiring':request.form['hire_date'],
        'Job_Id':request.form['job_id'],
        'Salary':request.form['salary'],
        'Manager_Id':request.form['manager_id'],
        'Department_Id':request.form['department_id']
    }
    collection.insert_one(New_Employee)
    return redirect('/employee_records');

#update existing records
@app.route('/edit/<id>',methods=['GET'])
def Edit_Employee_Data(id):
    Data_to_be_edited=collection.find_one({'Employee_Id':id})
    return render_template('Edit_Employee_Data.html',data=Data_to_be_edited)

#fetching existing record for updating
@app.route('/update/<id>',methods=['POST'])
def Update_Employee_Data(id):
    Updated_Data={
        'Employee_Id':request.form['employee_id'],
        'First_Name':request.form['first_name'],
        'Last_Name':request.form['last_name'],
        'Email':request.form['email'],
        'Phone_Number':request.form['phone_number'],
        'Date_of_Hiring':request.form['hire_date'],
        'Job_Id':request.form['job_id'],
        'Salary':request.form['salary'],
        'Manager_Id':request.form['manager_id'],
        'Department_Id':request.form['department_id']
    }
    collection.update_one({'Employee_Id':id},{'$set':Updated_Data})
    return redirect('/employee_records');

#remove record
@app.route('/delete/<id>')
def Delete_Employee_Data(id):
    collection.delete_one({'Employee_Id':id})
    return redirect('/employee_records');

#filter based on employee id
@app.route('/filterbyemployeeid',methods=['POST'])
def  FilterByEmployeeId():
    emp_id=request.form['employee_id']
    item=list(collection.find({"Employee_Id":emp_id}));
    return render_template('Employee_Records.html',data=item)

#filter based on job id
@app.route('/filterbyjobid',methods=['POST'])
def FilterByJobId():
    job_id=request.form['job_id']
    item=list(collection.find({"Job_Id":job_id}))
    return render_template('Employee_Records.html',data=item)


if(__name__=='__main__'):
    app.run(debug=True)
