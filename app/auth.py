from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import Professor, Aluno
from . import db, login_manager

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    try:
        tipo, id = user_id.split("_")
        if tipo == "prof":
            return Professor.query.get(int(id))
        elif tipo == "aluno":
            return Aluno.query.get(int(id))
    except:
        return None

@auth.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')

        user = None
        if tipo == "professor":
            user = Professor.query.filter_by(email=email).first()
        elif tipo == "aluno":
            user = Aluno.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            if user.is_professor():
                return redirect(url_for('main.dashboard'))
            else:
                return redirect(url_for('main.dashboard_aluno'))

        flash("E-mail ou senha incorretos")
    return render_template("login.html")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')

        if not nome or not email or not senha:
            flash("Todos os campos são obrigatórios")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(senha)

        if tipo == "professor":
            if Professor.query.filter_by(email=email).first():
                flash("E-mail de professor já cadastrado!")
                return redirect(url_for('auth.register'))
            user = Professor(nome=nome, email=email, senha=hashed_password)
        else:
            if Aluno.query.filter_by(email=email).first():
                flash("E-mail de aluno já cadastrado!")
                return redirect(url_for('auth.register'))
            user = Aluno(nome=nome, email=email, senha=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f"{tipo.capitalize()} cadastrado(a) com sucesso!")
        return redirect(url_for('auth.login'))

    return render_template("register.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
