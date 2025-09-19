// Base URL (assumes backend and frontend served from same domain)
const BASE_URL = "";

// ----------------- Tab Navigation -----------------
const tabs = document.querySelectorAll('.sidebar a[data-tab]');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', e => {
        e.preventDefault();
        const target = tab.dataset.tab;

        tabContents.forEach(tc => tc.style.display = 'none');
        document.getElementById(target).style.display = 'block';

        tabs.forEach(t => t.parentElement.classList.remove('active'));
        tab.parentElement.classList.add('active');
    });
});

// ----------------- NLP Form Submission -----------------
const nlpForm = document.getElementById('nlpForm');
const nlpResult = document.getElementById('nlpResult');

nlpForm.addEventListener('submit', async e => {
    e.preventDefault();
    const text = document.getElementById('medicalNote').value.trim();
    const task = document.getElementById('task').value;

    nlpResult.textContent = "Processing...";

    try {
        const res = await fetch(`${BASE_URL}/nlp/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, task })
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();

        nlpResult.innerHTML = `
            <div class="result-card">
                <strong>Task:</strong> ${data.task || task}<br>
                <strong>Input:</strong> ${data.input_text || text}<br>
                <strong>Result:</strong> ${data.result || "No result available"}
            </div>
        `;
    } catch (err) {
        nlpResult.textContent = "Error processing request.";
        console.error(err);
    }
});

// ----------------- Fetch Saved NLP Results -----------------
const fetchResultsBtn = document.getElementById('fetchResultsBtn');
const resultsList = document.getElementById('resultsList');

fetchResultsBtn.addEventListener('click', async () => {
    resultsList.innerHTML = "Fetching...";
    try {
        const res = await fetch(`${BASE_URL}/nlp/`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();

        resultsList.innerHTML = "";
        const results = data.results || data; // fallback if backend returns array directly

        if (!results || results.length === 0) {
            resultsList.textContent = "No NLP results found.";
            return;
        }

        results.forEach((item, index) => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${index + 1}. [${item.task || "N/A"}]</strong> ${item.input_text || ""} → ${item.result || ""}`;
            resultsList.appendChild(li);
        });
    } catch (err) {
        resultsList.innerHTML = "Error fetching results.";
        console.error(err);
    }
});

// ----------------- Patients CRUD -----------------
const fetchPatientsBtn = document.getElementById('fetchPatientsBtn');
const patientsList = document.getElementById('patientsList');

fetchPatientsBtn.addEventListener('click', async () => {
    patientsList.innerHTML = "Fetching...";
    try {
        const res = await fetch(`${BASE_URL}/patient/list/`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();

        patientsList.innerHTML = "";
        if (!data || data.length === 0) {
            patientsList.textContent = "No patients found.";
            return;
        }

        data.forEach(p => {
            const li = document.createElement('li');
            li.textContent = `[${p.id || "N/A"}] ${p.name || "Unnamed"} - ${p.age || "N/A"}y`;
            patientsList.appendChild(li);
        });
    } catch (err) {
        patientsList.innerHTML = "Error fetching patients.";
        console.error(err);
    }
});

// ----------------- Doctors CRUD -----------------
const fetchDoctorsBtn = document.getElementById('fetchDoctorsBtn');
const doctorsList = document.getElementById('doctorsList');

fetchDoctorsBtn.addEventListener('click', async () => {
    doctorsList.innerHTML = "Fetching...";
    try {
        const res = await fetch(`${BASE_URL}/doctor/list/`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();

        doctorsList.innerHTML = "";
        if (!data || data.length === 0) {
            doctorsList.textContent = "No doctors found.";
            return;
        }

        data.forEach(d => {
            const li = document.createElement('li');
            li.textContent = `[${d.id || "N/A"}] Dr. ${d.name || "Unnamed"} - ${d.specialty || d.specialization || "N/A"}`;
            doctorsList.appendChild(li);
        });
    } catch (err) {
        doctorsList.innerHTML = "Error fetching doctors.";
        console.error(err);
    }
});

// ----------------- Appointments CRUD -----------------
const fetchAppointmentsBtn = document.getElementById('fetchAppointmentsBtn');
const appointmentsList = document.getElementById('appointmentsList');

fetchAppointmentsBtn.addEventListener('click', async () => {
    appointmentsList.innerHTML = "Fetching...";
    try {
        const res = await fetch(`${BASE_URL}/appointment/list/`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();

        appointmentsList.innerHTML = "";
        if (!data || data.length === 0) {
            appointmentsList.textContent = "No appointments found.";
            return;
        }

        data.forEach(a => {
            const li = document.createElement('li');
            li.textContent = `[${a.id || "N/A"}] Patient ${a.patient_id || "N/A"} with Dr. ${a.doctor_id || "N/A"} on ${a.date || "N/A"}`;
            appointmentsList.appendChild(li);
        });
    } catch (err) {
        appointmentsList.innerHTML = "Error fetching appointments.";
        console.error(err);
    }
});
