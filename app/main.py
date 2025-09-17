from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Turma, Atividade

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    turmas = Turma.query.filter_by(professor_id=current_user.id).all()
    return render_template('dashboard.html', turmas=turmas)

@main.route('/cadastrar_turma', methods=['GET', 'POST'])
@login_required
def cadastrar_turma():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if nome:
            nova_turma = Turma(nome=nome, professor_id=current_user.id)
            db.session.add(nova_turma)
            db.session.commit()
            flash("Turma cadastrada com sucesso!")
            return redirect(url_for('main.dashboard'))
    return render_template('cadastrar_turma.html')

@main.route('/atividades/<int:turma_id>')
@login_required
def atividades(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    if turma.professor_id != current_user.id:
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard'))
    atividades = Atividade.query.filter_by(turma_id=turma.id).all()
    return render_template('atividades.html', turma=turma, atividades=atividades)

@main.route('/cadastrar_atividade/<int:turma_id>', methods=['GET', 'POST'])
@login_required
def cadastrar_atividade(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    if turma.professor_id != current_user.id:
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        if descricao:
            atividade = Atividade(descricao=descricao, turma_id=turma.id)
            db.session.add(atividade)
            db.session.commit()
            flash("Atividade cadastrada com sucesso!")
            return redirect(url_for('main.atividades', turma_id=turma.id))
    return render_template('cadastrar_atividade.html', turma=turma)

@main.route('/visualizar_turma/<int:turma_id>')
@login_required
def visualizar_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    if turma.professor_id != current_user.id:
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard'))
    atividades = Atividade.query.filter_by(turma_id=turma.id).all()
    return render_template('visualizar_turma.html', turma=turma, atividades=atividades)

@main.route('/excluir_turma/<int:turma_id>', methods=['POST'])
@login_required
def excluir_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    if turma.professor_id != current_user.id:
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard'))
    db.session.delete(turma)
    db.session.commit()
    flash("Turma excluída com sucesso!")
    return redirect(url_for('main.dashboard'))
