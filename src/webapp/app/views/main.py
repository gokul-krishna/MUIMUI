from flask import render_template, jsonify
from app import app
import random
from flask import send_from_directory
import os

root_dir = os.path.dirname(os.getcwd()) + '/webapp/app/'


@app.route('/js/<path:filename>')
def serve_js(filename):
    ''' Serve JS script given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'js'), filename)


@app.route('/images/<path:filename>')
def serve_images(filename):
    ''' Return images given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'images_2'), filename)


@app.route('/images_2/<path:filename>')
def serve_images_2(filename):
    ''' Return images given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'images_2'), filename)


@app.route('/plugins/<path:filename>')
def serve_plugins(filename):
    ''' Return plugins given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'plugins'), filename)


@app.route('/styles/<path:filename>')
def serve_styles(filename):
    ''' Return styles given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'styles'), filename)


@app.route('/css/<path:filename>')
def serve_css(filename):
    ''' Return css given a file name '''
    return send_from_directory(
            os.path.join(root_dir, 'static', 'css'), filename)


@app.route('/')
@app.route('/index')
def index():
    ''' Return index template '''
    return render_template('index_2.html', title='Home')


@app.route('/upload')
def upload():
    ''' Return upload template '''
    return render_template('upload2.html')


@app.route('/map')
def map():
    ''' Return template for maps '''
    return render_template('nav_bar.html', title='Map')

@app.route('/test')
def test():
    ''' Return template for maps '''
    return render_template('user/signin.html', title='Test')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    ''' Return maps co-ordinates '''
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    ''' Return template for contacts '''
    return render_template('contact.html', title='Contact')

@app.route('/about')
def about():
    ''' Return template for contacts '''
    return render_template('aboutus.html', title='Contact')