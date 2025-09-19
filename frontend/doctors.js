const DOCTORS_URL = 'http://127.0.0.1:8000/doctors/';

const doctorForm = document.getElementById('doctorForm');
const doctorsList = document.getElementById('doctorsList');
const fetchDoctorsBtn = document.getElementById('fetchDoctorsBtn');

// ----------- CREATE Doctor -----------
async function createDoctor(name, specialty, contact) {
    if (!name || !specialty || !contact) {
        alert("All fields are required!");
        return;
    }
    try {
        const res = await fetch(DOCTORS_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, specialty, contact })
        });
        if (!res.ok) {
            const errorData = await res.json();
            console.error("Error creating doctor:", errorData);
            alert("Failed to create doctor. Check console for details.");
            return;
        }
        const data = await res.json();
        console.log('Created:', data);
        return data;
    } catch (err) {
        console.error('Error creating doctor:', err);
        alert("Error creating doctor. Check console.");
    }
}

// ----------- LIST All Doctors -----------
async function listDoctors() {
    try {
        const res = await fetch(DOCTORS_URL);
        const data = await res.json();
        doctorsList.innerHTML = "";
        if (!data || data.length === 0) {
            doctorsList.textContent = "No doctors found.";
            return;
        }
        data.forEach(d => {
            const li = document.createElement('li');
            li.innerHTML = `[${d.id}] Dr. ${d.name} - ${d.specialty} (${d.contact}) 
                <button onclick="deleteDoctor(${d.id})">Delete</button>
                <button onclick="editDoctor(${d.id})">Edit</button>`;
            doctorsList.appendChild(li);
        });
        return data;
    } catch (err) {
        doctorsList.textContent = "Error fetching doctors.";
        console.error(err);
    }
}

// ----------- DELETE Doctor -----------
async function deleteDoctor(id) {
    try {
        const res = await fetch(`${DOCTORS_URL}${id}/`, { method: 'DELETE' });
        if (res.ok) {
            console.log(`Deleted Doctor ${id}`);
            listDoctors();
        } else {
            console.error('Failed to delete doctor');
            alert("Failed to delete doctor.");
        }
    } catch (err) {
        console.error(`Error deleting doctor ${id}:`, err);
    }
}

// ----------- UPDATE Doctor -----------
async function updateDoctor(id, updates) {
    if (!updates.name || !updates.specialty || !updates.contact) {
        alert("All fields are required for update!");
        return;
    }
    try {
        const res = await fetch(`${DOCTORS_URL}${id}/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        if (!res.ok) {
            const errorData = await res.json();
            console.error(`Error updating doctor ${id}:`, errorData);
            alert("Failed to update doctor. Check console for details.");
            return;
        }
        const data = await res.json();
        console.log(`Updated Doctor ${id}:`, data);
        listDoctors();
        return data;
    } catch (err) {
        console.error(`Error updating doctor ${id}:`, err);
        alert("Error updating doctor. Check console.");
    }
}

// ----------- FORM SUBMISSION -----------
doctorForm.addEventListener('submit', async e => {
    e.preventDefault();
    const name = document.getElementById('doctorName').value.trim();
    const specialty = document.getElementById('doctorSpecialty').value.trim();
    const contact = document.getElementById('doctorContact').value.trim();

    await createDoctor(name, specialty, contact);
    doctorForm.reset();
    listDoctors();
});

// ----------- REFRESH BUTTON -----------
fetchDoctorsBtn.addEventListener('click', listDoctors);

// Initial load
listDoctors();
