from flask import Flask, jsonify, render_template, session, redirect
from flask_security import Security, current_user
from flask_login import login_required, logout_user
import config
from models import db
from sec import store
from flask_restful import Api
import worker
import csv
from io import StringIO
from flask.wrappers import Response


app=None
api=None
celery=None

def initiate_app():
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    
    api=Api(app)
    app.app_context().push()

    celery=worker.celery
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        timezone=app.config['CELERY_TIMEZONE']
    )
    celery.Task=worker.ContextTask
    app.app_context().push()
    return app, api, celery 

app, api, celery=initiate_app()
security = Security(app, store)

    



# ************************************************************************************


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/user', methods=['GET'])
def get_user_info():
    if not current_user.is_authenticated:
        return jsonify(message="User not authenticated"), 401
    roles = [role.name for role in current_user.roles]

    return jsonify(response={
        'user_id': current_user.user_id,
        'username': current_user.username,
        'email': current_user.email,
        'roles': roles
    }), 200



@app.route("/export_halls", methods=["GET"])
@login_required
def export_halls():
    ufs = session["_user_id"]
    user=User.query.filter_by(fs_uniquifier=ufs).first()
    halls=Hall.query.filter_by(user_id=user.user_id).all()
    csv_text = StringIO()
    csv_file = csv.writer(csv_text, dialect="excel")
    csv_file.writerow(["hall_id", "hall_name", "place", "size", "show_id", "show_name", "time"])
    for h in halls:
        shows=Shows.query.filter_by(hall_id=h.hall_id).all()
        for s in shows:
            csv_file.writerow([h.hall_id, h.hall_name, h.place, h.size, s.show_id, s.show_name, s.time])
    return Response(csv_text.getvalue(), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=halls.csv"})


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/') 


from api import *
api.add_resource(registerAPI, '/api/register')
api.add_resource(HallManagerAPI, '/api/hall/<user_id>', '/api/hall/<user_id>/<hall_id>')
api.add_resource(ShowManagerAPI, '/api/shows/<user_id>/<hall_id>', '/api/shows/<user_id>/<hall_id>/<show_id>')
api.add_resource(getHallAPI, '/api/hall')
api.add_resource(getShowAPI, '/api/show/<hall_id>')
api.add_resource(BookingManagerAPI, "/api/booking/<user_id>", "/api/booking/<user_id>/<hall_id>/<show_id>", "/api/booking/<user_id>/<hall_id>/<show_id>/<booking_id>")



if __name__ == '__main__':
    app.run(debug=True)
    