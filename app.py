# from flask_cors import CORS
from flask import Flask, jsonify, request, json
from models import setup_app, db_drop_and_create_all, Patient, Doctor
from sqlalchemy.exc import IntegrityError
from auth import requires_auth

app = Flask(__name__)
setup_app(app)


# CORS(app)
# db_drop_and_create_all()

# ------------------------ patients routes ---------------#
@app.route('/')
def login():
    return request.args.get('access_token')


@app.route('/patients')
@requires_auth(permission='get:all_patients')
def get_all_patients():
    patients_list = []
    try:
        patients = Patient.query.all()
        if not patients:
            return jsonify({
                "success": True,
                "description": "patients not found"
            }), 404
    except Exception as err:
        print("get all patients: ", err)
        return jsonify({"success": False}), 500

    for patient in patients:
        # doctor = Doctor.query.get(patient.doctor_id).short_format()
        patients_list.append(patient.format())

    return jsonify({
        "success": True,
        "patients": patients_list
    }), 200


@app.route('/patients/<int:patient_id>')
@requires_auth(permission='get:patient')
def get_patient(patient_id):

    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({
                "success": True,
                "description": "patient not found"
            }), 404

    except Exception as err:
        print("get patient: ", err)
        return jsonify({"success": False}), 500

    return jsonify({
        "success": True,
        "patient": patient.format()
    }), 200


@app.route('/patients', methods=['POST'])
@requires_auth(permission='post:patient')
def create_patient():
    patient_data = json.loads(request.data)

    doctor = Doctor.query.get(patient_data['doctor_id'])
    if not doctor:
        return jsonify({
            "success": False,
            "description": "doctor id not found"
        }), 404

    patient = Patient(
        name=patient_data["name"],
        age=patient_data["age"],
        address=patient_data["address"],
        email=patient_data["email"],
        examine_report=patient_data["examine_report"],
    )
    patient.doctor = doctor
    try:
        patient.insert()
    except IntegrityError as err:
        print(err)
        return jsonify({
            "success": False,
            "description": "there is patient with the same email"
        }), 200
    # except Exception as err:
    #     print(err)
    #     return jsonify({"success": False}), 500

    return jsonify({
        "success": True,
        "patient": Patient.query.get(patient.id).format()
    }), 200


@app.route('/patients/<int:patient_id>', methods=['PUT'])
@requires_auth(permission='put:patient')
def update_patient(patient_id):
    patient_data = json.loads(request.data)
    doctor = Doctor.query.get(patient_data['doctor_id'])

    if not doctor:
        return jsonify({
            "success": False,
            "description": "doctor id not found"
        }), 404
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({
                "success": True,
                "description": "patient not found"
            }), 404
        else:
            patient.doctor = doctor
            patient.update(patient_data)
    except IntegrityError:
        return jsonify({
            "success": False,
            "description": "there is patient with the same email"
        }), 200

    except Exception as err:
        print("doctor update: ", err)
        return jsonify({"success": False}), 500

    return jsonify({
        "success": True,
        "patient": patient.format()
    }), 200


@app.route('/patients/<int:patient_id>', methods=['DELETE'])
@requires_auth(permission='delete:patient')
def delete_patient(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({
                "success": True,
                "description": "patient already not found"
            }), 200
        else:
            patient.delete()
    except Exception:
        return jsonify({"success": False}), 500

    return jsonify({
        "success": True,
        "patient_id ": patient_id
    }), 200


# ------------------------------------------------------------------------------#
# ------------------------------------ doctors routes ---------------------------#
@app.route('/doctors')
@requires_auth(permission='get:all_doctors')
def get_all_doctors():
    doctors_list = []
    try:
        doctors = Doctor.query.all()
        if not doctors:
            return jsonify({
                "success": True,
                "description": "doctors not found"
            }), 404
    except Exception:
        return jsonify({"success": False}), 500

    for doctor in doctors:
        doctors_list.append(doctor.format())

    return jsonify({
        "success": True,
        "doctors": doctors_list
    }), 200


@app.route('/doctors/<int:doctor_id>')
@requires_auth(permission='get:doctor')
def get_doctor(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({
                "success": True,
                "description": "doctor not found"
            }), 404

    except Exception:
        return jsonify({"success": False}), 500

    return jsonify({
        "success": True,
        "doctor": doctor.format()
    }), 200


@app.route('/doctors', methods=['POST'])
@requires_auth(permission='post:doctor')
def create_doctor():
    doctor_data = json.loads(request.data)
    doctor = Doctor(
        name=doctor_data["name"],
        address=doctor_data["address"],
        salary=doctor_data["salary"],
        email=doctor_data["email"]
    )
    try:
        doctor.insert()
    except IntegrityError:
        return jsonify({
            "success": False,
            "description": "there is doctor with the same email"
        })
    except Exception :
        return jsonify({"success": False}), 500

    return jsonify({
        "success": True,
        "doctor": doctor.format()
    }), 200


@app.route('/doctors/<int:doctor_id>', methods=['PUT'])
@requires_auth(permission='put:doctor')
def update_doctors(doctor_id):
    doctor_data = json.loads(request.data)
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({
                "success": True,
                "description": "doctor not found"
            }), 404
        else:
            doctor.update(doctor_data)
    except Exception:
        return jsonify({"success": False}), 500

    return jsonify({
        "success": True,
        "patient": doctor.format()
    }), 200


@app.route('/doctors/<int:doctor_id>', methods=['DELETE'])
@requires_auth(permission='delete:doctor')
def delete_doctor(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({
                "success": True,
                "description": "doctor already not found"
            }), 200
        else:
            doctor.delete()
    except IntegrityError as err:
        print("delete doctor: ", err)
        return jsonify({
            "success": False,
            "description": "cannot delete doctor 'he has patients', please reassign the patients "
        }), 500

    except Exception as err:
        print("delete doctor: ", err)
        return jsonify({"success": False}), 500

    return jsonify({
        "success": True,
        "doctor_id ": doctor_id
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(500)
def auth_error(auth_error):
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error['description']
        }), auth_error.status_code


@app.errorhandler(401)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "not authenticated"
                    }), 401


if __name__ == '__main__':
    app.run(debug=True)

