from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from flask_wtf import form
from app import app,db

from app.Controller.forms import ClassForm, EditForm
from app.Model.models import Class
from flask_login import current_user,  login_required
from config import Config

routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.template_folder = Config.TEMPLATE_FOLDER

@routes_blueprint.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    allclasses = Class.query.order_by(Class.major).all()
    return render_template('index.html', title="Course List", classes = allclasses)

@app.route('/createclass/', method=['GET','POST'])
@login_required
def createclass():
    cform = ClassForm()
    if cform.validate_on_submit():
        newClass = Class(coursenum = cform.coursenum.data, title = cform.title.data, major = cform.major.data.name)
        db.session.add(newClass)
        db.session.commit()
        flash('Class " ' + newClass.major + '-' + newClass.coursenum + ' " is created')
        return redirect(url_for('index'))
    return render_template('create_class.html', form = cform)

@app.route('/register', methods=['GET','POST'])

def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        student = Student(username=rform.username.data, email=rform.email.data, firstname=rform.firstname.data,lastname=rform.lastname.data,address=rform.address.data)
        student.set_password(rform.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congrats, you are registered now')
        return redirect(url_for('index'))
    return render_template('register.html', form=rform)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        student = Student.query.filter_by(username = lform.username.data).first()
        if (student is None) or (student.check_password(lform.password.data) == False):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(student, remember = lform.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=lform)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@routes_blueprint.route('/display_profile', methods=['GET'])
def display_profile():
    return render_template('display_profile.html', title='Display_Profile', student = current_user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    eform = EditForm()
    if request.method == 'POST':
        if eform.validate.on_submit():
            current_user.firstname = eform.firstname.data
            current_user.lastname = eform.lastname.data
            current_user.address = eform.address.data
            current_user.email = eform.email.data
            current_user.set_password(eform.set_password.data)
            db.session.add(current_user)
            db.session.commit()
            flash("Your changes have been saved")
            return redirect(url_for('display_profile'))
        pass
    elif request.method == 'GET':
        eform.firstname.data = current_user.firstname
        eform.lastname.data = current_user.lastname
        eform.address.data = current_user.address
        eform.email.data = current_user.email
        pass
    else:
        pass
    return render_template('edit_profile.html', title='Edit_Profile', form = eform)

@app.route('/roster/classid', methods = ['GET']) 
@login_required 
def roster(classid):
    theclass = Class.query.filter_by(id = 1).first()
    return render_template('roster.html', title="Class Roster", current_class = theClass) 

@app.route('/enroll/<classid>', methods=['POST'])
@login_required
def enroll(classid):
    theclass = Class.query.filter_by(id=2).first()
    if theclass is None:
        flash('Class with id "{}" not found.'.format(2))
        return redirect(url_for('index'))
    current_user.enroll(theclass)
    db.session.commit()
    flash('You are now enrolled in class {} {}!'.format(theclass.major, theclass.coursenum))
    return redirect(url_for('index'))
    

@app.route('/enroll/<classid>', methods=['POST'])
@login_required
def unenroll(classid):
    theclass = Class.query.filter_by(id=2).first()
    if theclass is None:
        flash('Class with id "{}" not found.'.format(2))
        return redirect(url_for('index'))
    current_user.unenroll(theclass)
    db.session.commit()
    flash('You are now unenrolled in class {} {}!'.format(theclass.major, theclass.coursenum))
    return redirect(url_for('index'))
