from flask import render_template, jsonify
from app import app
import random
from flask import send_from_directory
from sqlalchemy import desc
import os
from ..models import (db, User, InstaPost, UserInfluencerMap, 
                      Products, InstaInfluencer)
from flask.ext.login import login_user, logout_user, login_required
from flask_login import current_user, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from flask.ext.bootstrap import Bootstrap
from tempfile import NamedTemporaryFile
import sys
import os


sys.path.insert(0, os.path.abspath('../model/'))
from inference import get_nn


bootstrap = Bootstrap(app)
root_dir = os.path.dirname(os.getcwd()) + '/webapp/app/'


class UploadFileForm(FlaskForm):
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')


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


@app.route('/tmp/<path:filename>')
def serve_tmp(filename):
    ''' Return images given a file name '''
    return send_from_directory('/tmp/', filename)


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
    recent_posts = InstaPost.query.order_by(desc(InstaPost.post_date)
                                    ).limit(6).all()
    post_links = [i.post_link for i in recent_posts]
    return render_template('index_2.html',
                           authenticated=current_user.is_authenticated,
                           post_links=post_links)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    ''' Return upload template '''
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file_selector.data
        file.seek(0)
        ftemp = NamedTemporaryFile(delete=False)
        file.save(ftemp)
        links = get_nn(ftemp.name)
        products = Products.query.filter(Products.id.in_(tuple(links))).all()
        products = products[1:]
        return render_template('discovery.html', products=products,
                                tmpfile=ftemp.name)

    return render_template('upload2.html', form=form)


@app.route('/product')
@login_required
def product():
    ''' Return template for maps '''
    user_email = current_user.email
    influencers = UserInfluencerMap.query.filter_by(user_email=user_email).all()
    influencers = [i.influencer_id for i in influencers]
    influencers = InstaInfluencer.query\
                    .filter(InstaInfluencer.id.in_(tuple(influencers))).all()
    influencers = [i.user_name for i in influencers]
    insta_urls = InstaPost.query.filter(InstaPost.user_name.in_(tuple(influencers))
                                       ).order_by(desc(InstaPost.post_date))\
                                        .limit(5).all()
    insta_urls = [i.post_link + '/' for i in insta_urls]
    return render_template('product.html', insta_url=insta_urls)


@app.route('/contact')
def contact():
    ''' Return template for contacts '''
    return render_template('contact.html', title='Contact')

@app.route('/about')
def about():
    ''' Return template for contacts '''
    return render_template('aboutus.html', title='Contact')