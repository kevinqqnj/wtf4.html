# wtf4.html
wtf.html (Flask-wtf & Flask-bootstrap) adapted for Bootstrap4 styles. 


##### [Live Demo](http://tianya.heroku.com/wtf)


## Purpose
To quickly render out form with latest Bootstrap4 styes, by customized wtf.html (part of Flask-Bootstrap)
##### snapshot
![](http://img.blog.csdn.net/20161111105913670?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

![](http://img.blog.csdn.net/20161116090216256?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)



## Background
We know Flask-bootstrap provides a macro to quickly render out a form by one line:
> /app/forms.py
```
class CommentForm(Form):
  name = StringField(...)
  ...
```

> /tempelate/demo.html
```
{% import "bootstrap/wtf.html" as wtf %}
    {{ wtf.quick_form(form, button_map={'submit':'primary'} }}
```

But it's a bit simple, although you can add customized CSS in forms.by like below, but it's not adapted for Bootstrap4 (Alpha5).
> 
```
class CommentForm(Form):
    name = StringField('', validators=[Length(0, 64)], render_kw={"placeholder": "your name",
                                                                  "style": "background: url(/static/login-locked-icon.png) no-repeat 15px center;text-indent: 28px"})
    email = StringField('', description='* We\'ll never share your email with anyone else.', validators= \
        [DataRequired(), Length(4, 64), Email(message=u"邮件格式有误")], render_kw={"placeholder": "yourname@example.com"})
    comment = TextAreaField('', description=u"请提出宝贵意见和建议", validators=[DataRequired()],
                            render_kw = {"placeholder": "Input your comments here"})
    submit = SubmitField(u'提交')
```

The styles and format of form are defined in wtf.html, it's in your Flask-bootstrap install directly.
> e.g. C:\git\tianya\venv\Lib\site-packages\flask_bootstrap\templates\bootstrap\wtf.html

## Install and how to use
1. simplely clone this git to local, it's a well-formed Flask framework, and included local Bootstrap4 CSS. Or just copy '/app/templates/_wtf4.html' to you Flask template directory
> e.g. C:\git\tianya\app\templates\

2. use the macro in your html like this
> /tempelate/demo.html
```
{% import "_wtf4.html" as _wtf4 %}
{% block page_content %}
    {{ _wtf4.quick_form(form, form_type="basic", button_map={'submit':'primary', }, id='comment_form') }}
```

3. design your form

> /app/forms.py
```
class CommentForm(Form):
    name = StringField('', validators=[Length(0, 64)], render_kw={"placeholder": "your name",})
    email = StringField('', description='* We\'ll never share your email with anyone else.', validators= \
        [DataRequired(), Length(4, 64), Email(message=u"邮件格式有误")], render_kw={"placeholder": "yourname@example.com"})
    comment = TextAreaField('', description=u"* 请提出宝贵意见和建议", validators=[DataRequired()],
                            render_kw = {"placeholder": "input your comments here"})
    submit = SubmitField(u'提交')
    # FontAwesome css, show icon as prefix of fields
    fa_addon = {
        'email': 'fa-envelope-o',
        'name': 'fa-user-o',
    }
```
 
4. fa_addon is used as icons ahead of every input fields, needs [FontAwesome CSS](http://fontawesome.io/examples/), you can add the CDN in your html like this:

```
<link rel="stylesheet" type="text/css" href="//cdn.bootcss.com/font-awesome/4.7.0/css/font-awesome.css">
```

I've adapted for the following CSS in \_wtf4.html:
```
class="input-group-addon"
class="form-text text-muted"
class="form-text text-warning">
```
You can add/change any more CSS as you want, in _wtf4.html


## use Vue-validator to do validation on client side (_wtf4v.html)

According to MVVM，forms.py belongs to Model, so just define the funciton of form fields, no need to worry about how it's displayed in user's web browser.

> app/main/forms.py
```
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
```

Then define your validation rule and CSS style in your html. Also include any java-scripts to do cv (Customized Validation), e.g. comparing password and password-repeat. "\_wtf4v.html" does the whole work of constructing the Form's HTML code for you.

> app/template/demo-v.html
```
{% import "_wtf4v.html" as _wtf4v %}
       {{ _wtf4v.quick_form(form, form_type="basic", button_map={'submit':'primary', }, id='form',
            fa_map={
            	'email': 'fa-envelope-o',
            	'name': 'fa-user-o',
           	  'password': 'fa-key', 	
           	  'passwordrepeat': 'fa-key', 	
            },
            validator_map={
                'comment': {
                    'validators': '{minlength:3, maxlength:10}',
                    'feedbacks': {'minlength':'your comments need more than 3 chars', 'maxlength':'your comments should not exceed 10 chars'}
                    },
                 'name':  {
                    'validators': '{required: true}',
                    'feedbacks': {'required':'name is required'},
                    },
                'email':  {
                    'validators': '{email:true}',
                    'feedbacks': {'email':'email format is wrong'},
                    },
                'password':  {
                    'validators': '{passw:true, minlength:4, maxlength:8}',
                    'feedbacks': { 'passw':'passsword need in (A-Z, a-z, 0-9, _)','minlength':'password too short', 'maxlength':'password too long' },
                   '_cv': { 'cv_password': 'password not match' },  
                    '@valid': 'onPasswordValid'
                    },
                'passwordrepeat':  {
                    'validators': '{required:true}',
                    'feedbacks': { 'required':'repeat passsword' },
                   '_cv': { 'cv_password': 'password not match' },  
                    '@valid': 'onPasswordValid'
                    },
                  'submit': {
                   '@click': 'submitMethod',
                    'v-bind:class': "[{'disabled': ($validation.invalid && $validation.touched) || !cv_password }]"
                    }
                }
            ) }}

```
