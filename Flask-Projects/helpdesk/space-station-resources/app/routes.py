from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .models import Resource
from . import db

bp = Blueprint('resources', __name__)

@bp.route('/resources', methods=['GET'])
def index():
    resources = Resource.query.all()
    return render_template('index.html', resources=resources)

@bp.route('/resources/add', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        new_resource = Resource(name=name, quantity=quantity)
        db.session.add(new_resource)
        db.session.commit()
        return redirect(url_for('resources.index'))
    return render_template('add_resource.html')

@bp.route('/resources/edit/<int:id>', methods=['GET', 'POST'])
def edit_resource(id):
    resource = Resource.query.get_or_404(id)
    if request.method == 'POST':
        resource.name = request.form['name']
        resource.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for('resources.index'))
    return render_template('edit_resource.html', resource=resource)

@bp.route('/resources/delete/<int:id>', methods=['POST'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for('resources.index'))