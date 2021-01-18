from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        form_name = request.form['name']
        form_number = request.form['number']
        new_addition = Contact(name=form_name, number=form_number)
        db.session.add(new_addition)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        contacts = Contact.query.order_by(Contact.date_created).all()
        return render_template('index.html', title='Home', contacts=contacts)

    
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    contacts = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contacts.name = request.form['name']
        contacts.number = request.form['number']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "There was an error updating your contact."
    return render_template('update.html', title='Update Contact', contacts=contacts)

@app.route('/delete/<int:id>')
def delete(id):
    contact_delete = Contact.query.get_or_404(id)
    try:
        db.session.delete(contact_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was a problem deleting that task."
    return render_template('index.html')

if __name__ =='__main__':
    app.run(debug=True)