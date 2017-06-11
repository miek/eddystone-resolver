from flask import Flask, request, _app_ctx_stack
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

@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

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

@app.route('/beacon/')
def list_beacons():
    rv = query_db('select name from beacon')
    return '<ul>' + ''.join(['<li>' + row['name'] + '</li>' for row in rv]) + '</ul>'

@app.route('/beacon/<name>', methods=['POST'])
def register_beacon(name):
    db = get_db()
    # TODO: get & verify parameters from request
    # TODO: generate IK from ECDH keys
    # TODO: pass IK & params to _crypto and check first EID is correct
    db.execute('insert into beacon (name, identity_key, clock_offset, k) values (?, ?, ?, ?)',
               [name, 'abcd', 1234, 11])
    db.commit()
    return 'Registered beacon ' + name

@app.route('/eid/<eid>')
def resolve_eid(eid):
    rv = query_db(
            'select name from beacon join eid on id = beacon_id where eid = ?',
            [eid], True
    )
    return 'Hey ' + eid

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
