const PATIENTS_URL = 'http://127.0.0.1:8000/patients/';

const patientForm = document.getElementById('patientForm');
const patientsList = document.getElementById('patientsList');

// ----------- CREATE Patient -----------
async function createPatient(name, age, gender, allergies = "") {
    try {
        const res = await fetch(PATIENTS_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, age, gender, allergies })
        });
        const data = await res.json();
        console.log('Created:', data);
        return data;
    } catch (err) {
        console.error('Error creating patient:', err);
    }
}

// ----------- LIST All Patients -----------
async function listPatients() {
    try {
        const res = await fetch(PATIENTS_URL);
        const data = await res.json();
        patientsList.innerHTML = "";
        if (!data || data.length === 0) {
            patientsList.textContent = "No patients found.";
            return;
        }
        data.forEach(p => {
            const li = document.createElement('li');
            li.innerHTML = `[${p.id}] ${p.name} - ${p.age}y (${p.gender}) 
                <button onclick="deletePatient(${p.id})">Delete</button>
                <button onclick="editPatient(${p.id})">Edit</button>`;
            patientsList.appendChild(li);
        });
        return data;
    } catch (err) {
        patientsList.textContent = "Error fetching patients.";
        console.error(err);
    }
}

// ----------- DELETE Patient -----------
async function deletePatient(id) {
    try {
        const res = await fetch(`${PATIENTS_URL}${id}/`, { method: 'DELETE' });
        if (res.ok) {
            console.log(`Deleted Patient ${id}`);
            listPatients(); // Refresh list
        } else {
            console.error('Failed to delete patient');
        }
    } catch (err) {
        console.error(`Error deleting patient ${id}:`, err);
    }
}

// ----------- UPDATE Patient -----------
async function updatePatient(id, updates) {
    try {
        const res = await fetch(`${PATIENTS_URL}${id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        const data = await res.json();
        console.log(`Updated Patient ${id}:`, data);
        listPatients(); // Refresh list
        return data;
    } catch (err) {
        console.error(`Error updating patient ${id}:`, err);
    }
}

// ----------- FORM SUBMISSION -----------
patientForm.addEventListener('submit', async e => {
    e.preventDefault();
    const name = document.getElementById('patientName').value.trim();
    const age = parseInt(document.getElementById('patientAge').value);
    const gender = document.getElementById('patientGender').value;
    const allergies = document.getElementById('patientAllergies').value.trim();

    await createPatient(name, age, gender, allergies);
    patientForm.reset();
    listPatients();
});

// Initial load
listPatients();
