# -*- coding: utf-8 -*-
# 17197602@qq.com

from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from .forms import CommentForm, CommentFormV


@main.route('/', methods=['GET', 'POST'])
def index():
    page = """
    <html>
    <br/>
    <a href="/demo"> Demo: wtf4.html to render Bootstrap 4 style form. Validate in Server</a>
     <br/>
     <br/>
    <a href="/demo-v"> Demo: wtf4v.html to render Vue-js validator form. Validate in both Client and Server</a>
     <br/>
     <br/>
    <a href="/demo-addClear"> Demo: wtf4addClear.html with vue-validator, and add Clear button in input</a>
   </html>
    """
    return page


@main.route('/demo', methods=['GET', 'POST'])
def demo():
    form = CommentForm()
    # print form.fa_addon
    if form.validate_on_submit():
        flash( u'Thanks %s！您的建议已经被收录' % (form.name.data) )
        # do some db actions here
        return redirect(url_for('.demo' ) )

    return render_template('demo.html', form=form)

@main.route('/demo-v', methods=['GET', 'POST'])
def demo_v():
    form = CommentFormV()
    return render_template('demo-v.html', form=form)

@main.route('/demo-addClear', methods=['GET', 'POST'])
def demo_addClear():
    form = CommentFormV()
    return render_template('demo-addClear.html', form=form)

@main.route('/vue3', methods=['GET', 'POST'])
def vue3():
    return render_template('vuevalidator3.html')
