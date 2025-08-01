from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20),primary_key=True, nullable=False)
    expense= db.Column(db.Float, nullable=False, default=0.0)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/addcontact', methods=['POST'])
def add_contact():
    data = request.get_json()
    name = data.get("name")
    phone = data.get("phone")
    expense = data.get("expense", 0.0)
    db.session.add(Contact(name=name, phone=phone, expense=expense) )
    print("POST CALLED")
    db.session.commit()
    return jsonify({"message": "Contact added successfully!"})

@app.route('/modify', methods=['POST'])
def modify_contact():
    data = request.get_json()
    print("MODIFY DATA::", data)
    phone = data.get("phone")
    contact = Contact.query.filter_by(phone=phone).first()
    print("MODIFY CONTACT:", contact)
    if contact:
        contact.expense+=data.get("nexpense")
        db.session.commit()

        return jsonify({"message": "Contact modified successfully!"})
    return jsonify({"error": "Contact not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
