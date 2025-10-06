from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user

login = Blueprint("login", __name__, template_folder="../templates")

@login.route('/login', methods=['GET'])
def login_form():
    return render_template("login.html")

@login.route('/validated_user', methods=['POST'])
def validated_user():
    user = request.form.get('user', '').strip()
    password = request.form.get('password', '').strip()

    USERS = current_app.config["USERS_STORE"]
    User = current_app.config["USER_CLASS"]

    if user in USERS and USERS[user]["password"] == password:
        login_user(User(user))
        flash(f"Bem-vindo, {user}!", "success")
        next_url = request.args.get("next") or url_for("home")
        return redirect(next_url)
    else:
        flash("Usuário ou senha inválidos.", "error")
        return redirect(url_for('login.login_form'))

@login.route('/logout', methods=['POST'])
@login_required
def logout():
    name = current_user.id
    logout_user()
    flash(f"Até logo, {name}.", "info")
    return redirect(url_for('home'))

@login.route("/users", methods=["GET"])
@login_required
def list_users():
    USERS = current_app.config["USERS_STORE"]
    return render_template("users.html", devices=USERS.keys())

@login.route('/register', methods=['GET'])
def register_user():
    return render_template("register_user.html")

@login.route('/register', methods=['POST'])
def create_user():
    USERS = current_app.config["USERS_STORE"]
    user = request.form.get('user', '').strip()
    password = request.form.get('password', '').strip()

    if not user or not password:
        flash("Informe usuário e senha.", "error")
        return redirect(url_for('login.register_user'))

    if user in USERS:
        flash("Usuário já existe.", "error")
        return redirect(url_for('login.register_user'))

    USERS[user] = {"password": password}
    flash("Usuário cadastrado.", "success")
    return redirect(url_for('login.list_users'))

@login.route('/remove', methods=['GET'])
@login_required
def remove_user_form():
    USERS = current_app.config["USERS_STORE"]
    return render_template("remove_user.html", devices=USERS.keys())

@login.route('/del_user', methods=['POST'])
@login_required
def del_user():
    USERS = current_app.config["USERS_STORE"]
    user = request.form.get('user', '').strip()
    if user in USERS:
        USERS.pop(user)
        flash('Usuário removido.', 'success')
    else:
        flash('Usuário não encontrado.', 'error')
    return redirect(url_for('login.list_users'))