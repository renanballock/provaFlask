from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Turma, Atividade

main = Blueprint('main', __name__)

# --- DASHBOARD PROFESSOR ---
@main.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_professor():
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard_aluno'))

    turmas = current_user.turmas
    return render_template('dashboard.html', turmas=turmas)

# --- DASHBOARD ALUNO ---
@main.route('/dashboard_aluno')
@login_required
def dashboard_aluno():
    if current_user.is_professor():
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard'))

    turmas = current_user.turmas
    todas_turmas = Turma.query.all()
    return render_template('dashboard_aluno.html', turmas=turmas, todas_turmas=todas_turmas)

# --- PROFESSOR ---
@main.route('/cadastrar_turma', methods=['GET', 'POST'])
@login_required
def cadastrar_turma():
    if not current_user.is_professor():
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard_aluno'))

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

    # Professores: só suas turmas
    if current_user.is_professor() and turma.professor_id != current_user.id:
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard'))

    # Alunos: só turmas matriculadas
    if not current_user.is_professor() and current_user not in turma.alunos:
        flash("Você não está matriculado nesta turma!")
        return redirect(url_for('main.dashboard_aluno'))

    atividades = Atividade.query.filter_by(turma_id=turma.id).all()
    return render_template('atividades.html', turma=turma, atividades=atividades)

@main.route('/cadastrar_atividade/<int:turma_id>', methods=['GET', 'POST'])
@login_required
def cadastrar_atividade(turma_id):
    turma = Turma.query.get_or_404(turma_id)

    if not current_user.is_professor() or turma.professor_id != current_user.id:
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

    if current_user.is_professor() and turma.professor_id != current_user.id:
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard'))

    if not current_user.is_professor() and current_user not in turma.alunos:
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard_aluno'))

    atividades = Atividade.query.filter_by(turma_id=turma.id).all()
    return render_template('visualizar_turma.html', turma=turma, atividades=atividades)

@main.route('/excluir_turma/<int:turma_id>', methods=['POST'])
@login_required
def excluir_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)

    if not current_user.is_professor() or turma.professor_id != current_user.id:
        flash("Acesso negado!")
        return redirect(url_for('main.dashboard'))

    db.session.delete(turma)
    db.session.commit()
    flash("Turma excluída com sucesso!")
    return redirect(url_for('main.dashboard'))

# --- ALUNO ---
@main.route('/entrar_turma/<int:turma_id>', methods=['POST'])
@login_required
def entrar_turma(turma_id):
    if current_user.is_professor():
        flash("Professores não podem se matricular em turmas!")
        return redirect(url_for('main.dashboard'))

    turma = Turma.query.get_or_404(turma_id)
    if current_user in turma.alunos:
        flash("Você já está matriculado nessa turma!")
    else:
        turma.alunos.append(current_user)
        db.session.commit()
        flash(f"Você entrou na turma {turma.nome} com sucesso!")

    return redirect(url_for('main.dashboard_aluno'))
