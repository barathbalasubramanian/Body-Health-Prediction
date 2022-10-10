from flask import *
from flask import Flask, render_template,request ,flash
from flask_session.__init__ import Session
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pyrebase
import random
import joblib

config = {
    'apiKey': "AIzaSyD-kru0iiBzp688ccRoHqv-uMpl8RrC9Is",
    'authDomain': "engineering-sprints.firebaseapp.com",
    'databaseURL': "https://engineering-sprints-default-rtdb.firebaseio.com",
    'projectId': "engineering-sprints",
    'storageBucket': "engineering-sprints.appspot.com",
    'messagingSenderId': "561728301144",
    'appId': "1:561728301144:web:eca61c6e3ed6630c35822d",
    'measurementId': "G-3MSDDQNM7P"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
sess = Session()

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'super secret key'
# db = firebase.database()
cred = credentials.Certificate("file.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/index',methods=['POST'])
def form():
    return render_template('index.html')

@app.route('/login_validation',methods = ['POST'])
def login_validation():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            error = ' Login Succesful '
            return render_template('fill.html' ,error=error)
        except:
            error = None
            if request.form['pass'] != 'jtp':
                error = "INVALID PASSWORD OR USERNAME"  
                return render_template('index.html',error=error)
            return render_template('index.html')

@app.route('/register_validation' ,methods = ['POST'])
def register_validation():
    if request.method == 'POST':
            reg_email = request.form.get('email')
            password = request.form.get('f_pass')
            con_password = request.form.get('c_pass')
            if password == con_password :
                try :
                    user = auth.create_user_with_email_and_password(reg_email,password)

                except :
                    error = ' This E-mail was Already Registered'
                    return render_template('/register.html',error=error)
            else :
                error = 'Password is Unmatch'
                return render_template('/register.html',error=error)
    return render_template('/index.html')

@app.route('/last', methods=['POST'])
def collection() :
    bmi_list = []
    diabetes_list = []
    heart_list = []
    stroke_list = []
    diabetestype = ['1 Insulin Dependent Diabetes Mellitus',' 2 Adult-Onset Diabetes']
    if request.method == 'POST' :
        gender =  request.form.get('gender')
        if gender == ['MALE'] : gender = 1
        else : gender = 0
        age = request.form.get('age')
        weight = request.form.get('weight')
        height = request.form.get('height')
        print(type(height),type(weight))
        gl = request.form.get('quantity')
        # sugar = request.form.get('sugar')
        # if sugar == ['YES'] : sugar = 1 
        # else : sugar = 0
        # heart = request.form.get('heart')
        # if heart == ['YES'] : heart = 1 
        # else : heart = 0
        BloodPressure = request.form.get('pressure')
        ChestPainType = request.form.get('ChestPainType')
        if ChestPainType == ['ATA'] : ChestPainType = 1 
        elif ChestPainType == ['ASY'] : ChestPainType = 2
        elif ChestPainType == ['NAP'] : ChestPainType = 3 
        else : ChestPainType = 4
        Cholesterol = request.form.get('cholesterol')
        ExerciseAngina = request.form.get('exercise')
        if ExerciseAngina == ['YES']: ExerciseAngina = 1 
        else : ExerciseAngina = 0
        hypertension = request.form.get('hpt')
        if hypertension == ['YES'] : hypertension = 1 
        else : hypertension = 0
        smoking_status = request.form.get('smoke')
        if smoking_status == 'UNKNOWN' : smoking_status = 0 
        elif smoking_status == 'SMOKES' : smoking_status = 3 
        elif smoking_status == 'NEVER SMOKE' : smoking_status = 1
        else : smoking_status = 2
        height_in_inches = 0.394*int(height)
        print(height_in_inches,'height')
        weight_in_pounds = 2.205 * int(weight)
        print(weight_in_pounds,'weight')
#         db.collection('persons').add({'age':age,'weight':weight,'height':height,'glucose level':gl})
        error = 'SUCCESSFULLY REGISTERED'
        # BMI
        bmi_list.append([gender,int(age),round(height_in_inches),round(weight_in_pounds)])
        model = joblib.load('trained_bmi_new.joblib')
        print(bmi_list,1)
        pred_bmi = model.predict(bmi_list)
        pred_bmi = pred_bmi[0]
        print(pred_bmi,'bmi')
        pred_bmi = (int(weight) / (int( height) *  int(height))) * 10000       
        pred_bmi = round(pred_bmi,2)
        # DIABETES
        diabetes_list.append([int(age),int(gl),int(BloodPressure),round(pred_bmi)])
        model = joblib.load('trained_diabetes.joblib')
        print(diabetes_list,2)
        pred_diabetes = model.predict(diabetes_list)
        pred_diabetes= pred_diabetes[0]
        print(pred_diabetes,'diabetes')
        if pred_diabetes == 1  : 
            if int(age) > 40 and pred_bmi > 25 : 
                diabetestype = diabetestype[0]
            elif int(age) < 40 and pred_bmi > 25 :
                diabetestype = diabetestype[1]
            else :
                diabetestype = ' 1 BUT IT CAN EASILY CURABLE'
        # HEART
        heart_list.append([int(age),gender,ChestPainType,int(BloodPressure),int(Cholesterol),ExerciseAngina])
        model = joblib.load('trained_heart.joblib')
        print(heart_list)
        pred_heart = model.predict(heart_list)
        pred_heart = pred_heart[0]
        print(pred_heart,'heart')
        # stroke
        stroke_list.append([int(gl),gender,int(age),int(hypertension),pred_heart,round(pred_bmi,1),smoking_status])
        model = joblib.load('trained_stroke.joblib')
        print(stroke_list)
        pred_stroke = model.predict(stroke_list)
        pred_stroke = pred_stroke[0]
        print(pred_stroke,'stroke')
        if pred_diabetes == 1 : pred_diabetes = 'YES' ; 
        else : pred_diabetes = 'NO'
        if pred_heart == 1 : pred_heart = 'YES' ; 
        else : pred_heart = 'NO'
        if pred_stroke == 1 : pred_stroke = 'YES' ; 
        else : pred_stroke = 'NO'
        return render_template('/last.html',error=error,pred_bmi=pred_bmi,pred_diabetes=pred_diabetes,pred_heart=pred_heart,pred_stroke=pred_stroke,diabetestype=diabetestype)

if __name__ == '__main__':
    sess.init_app(app)
    app.run(debug=True,host='0.0.0.0',port = 5000)


