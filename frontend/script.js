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

// ----------------- NLP Form -----------------
const nlpForm = document.getElementById('nlpForm');
const nlpResult = document.getElementById('nlpResult');

nlpForm.addEventListener('submit', async e => {
    e.preventDefault();
    const text = document.getElementById('medicalNote').value.trim();
    const task = document.getElementById('task').value;

    nlpResult.textContent = "Processing...";

    try {
        const res = await fetch('http://127.0.0.1:8000/nlp/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, task })
        });
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        nlpResult.innerHTML = `
            <div class="result-card">
                <strong>Task:</strong> ${data.task}<br>
                <strong>Input:</strong> ${data.input_text}<br>
                <strong>Result:</strong> ${data.result}
            </div>
        `;
    } catch (err) {
        nlpResult.textContent = "Error processing request.";
        console.error(err);
    }
});

// ----------------- NLP Results -----------------
const fetchResultsBtn = document.getElementById('fetchResultsBtn');
const resultsList = document.getElementById('resultsList');

fetchResultsBtn.addEventListener('click', async () => {
    resultsList.innerHTML = "Fetching...";
    try {
        const res = await fetch('http://127.0.0.1:8000/nlp/');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        resultsList.innerHTML = "";
        data.forEach((item, index) => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${index + 1}. [${item.task}]</strong> ${item.input_text} → ${item.result}`;
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
        const res = await fetch('http://127.0.0.1:8000/patient/list/');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        patientsList.innerHTML = "";
        data.forEach(p => {
            const li = document.createElement('li');
            li.textContent = `[${p.id}] ${p.name} - ${p.age}y`;
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
        const res = await fetch('http://127.0.0.1:8000/doctor/list/');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        doctorsList.innerHTML = "";
        data.forEach(d => {
            const li = document.createElement('li');
            li.textContent = `[${d.id}] Dr. ${d.name} - ${d.specialty || d.specialization}`;
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
        const res = await fetch('http://127.0.0.1:8000/appointment/list/');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        appointmentsList.innerHTML = "";
        data.forEach(a => {
            const li = document.createElement('li');
            li.textContent = `[${a.id}] Patient ${a.patient_id} with Dr. ${a.doctor_id} on ${a.date}`;
            appointmentsList.appendChild(li);
        });
    } catch (err) {
        appointmentsList.innerHTML = "Error fetching appointments.";
        console.error(err);
    }
});
