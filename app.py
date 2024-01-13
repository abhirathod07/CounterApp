from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'counterapp')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
db = SQLAlchemy(app)


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    counter = db.Column(db.Integer,  nullable=False)


@app.route('/', methods=['GET', 'POST'])
def main():
    new_counter = 0
    counter_record = db.session.query(Counter).order_by(Counter.id.desc()).first()
    counter = request.form.get('counter')
    if request.method == 'POST':
        if counter_record:
            counter_record.counter = counter
        else:
            new_counter = Counter(counter=counter)
            db.session.add(new_counter)
        db.session.commit()
        new_counter = int(counter)
    elif request.method == 'GET':
        new_counter = counter_record.counter if counter_record else 0
    return render_template('index.html', counter=new_counter)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)