# -*- coding: utf-8 -*-
# 17197602@qq.com

from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from .forms import CommentForm


@main.route('/')
@main.route('/about', methods=['GET', 'POST'])
def about():
    form = CommentForm()
    print form.fa_addon
    if form.validate_on_submit():
        flash( u'Thanks %s！您的建议已经被收录' % (form.name.data) )
        # do some db actions here
        return redirect(url_for('.about' ) )

    return render_template('about.html', form=form)
