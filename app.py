from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def generate_slots(start_time, end_time, break_start, break_end):
    slots = []
    current_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")
    break_start = datetime.strptime(break_start, "%H:%M")
    break_end = datetime.strptime(break_end, "%H:%M")

    while current_time < end_time:
        if not (break_start <= current_time < break_end):
            slots.append(current_time.strftime("%I:%M %p"))  # 12-hour format
        current_time += timedelta(minutes=15)
    return slots

@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/add-doctor", methods=["GET", "POST"])
def add_doctor():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        data = load_data()
        username = session['username']
        
        new_doctor = {
            "name": request.form["doctor-name"],
            "mobile": request.form["mobile"],
            "email": request.form["email"],
            "gender": request.form["gender"],
            "dob": request.form["dob"],
            "address": request.form["address"],
            "specialization": request.form["specialization"],
            "experience": request.form["experience"],
            "qualification": request.form["qualification"],
            "consultation_fee": request.form["consultation-fee"],
        }
        
        if username not in data:
            data[username] = {"doctors": [], "appointments": [], "patients": []}
        data[username]["doctors"].append(new_doctor)
        save_data(data)
        return redirect(url_for("home"))
    return render_template("add-doctor.html")

@app.route("/add-patient", methods=["GET", "POST"])
def add_patient():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        data = load_data()
        username = session['username']
        
        new_patient = {
            "name": request.form["patient-name"],
            "mobile": request.form["mobile"],
            "email": request.form["email"],
            "gender": request.form["gender"],
            "address": request.form["address"],
            "dob": request.form["dob"],
        }
        
        if username not in data:
            data[username] = {"doctors": [], "appointments": [], "patients": []}
        data[username]["patients"].append(new_patient)
        save_data(data)
        return redirect(url_for("home"))
    return render_template("add-patient.html")

@app.route("/schedule-appointment", methods=["GET", "POST"])
def schedule_appointment():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    username = session['username']
    
    if request.method == "POST":
        new_appointment = {
            "patient_name": request.form["patient-name"],
            "doctor": request.form["doctor"],
            "date": request.form["date"],
            "time": request.form["slot"],
            "status": "Scheduled",
        }
        
        if username not in data:
            data[username] = {"doctors": [], "appointments": [], "patients": []}
        data[username]["appointments"].append(new_appointment)
        save_data(data)
        return redirect(url_for("view_appointments"))
    
    doctors = data.get(username, {}).get("doctors", [])
    patients = data.get(username, {}).get("patients", [])
    return render_template("schedule-appointments.html", doctors=doctors, patients=patients)

@app.route("/get-doctor-slots")
def get_doctor_slots():
    if 'username' not in session:
        return jsonify({"success": False, "message": "Unauthorized"})

    doctor_name = request.args.get("doctor")
    date = request.args.get("date")

    data = load_data()
    username = session['username']
    doctors = data.get(username, {}).get("doctors", [])
    appointments = data.get(username, {}).get("appointments", [])

    # Find the selected doctor
    doctor = next((doc for doc in doctors if doc["name"] == doctor_name), None)
    if not doctor:
        return jsonify({"success": False, "message": "Doctor not found"})

    # Generate slots based on doctor's availability
    slots = generate_slots(doctor.get("start_time", "09:00"),
                          doctor.get("end_time", "17:00"),
                          doctor.get("break_start", "12:00"),
                          doctor.get("break_end", "13:00"))

    # Check booked slots for the selected date
    booked_slots = [appt["time"] for appt in appointments if appt["doctor"] == doctor_name and appt["date"] == date]

    # Prepare slot data
    slot_data = [{"time": slot, "booked": slot in booked_slots} for slot in slots]

    return jsonify({"success": True, "slots": slot_data})

@app.route("/view-appointments")
def view_appointments():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    username = session['username']
    appointments = data.get(username, {}).get("appointments", [])
    return render_template("view-appointments.html", appointments=appointments)

@app.route("/delete-appointment", methods=["POST"])
def delete_appointment():
    if 'username' not in session:
        return jsonify({"success": False})
    
    data = load_data()
    username = session['username']
    appointments = data.get(username, {}).get("appointments", [])
    
    patientName = request.json.get("patientName")
    date = request.json.get("date")
    time = request.json.get("time")
    
    # Filter out the appointment to delete
    data[username]["appointments"] = [appt for appt in appointments if not (
        appt["patient_name"] == patientName and
        appt["date"] == date and
        appt["time"] == time
    )]
    
    save_data(data)
    return jsonify({"success": True})
    

@app.route("/view-doctors")
def view_doctors():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    username = session['username']
    doctors = data.get(username, {}).get("doctors", [])
    return render_template("view-doctors.html", doctors=doctors)

@app.route("/set-availability", methods=["POST"])
def set_availability():
    if 'username' not in session:
        return jsonify({"success": False})
    
    data = load_data()
    username = session['username']
    doctors = data.get(username, {}).get("doctors", [])

    doctor_name = request.json.get("doctorName")
    start_time = request.json.get("startTime")
    break_start = request.json.get("breakStart")
    break_end = request.json.get("breakEnd")
    end_time = request.json.get("endTime")

    for doctor in doctors:
        if doctor["name"] == doctor_name:
            doctor["start_time"] = start_time
            doctor["break_start"] = break_start
            doctor["break_end"] = break_end
            doctor["end_time"] = end_time
            break

    save_data(data)
    return jsonify({"success": True})

@app.route("/view-patients")
def view_patients():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data = load_data()
    username = session['username']
    patients = data.get(username, {}).get("patients", [])
    return render_template("view-patients.html", patients=patients)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = load_data()
        username = request.json.get("username")
        password = request.json.get("password")

        user = next((user for user in data.get("users", []) if user["username"] == username and user["password"] == password), None)
        if user:
            session['username'] = username
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Invalid username or password."})
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = load_data()
        name = request.json.get("name")
        email = request.json.get("email")
        username = request.json.get("username")
        password = request.json.get("password")

        if any(user["username"] == username for user in data.get("users", [])):
            return jsonify({"success": False, "message": "Username already exists."})

        new_user = {
            "name": name,
            "email": email,
            "username": username,
            "password": password,
        }
        if "users" not in data:
            data["users"] = []
        data["users"].append(new_user)
        save_data(data)
        return jsonify({"success": True})
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)