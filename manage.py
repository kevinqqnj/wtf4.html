# -*- coding: utf-8 -*-
# 17197602@qq.com

#!/usr/bin/env python
import os
from app import create_app
from flask_script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)



if __name__ == '__main__':
    manager.run()

""" 
migrate: 
python manage.py db init
python manage.py db commit -m "xxx"
python manage.py db upgrade


"""
