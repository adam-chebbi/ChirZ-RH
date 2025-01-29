from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from models import db, User, CV, JD, MatchResult
from matching_algorithm import match_cv_with_jd
import os

routes = Blueprint('routes', __name__)

def register_routes(app):
    app.register_blueprint(routes)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@routes.route('/upload_cv', methods=['GET', 'POST'])
def upload_cv():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        if file:
            cv = CV(filename=file.filename, data=file.read(), user_id=session['user_id'])
            db.session.add(cv)
            db.session.commit()
            flash('CV uploaded successfully')
    return render_template('upload_cv.html')

@routes.route('/upload_jd', methods=['GET', 'POST'])
def upload_jd():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        text = request.form['text']
        jd = JD(text=text, user_id=session['user_id'])
        db.session.add(jd)
        db.session.commit()
        flash('JD uploaded successfully')
    return render_template('upload_jd.html')

@routes.route('/match', methods=['GET', 'POST'])
def match():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        cv_id = int(request.form['cv_id'])
        jd_id = int(request.form['jd_id'])
        cv = CV.query.get(cv_id)
        jd = JD.query.get(jd_id)
        if cv and jd:
            match_result = match_cv_with_jd(cv, jd)
            db.session.add(match_result)
            db.session.commit()
            # Fetch updated list of CVs and JDs for the form
            cvs = CV.query.filter_by(user_id=session['user_id']).all()
            jds = JD.query.filter_by(user_id=session['user_id']).all()
            return render_template('match.html', cvs=cvs, jds=jds, match_result=match_result)
    cvs = CV.query.filter_by(user_id=session['user_id']).all()
    jds = JD.query.filter_by(user_id=session['user_id']).all()
    return render_template('match.html', cvs=cvs, jds=jds)

@routes.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['user_id'] != 1:  # Assuming admin is user with ID 1
        return redirect(url_for('login'))
    cvs = CV.query.all()
    jds = JD.query.all()
    match_results = MatchResult.query.all()
    return render_template('admin_dashboard.html', cvs=cvs, jds=jds, match_results=match_results)

@routes.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    match_results = MatchResult.query.join(CV).filter(CV.user_id == session['user_id']).all()
    return render_template('user_dashboard.html', match_results=match_results)