from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms_module import ClientForm, ContactForm  # Importing forms from forms_module
from config import Config  # Import configuration settings

app = Flask(__name__)
app.config.from_object(Config)  # Load settings from config.py
db = SQLAlchemy(app)

# Models
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    client_code = db.Column(db.String(10), unique=True, nullable=False)
    contacts = db.relationship('Contact', secondary='client_contact', backref='clients')

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

client_contact = db.Table('client_contact',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), primary_key=True)
)

# Routes
@app.route('/')
def index():
    return redirect(url_for('client_list'))

@app.route('/clients')
def client_list():
    clients = Client.query.order_by(Client.name).all()
    return render_template('client_list.html', clients=clients)

@app.route('/client/new', methods=['GET', 'POST'])
def new_client():
    form = ClientForm()
    if form.validate_on_submit():
        client_code = generate_client_code(form.name.data)
        client = Client(name=form.name.data, client_code=client_code)
        db.session.add(client)
        db.session.commit()
        flash('Client created successfully!', 'success')
        return redirect(url_for('client_list'))
    return render_template('client_form.html', form=form)

@app.route('/contacts')
def contact_list():
    contacts = Contact.query.order_by(Contact.surname).all()
    return render_template('contact_list.html', contacts=contacts)

@app.route('/contact/new', methods=['GET', 'POST'])
def new_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, surname=form.surname.data, email=form.email.data)
        db.session.add(contact)
        db.session.commit()
        flash('Contact created successfully!', 'success')
        return redirect(url_for('contact_list'))
    return render_template('contact_form.html', form=form)

# Function to generate client code based on rules
def generate_client_code(name):
    code = ''.join([x[0].upper() for x in name.split()][:3])
    if len(code) < 3:
        code += 'A' * (3 - len(code))
    count = 1
    while True:
        final_code = f"{code}{str(count).zfill(3)}"
        if not Client.query.filter_by(client_code=final_code).first():
            return final_code
        count += 1

# Function to create the database tables
def create_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':  # Corrected line
    create_database()  # Ensure the database tables are created before running the app
    app.run(debug=True, port=5001)
