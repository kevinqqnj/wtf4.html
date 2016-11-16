# -*- coding: utf-8 -*-
# 17197602@qq.com

from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, PasswordField
from wtforms.validators import Length, Email, Regexp, DataRequired


class CommentForm(Form):
    # name = StringField('', validators=[Length(0, 64)], render_kw={"placeholder": "your name",
    #                                                               "style": "background: url(/static/login-locked-icon.png) no-repeat 15px center;text-indent: 28px"})
    name = StringField('', validators=[Length(0, 64)], render_kw={"placeholder": "your name",})
    email = StringField('', description='* We\'ll never share your email with anyone else.', validators= \
        [DataRequired(), Length(4, 64), Email(message=u"邮件格式有误")], render_kw={"placeholder": "you@example.com"})
    comment = TextAreaField('', description=u"* 请提出宝贵意见和建议", validators=[DataRequired()],
                            render_kw = {"placeholder": "input your comments here"})
    submit = SubmitField(u'提交')
    # FontAwesome css, show icon as prefix of fields
    fa_addon = {
        'email': 'fa-envelope-o',
        'name': 'fa-user-o',
    }

class CommentFormV(Form):
    name = StringField('', validators=[Length(0, 64)], render_kw={"placeholder": "your name"})
    email = StringField('', description='* We\'ll never share your email with anyone else', validators= \
        [DataRequired(), Length(4, 64), Email(message=u"邮件格式有误")], render_kw={"placeholder": "you@example.com"})
    password = PasswordField('', validators=[Length(4, 8)], description='* password is 4~8 long, [A-Za-z0-9_]',
    					render_kw={"placeholder": "password"})
    passwordrepeat = PasswordField('', validators=[Length(4, 8)], render_kw={"placeholder": "repeat password"})
    comment = TextAreaField('', description=u"* Comments. 请提出宝贵意见和建议", validators=[DataRequired()],
                            render_kw = {"placeholder": "input your comments here, 3~10 chars"})
    submit = SubmitField(u'Submit Comments', render_kw = {})


