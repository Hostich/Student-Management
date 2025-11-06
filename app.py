import sys
import os
sys.path.insert(0,'db/')
from db.dbhelper import * 
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session, flash, make_response,url_for

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENTIONS = {'png','jpg','jpeg','gif'}
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']='6a35534468a14e0ef04fe4c0d2cef645'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower()  in ALLOWED_EXTENTIONS 

@app.route("/")
def index()->None:
    school = getall('students')
    return  render_template('index.html', studentslist = school)

# @app.route("/loginvalidate",methods=['POST'])
# def loginvalidate()->None:
    # username:str = request.form['username']
    # password:str = request.form['password']
    # manage:list = getrecord('admin', username=username, password=password)
    # if len(manage)>0:
        # session['username'] = username
        # return redirect("/main")
    # else:
        # flash('Incorrect username and password','error')
        # return redirect("/")

@app.route("/addstudent",methods=['POST'])
def addstudent()->None:
    id:str = request.form['id']
    idno:str = request.form['idno']
    lastname:str = request.form['lastname']
    firstname:str = request.form['firstname']
    course:str = request.form['course']
    level:str = request.form['level']
    type:str = request.form['type']
    photo:str = request.files['photo']
    
    if not idno or not lastname or not firstname or not course or not level:
        flash("FILL OUT ALL THE FIELDS BEFORE SAVING", "error")
        return redirect("/")
    
    #This will get the filename of the photo and upload it safely into the folder 
    filename = None
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(UPLOAD_FOLDER, filename))
    
    #This store the filename/photo to the database    
    ok:bool = addrecord('students',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level,image=filename)
        
    
    if type=='add':
        ok:bool = addrecord('students',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level,image=filename)
    else:
        ok:bool = updaterecord('students',id=id,idno=idno,lastname=lastname,firstname=firstname,course=course,level=level)
    
    if ok==True:
        flash("Student Information Save","info")
    else:
        flash("Error Saving Student Information","error")
    return redirect("/")
    
    
@app.route("/deletestudent")
def deletestudent()->None:
    id:int = request.args.get('id')
    ok:bool = deleterecord('students',id=id)
    if ok==True:
        flash("Student Deleted","success")
    else:
        flash("Error Deleting Student","error")
    return redirect("/")
    
# @app.route("/")
# def main()->None:
        # school:list = getall('students')
        # return render_template('index.html', studentslist = school)

# @app.route('/logout')
# def logout():
    # session.pop('username', None) # Remove 'username' from session
    # flash('You are logged out','info')
    # return redirect("/")

# @app.after_request
# def cacheres(response):
    # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # response.headers["Pragma"] = "no-cache"
    # response.headers["Expries"] = "0"
    # return response
    
if __name__== "__main__":
    app.run(debug=True)