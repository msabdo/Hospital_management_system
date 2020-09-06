from flask_sqlalchemy import SQLAlchemy

# database_name = 'hospital_management'
# database_path = "postgres://{}:{}@{}/{}".format('postgres', 'root', 'localhost:5432', database_name)
database_path = 'postgres://plbmlrvknliolr:fabd3bda8491555ab1cfc0537c36ec14e91d77bf7121529ef82aa6662e5691de@ec2-34-238-26-109.compute-1.amazonaws.com:5432/df2vb936auvtnv'
db = SQLAlchemy()


def setup_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    # db.drop_all()
    db.create_all()


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String(120))
    salary = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    patients = db.relationship('Patient', backref=db.backref('doctor'))

    def __init__(self, name, address, salary, email):
        self.name = name
        self.address = address
        self.salary = salary
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        self.name = data["name"]
        self.address = data["address"]
        self.salary = data["salary"]
        self.email = data["email"]
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short_format(self):
        return {
            "name": self.name,
            "email": self.email
        }

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "salary": self.salary,
            "email": self.email
        }


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(120))
    email = db.Column(db.String(100),  unique=True)
    examine_report = db.Column(db.String)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __init__(self, name, age, address, email, examine_report):
        self.name = name
        self.age = age
        self.address = address
        self.email = email
        self.examine_report = examine_report

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        self.name = data["name"]
        self.age = data["age"]
        self.address = data["address"]
        self.email = data["email"]
        self.examine_report = data["examine_report"]
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "address": self.address,
            "email": self.email,
            "examine_report": self.examine_report,
            "doctor": Doctor.query.get(self.doctor_id).short_format()
        }