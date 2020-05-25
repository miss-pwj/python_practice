from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager

from libs.db import db
from main import app
from user.models import User
from weibo.models import Weibo
# 初始化app
# db.init_app(app)

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()