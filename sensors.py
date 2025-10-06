from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

sensors = Blueprint('sensors', __name__, template_folder="../templates")

SENSORS = {}

@sensors.route('/sensors', methods=['GET'])
@login_required
def list_sensors():
    return render_template('sensors.html', sensors=SENSORS)

@sensors.route('/sensors/add', methods=['POST'])
@login_required
def add_sensor():
    sid  = request.form.get('id', '').strip()
    name = request.form.get('name', '').strip()
    typ  = request.form.get('type', '').strip()
    loc  = request.form.get('location', '').strip()
    val  = request.form.get('value', '').strip()

    if not sid or sid in SENSORS:
        flash('ID inválido ou já existe.', 'error')
        return redirect(url_for('sensors.list_sensors'))

    try:
        value = float(val) if val else None
    except ValueError:
        value = None

    SENSORS[sid] = {'name': name or sid, 'type': typ, 'location': loc, 'value': value}
    flash('Sensor adicionado.', 'success')
    return redirect(url_for('sensors.list_sensors'))

@sensors.route('/sensors/<sid>/delete', methods=['POST'])
@login_required
def delete_sensor(sid):
    if sid in SENSORS:
        SENSORS.pop(sid)
        flash('Sensor removido.', 'success')
    else:
        flash('Sensor não encontrado.', 'error')
    return redirect(url_for('sensors.list_sensors'))

@sensors.route('/sensors/<sid>/update', methods=['POST'])
@login_required
def update_sensor(sid):
    if sid not in SENSORS:
        flash('Sensor não encontrado.', 'error')
        return redirect(url_for('sensors.list_sensors'))

    name = request.form.get('name', '').strip()
    typ  = request.form.get('type', '').strip()
    loc  = request.form.get('location', '').strip()
    val  = request.form.get('value', '').strip()

    try:
        value = float(val) if val else None
    except ValueError:
        value = None

    if name: SENSORS[sid]['name'] = name
    if typ:  SENSORS[sid]['type'] = typ
    if loc:  SENSORS[sid]['location'] = loc
    if val:  SENSORS[sid]['value'] = value

    flash('Sensor atualizado.', 'success')
    return redirect(url_for('sensors.list_sensors'))