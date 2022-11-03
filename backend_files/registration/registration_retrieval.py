from __main__ import app, db, Registration


from flask import jsonify


# get registrations
@app.route('/registration')
def registration():
    registrations = Registration.query.all()

    if len(registrations):
        return jsonify({"code": 200, "data": {"registrations": [
            registration.json() for registration in registrations]}})

    return jsonify(
        {
            "code": 404,
            "message": "There are no registrations."
        }
    ), 404
