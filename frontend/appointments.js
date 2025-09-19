const APPOINTMENTS_URL = 'http://127.0.0.1:8000/appointments/';
const PATIENTS_URL = 'http://127.0.0.1:8000/patients/';
const DOCTORS_URL = 'http://127.0.0.1:8000/doctors/';

const appointmentForm = document.getElementById('appointmentForm');
const patientSelect = document.getElementById('patient');
const doctorSelect = document.getElementById('doctor');
const appointmentsList = document.getElementById('appointmentsList');
const fetchAppointmentsBtn = document.getElementById('fetchAppointmentsBtn');

// ----------- Populate patient and doctor dropdowns -----------
async function populateDropdowns() {
    const patients = await fetch(PATIENTS_URL).then(res => res.json());
    patientSelect.innerHTML = "";
    patients.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = `${p.name} (${p.age}y)`;
        patientSelect.appendChild(option);
    });

    const doctors = await fetch(DOCTORS_URL).then(res => res.json());
    doctorSelect.innerHTML = "";
    doctors.forEach(d => {
        const option = document.createElement('option');
        option.value = d.id;
        option.textContent = `Dr. ${d.name} (${d.specialty})`;
        doctorSelect.appendChild(option);
    });
}

// ----------- CREATE Appointment -----------
async function createAppointment(patient_id, doctor_id, date, notes = "") {
    try {
        const res = await fetch(APPOINTMENTS_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ patient_id, doctor_id, date, notes })
        });
        const data = await res.json();
        console.log('Created:', data);
        return data;
    } catch (err) {
        console.error('Error creating appointment:', err);
    }
}

// ----------- LIST Appointments -----------
async function listAppointments() {
    try {
        const res = await fetch(APPOINTMENTS_URL);
        const data = await res.json();
        appointmentsList.innerHTML = "";
        if (!data || data.length === 0) {
            appointmentsList.textContent = "No appointments found.";
            return;
        }
        data.forEach(a => {
            const li = document.createElement('li');
            li.innerHTML = `[${a.id}] Patient ${a.patient_id} with Dr. ${a.doctor_id} on ${new Date(a.date).toLocaleString()} 
                <button onclick="deleteAppointment(${a.id})">Delete</button>`;
            appointmentsList.appendChild(li);
        });
    } catch (err) {
        appointmentsList.textContent = "Error fetching appointments.";
        console.error(err);
    }
}

// ----------- DELETE Appointment -----------
async function deleteAppointment(id) {
    try {
        const res = await fetch(`${APPOINTMENTS_URL}${id}/`, { method: 'DELETE' });
        if (res.ok) {
            console.log(`Deleted Appointment ${id}`);
            listAppointments();
        } else {
            console.error('Failed to delete appointment');
        }
    } catch (err) {
        console.error(`Error deleting appointment ${id}:`, err);
    }
}

// ----------- FORM SUBMISSION -----------
appointmentForm.addEventListener('submit', async e => {
    e.preventDefault();
    const patient_id = patientSelect.value;
    const doctor_id = doctorSelect.value;
    const date = document.getElementById('date').value;
    const notes = document.getElementById('notes').value;

    await createAppointment(patient_id, doctor_id, date, notes);
    appointmentForm.reset();
    listAppointments();
});

// ----------- REFRESH BUTTON -----------
fetchAppointmentsBtn.addEventListener('click', listAppointments);

// Initial load
populateDropdowns().then(listAppointments);
