from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


DBpassword = '' #for wamp it is default empty string
DBport = '3306'
DBusername = 'root'
DBhost = 'localhost'
DBname = 'ljms'

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DBusername}:{DBpassword}@{DBhost}:{DBport}/{DBname}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)


from backend_files.Course import course_retrieval
from backend_files.staff import staff_retrieval
from backend_files.role import role_retrieval
from backend_files.registration import registration_retrieval

from backend_files.jobrole import jobrole_manager
from backend_files.skill import skill_manager
from backend_files.skill import course_skill_linker
from backend_files.skill import jobrole_skills_linker
from backend_files.learningjourney import learningjourney_manager
from backend_files.learningjourney import learningjourney_course_linker




@app.route('/')
def home():
    return """
    <h1>Hello! this links are to test the backend, expect json files from them.</h1>
    <a href='/course'>get courses</a>
    <a href='/staff'>get staffs</a>
    <a href='/role'>get roles</a>
    <a href='/jobrole'>get jobroles</a>
    <a href='/skill'>get skills</a>
    <a href='/roleskill'>get roleskills</a>
    <a href='/courseskill'>get courseskills</a>
    <a href='/registration'>get registrations</a>
    <a href='/learningjourney'>get learningjourneys</a>
    <a href='/learningjourneycourse'>get learningjourneycourse</a>
    """



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)