from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
import os

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('public/home.html')

@home_bp.route('/sobre')
def about():
    return render_template('public/about.html')

@home_bp.route('/eventos')
def events():
    return render_template('public/events.html')

@home_bp.route('/galeria')
def gallery():
    return render_template('public/gallery.html')

@home_bp.route('/contato')
def contact():
    return render_template('public/contact.html')
