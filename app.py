from flask import Flask, render_template, request, redirect, url_for,session
from db_config import db
from models import Patient, Doctor

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

# Import models after db is defined
from models import Patient, Doctor

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Replace with real auth check if needed
        if username == 'admin' and password == 'admin':
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# 🏠 Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# 🔽 READ Patients
@app.route('/patients')
def patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients)

# 🔼 CREATE Patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        doctor_id = request.form['doctor_id']
        new_patient = Patient(name=name, age=age, gender=gender, doctor_id=doctor_id)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('patients'))
    doctors = Doctor.query.all()
    return render_template('add_patient.html', doctors=doctors)

# 📝 UPDATE Patient
@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.gender = request.form['gender']
        patient.doctor_id = request.form['doctor_id']
        db.session.commit()
        return redirect(url_for('patients'))
    doctors = Doctor.query.all()
    return render_template('edit_patient.html', patient=patient, doctors=doctors)

# ❌ DELETE Patient
@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('patients'))

# 🔽 READ Doctors
@app.route('/doctors')
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors)

# 🔼 CREATE Doctor
@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        new_doctor = Doctor(name=name, specialization=specialization)
        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('doctors'))
    return render_template('add_doctor.html')

# 📝 UPDATE Doctor
@app.route('/edit_doctor/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    if request.method == 'POST':
        doctor.name = request.form['name']
        doctor.specialization = request.form['specialization']
        db.session.commit()
        return redirect(url_for('doctors'))
    return render_template('edit_doctor.html', doctor=doctor)

# ❌ DELETE Doctor
@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('doctors'))

# 🧾 VIEW all appointments
@app.route('/appointments')
def appointments():
    from models import Appointment, Patient, Doctor
    all_appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=all_appointments)

# ➕ ADD appointment
@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    from models import Appointment, Patient, Doctor
    if request.method == 'POST':
        appointment = Appointment(
            patient_id=request.form['patient_id'],
            doctor_id=request.form['doctor_id'],
            date=request.form['date'],
            sickness=request.form['sickness'],
            medicines=request.form['medicines'],
            notes=request.form['notes']
        )
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('appointments'))
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('add_appointment.html', patients=patients, doctors=doctors)

# 📝 EDIT appointment
@app.route('/edit_appointment/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    from models import Appointment, Patient, Doctor
    appointment = Appointment.query.get_or_404(id)
    if request.method == 'POST':
        appointment.patient_id = request.form['patient_id']
        appointment.doctor_id = request.form['doctor_id']
        appointment.date = request.form['date']
        appointment.sickness = request.form['sickness']
        appointment.medicines = request.form['medicines']
        appointment.notes = request.form['notes']
        db.session.commit()
        return redirect(url_for('appointments'))
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('edit_appointment.html', appointment=appointment, patients=patients, doctors=doctors)

# ❌ DELETE appointment
@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    from models import Appointment
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for('appointments'))



if __name__ == '__main__':
    app.run(debug=True)
