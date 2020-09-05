import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_app, Patient, Doctor


class HospitalTestCases(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        setup_app(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.patient_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im93MjVwTjVXQ3lWV0FpcDVKNEZBVCJ9.eyJpc3MiOiJodHRwczovL2VuZy1hdXRoLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjUyNWZiYmM2NDc4YjAwNjdkOTA3MWMiLCJhdWQiOiJIb3NwaXRhbF9BUEkiLCJpYXQiOjE1OTkyOTI2NjEsImV4cCI6MTU5OTM3OTA2MSwiYXpwIjoiOXFFZ1hqbHJ5b0hsV1FEdElSSGdMTlRSYlJ2elB0ZmgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpwYXRpZW50Il19.wO9WTPt8kZ8mE6MlrfX_1MyrkTVgS5HdIW2oyR3-mh6L0YTEcLoeI9qF8pfJ6FS3UkXgoCTb4vC71ZgTbYmOhY58Gk0mOI0MTQr1GGagBbHjfMt9GcfCTqBqkZWWNrYUK_y2NqwPMWVWDCK25Eg8C2F_77Jj0yO55bJbKII2zsXj0lGZNdPe0f1JcC_3JPWfb9KmX9u2ksrvGRyEG5yLSQCjuMwt-Fv0Mj507XN3kZwvL-JAAq1dZniuktDE4chMosAPtPN5LtpY3QUQ7JH6e-1Y8manvS4Y-OM1eY6kzdAyyVJVc_tYrYg2yw4hay_0Tx3jSBuFDh_J7Outc9ln5g'
        self.doctor_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im93MjVwTjVXQ3lWV0FpcDVKNEZBVCJ9.eyJpc3MiOiJodHRwczovL2VuZy1hdXRoLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjUyNWY3OTIwNzZhNzAwNjc4ZjdjMTIiLCJhdWQiOiJIb3NwaXRhbF9BUEkiLCJpYXQiOjE1OTkyOTQxMDYsImV4cCI6MTU5OTM4MDUwNiwiYXpwIjoiOXFFZ1hqbHJ5b0hsV1FEdElSSGdMTlRSYlJ2elB0ZmgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpwYXRpZW50IiwiZ2V0OmFsbF9wYXRpZW50cyIsImdldDpkb2N0b3IiLCJnZXQ6cGF0aWVudCIsInBvc3Q6cGF0aWVudCIsInB1dDpwYXRpZW50Il19.6BxBWfIOXqaNuH_rsH2xL0zXYQWYLxvmBwqX_4o2_QkuqAAzA6iQzsb7UB0UEpZytpYuh0BzP3DGzFLd2CH2cTWXu8_OI0v1EWNJQL-YzG-_YwjtOqdwgKiRF1BedvciIVLwEiW5CotJxVnDnmQMXgrAiMAkPBLSxqnERDGU5o8Jpc712KHLUhjJnQw01yl8Dt1LYc6Fj4KlZgwy2qxCIBj7F9olXSrgTQbmeTvYBc7pDqZ9NSZtuns3Ig-WMERm84tl9fuWT2X_vG2UQ0qbAY0WqGzIoGQXGF1QIeJ9vaGsHTrY2sXms2yZiMmFyYYzC4OdpaEiUeg15MWEWYIeTQ'

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_patients(self):
        res = self.client().get('/patients', headers={'Authorization': self.patient_token})
        self.assertEqual(res.status_code, 500)

    def test_get_patient(self):
        p = Patient.query.first()
        _id = p.id
        res = self.client().get('/patients/' + str(_id), headers={'Authorization': self.patient_token})
        self.assertEqual(res.status_code, 200)

    def test_404_get_patient(self):
        res = self.client().get('/patients/10000', headers={'Authorization': self.patient_token})
        self.assertEqual(res.status_code, 404)

    def test_create_patient(self):
        doctor = Doctor.query.first()
        patient = {
            "name": "patient50",
            "age": 50,
            "address": "Cairo-Egypt",
            "email": "patient50@example.com",
            "examine_report": "cancer ",
            "doctor_id": doctor.id
        }
        res = self.client().post('/patients', json=patient, headers={'Authorization': self.patient_token})
        self.assertEqual(res.status_code, 500)

    # def test_404_create_patient(self):
    #     patient = {
    #         "name": "patient55",
    #         "age": 50,
    #         "address": "Cairo-Egypt",
    #         "email": "patient55@example.com",
    #         "examine_report": "cancer ",
    #         "doctor_id": 10000
    #     }
    #     res = self.client().post('/patients', json=patient, headers={'Authorization': self.patient_token})
    #     self.assertEqual(res.status_code, 500)

    def test_update_patient(self):
        p = Patient.query.first()
        _id = p.id
        patient = {
            "name": "patient60",
            "age": 50,
            "address": "Cairo-Egypt",
            "email": "patient60@example.com",
            "examine_report": "cancer ",
            "doctor_id": p.doctor.id
        }
        res = self.client().put('/patients/' + str(_id), json=patient, headers={'Authorization': self.patient_token})
        self.assertEqual(res.status_code, 500)

    # def test_404_update_patient(self):
    #     _id = 10000
    #     patient = {
    #         "name": "patient60",
    #         "age": 50,
    #         "address": "Cairo-Egypt",
    #         "email": "patient60@example.com",
    #         "examine_report": "cancer ",
    #         "doctor_id": 10
    #     }
    #     res = self.client().put('/patients/' + str(_id), json=patient, headers={'Authorization': self.patient_token})
    #     self.assertEqual(res.status_code, 500)

    def test_delete_patient(self):
        p = Patient.query.first()
        _id = p.id
        patient = {
            "name": "patient60",
            "age": 50,
            "address": "Cairo-Egypt",
            "email": "patient60@example.com",
            "examine_report": "cancer ",
            "doctor_id": p.doctor.id
        }
        res = self.client().delete('/patients/' + str(_id), headers={'Authorization': self.patient_token})
        self.assertEqual(res.status_code, 500)

    # --------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------#
    def test_get_all_patients(self):
        res = self.client().get('/patients', headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 200)

    def test_get_patient(self):
        p = Patient.query.first()
        _id = p.id
        res = self.client().get('/patients/' + str(_id), headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 200)

    def test_404_get_patient(self):
        res = self.client().get('/patients/10000', headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 404)

    def test_create_patient(self):
        doctor = Doctor.query.first()
        patient = {
            "name": "patient50",
            "age": 50,
            "address": "Cairo-Egypt",
            "email": "patient50@example.com",
            "examine_report": "cancer ",
            "doctor_id": doctor.id
        }
        res = self.client().post('/patients', json=patient, headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 200)

    def test_404_create_patient(self):
        patient = {
            "name": "patient55",
            "age": 50,
            "address": "Cairo-Egypt",
            "email": "patient55@example.com",
            "examine_report": "cancer ",
            "doctor_id": 10000
        }
        res = self.client().post('/patients', json=patient, headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 404)

    def test_update_patient(self):
        p = Patient.query.first()
        _id = p.id
        patient = {
            "name": "patient60",
            "age": 50,
            "address": "Cairo-Egypt",
            "email": "patient60@example.com",
            "examine_report": "cancer ",
            "doctor_id": p.doctor.id
        }
        res = self.client().put('/patients/' + str(_id), json=patient, headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 200)

    def test_404_update_patient(self):
        _id = 10000
        patient = {
            "name": "patient60",
            "age": 50,
            "address": "Cairo-Egypt",
            "email": "patient60@example.com",
            "examine_report": "cancer ",
            "doctor_id": 10
        }
        res = self.client().put('/patients/' + str(_id), json=patient, headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 404)

    def test_delete_patient(self):
        p = Patient.query.first()
        _id = p.id
        patient = {
            "name": "patient60",
            "age": 50,
            "address": "Cairo-Egypt",
            "email": "patient60@example.com",
            "examine_report": "cancer ",
            "doctor_id": p.doctor.id
        }
        res = self.client().delete('/patients/' + str(_id), headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 200)



    def test_get_all_doctors(self):
        res = self.client().get('/doctors', headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 500)

    def test_get_doctor(self):
        d = Doctor.query.first()
        _id = d.id
        res = self.client().get('/doctors/' + str(_id), headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 200)

    def test_404_get_doctors(self):
        res = self.client().get('/doctors/10000', headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 404)

    def test_create_doctors(self):
        doctor = {
           "name": "doctor40",
           "address": "Asharqia-Egypt",
           "salary": 2500,
           "email": "doctor40@example.com"
        }
        res = self.client().post('/doctors', json=doctor, headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 500)

    def test_update_doctor(self):
        d = Doctor.query.first()
        _id = d.id
        doctor = {
            "name": d.name,
            "address": "Asharqia-Egypt",
            "salary": 2500,
            "email": d.email
        }
        res = self.client().post('/doctors/'+str(_id), json=doctor, headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 405)

    # def test_404_update_doctor(self):
    #     _id = 10000
    #     doctor = {
    #         "name": "doctor40",
    #         "address": "Asharqia-Egypt",
    #         "salary": 2500,
    #         "email": "doctor40@example.com"
    #     }
    #     res = self.client().post('/doctors/' + str(_id), json=doctor, headers={'Authorization': self.doctor_token})
    #     self.assertEqual(res.status_code, 404)

    def test_delete_doctor(self):
        p = Doctor.query.first()
        _id = p.id
        res = self.client().delete('/doctors/' + str(_id), headers={'Authorization': self.doctor_token})
        self.assertEqual(res.status_code, 500)


if __name__ == "__main__":
    unittest.main()
