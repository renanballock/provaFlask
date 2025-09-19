from . import db
from flask_login import UserMixin

# Associação entre Aluno e Turma
aluno_turma = db.Table('aluno_turma',
    db.Column('aluno_id', db.Integer, db.ForeignKey('aluno.id')),
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'))
)

class Professor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    turmas = db.relationship('Turma', backref='professor', lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return f"prof_{self.id}"

    def is_professor(self):
        return True

class Aluno(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    turmas = db.relationship('Turma', secondary=aluno_turma, backref='alunos', lazy='dynamic')

    def get_id(self):
        return f"aluno_{self.id}"

    def is_professor(self):
        return False

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    atividades = db.relationship('Atividade', backref='turma', lazy=True, cascade="all, delete-orphan")

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(300), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
