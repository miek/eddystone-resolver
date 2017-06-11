from flask import Flask, _app_ctx_stack
from sqlite3 import dbapi2 as sqlite3

DATABASE = '/tmp/beacons.db'

app = Flask(__name__)
app.config.from_object(__name__)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

@app.route('/beacon/<eid>')
def get_beacon(eid):
    return 'Hey ' + eid

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
