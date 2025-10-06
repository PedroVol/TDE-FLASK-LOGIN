from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

actuators = Blueprint("actuators", __name__, template_folder="../templates")

ACTUATORS = {}

@actuators.route("/actuators", methods=["GET"])
@login_required
def list_actuators():
    return render_template("actuators.html", actuators=ACTUATORS)

@actuators.route("/actuators/add", methods=["POST"])
@login_required
def add_actuator():
    aid  = request.form.get("id", "").strip()
    name = request.form.get("name", "").strip()
    typ  = request.form.get("type", "").strip()
    loc  = request.form.get("location", "").strip()
    st   = request.form.get("state", "off").strip()

    if not aid or aid in ACTUATORS:
        flash("ID inválido ou já existe.", "error")
        return redirect(url_for("actuators.list_actuators"))

    ACTUATORS[aid] = {
        "name": name or aid,
        "type": typ,
        "location": loc,
        "state": (st.lower() == "on"),
    }
    flash("Atuador adicionado.", "success")
    return redirect(url_for("actuators.list_actuators"))

@actuators.route("/actuators/<aid>/delete", methods=["POST"])
@login_required
def delete_actuator(aid):
    if aid in ACTUATORS:
        ACTUATORS.pop(aid)
        flash("Atuador removido.", "success")
    else:
        flash("Atuador não encontrado.", "error")
    return redirect(url_for("actuators.list_actuators"))

@actuators.route("/actuators/<aid>/update", methods=["POST"])
@login_required
def update_actuator(aid):
    if aid not in ACTUATORS:
        flash("Atuador não encontrado.", "error")
        return redirect(url_for("actuators.list_actuators"))

    name = request.form.get("name", "").strip()
    typ  = request.form.get("type", "").strip()
    loc  = request.form.get("location", "").strip()
    st   = request.form.get("state", "").strip()

    if name: ACTUATORS[aid]["name"] = name
    if typ:  ACTUATORS[aid]["type"] = typ
    if loc:  ACTUATORS[aid]["location"] = loc
    if st:
        ACTUATORS[aid]["state"] = (st.lower() == "on")

    flash("Atuador atualizado.", "success")
    return redirect(url_for("actuators.list_actuators"))

@actuators.route("/actuators/<aid>/toggle", methods=["POST"])
@login_required
def toggle_actuator(aid):
    if aid not in ACTUATORS:
        flash("Atuador não encontrado.", "error")
    else:
        ACTUATORS[aid]["state"] = not ACTUATORS[aid]["state"]
        flash(f"Atuador '{aid}' agora está {'ligado' if ACTUATORS[aid]['state'] else 'desligado'}.", "success")
    return redirect(url_for("actuators.list_actuators"))