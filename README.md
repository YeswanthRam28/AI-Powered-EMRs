🏥 AI-Powered Electronic Medical Records (EMR)

A full-stack AI-powered EMR system that helps manage patients, doctors, and appointments while also providing NLP-based medical note analysis (summarization, keywords, diagnosis support, and more).


---

✨ Features

👩‍⚕️ Patients Management – Add, update, search, and delete patients.

🧑‍⚕️ Doctors Management – Manage doctor records with specialties and contact info.

📅 Appointments Management – Book, view, and manage patient–doctor appointments.

🧠 NLP Tool – Process medical notes with AI:

Summarization

Keyword Extraction

Insights & Risk Factors

Diagnosis Support

Treatment Plan Suggestions

Translation (Tamil)

Sentiment Analysis

Named Entity Recognition (NER)


📊 Results Dashboard – View previously processed NLP results in a dedicated page.

🎨 Modern UI – Sidebar dashboard layout with attractive, psychologically engaging colors.



---

🛠️ Tech Stack

Backend: FastAPI (Python)

Database: SQLite (default, can be extended to PostgreSQL/MySQL)

Frontend: HTML, CSS, JavaScript (vanilla, no frameworks for simplicity)

AI/NLP: Python-based processing (extensible with LLM APIs or custom ML models)



---

📂 Project Structure

AI-Powered-EMRs/
│── backend/
│   ├── main.py            # FastAPI backend entry point
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   ├── routers/           # API routes (patients, doctors, appointments, NLP)
│
│── frontend/
│   ├── index.html         # Main dashboard
│   ├── patients.html      # Patients management
│   ├── doctors.html       # Doctors management
│   ├── appointments.html  # Appointments management
│   ├── nlp.html           # NLP form page
│   ├── nlp_results.html   # NLP results page
│   ├── static/            # JS & CSS files
│
│── README.md


---

🚀 Getting Started

1️⃣ Clone the Repository

git clone https://github.com/your-username/AI-Powered-EMRs.git
cd AI-Powered-EMRs

2️⃣ Setup Backend

cd backend
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt
uvicorn main:app --reload

Backend runs at: http://127.0.0.1:8000


3️⃣ Setup Frontend

cd frontend
# Simply open index.html in a browser (or use Live Server in VS Code)

Dashboard runs locally in your browser.

API requests go to backend: http://127.0.0.1:8000/



---

📖 API Endpoints

GET /patients/ → List all patients

POST /patients/ → Add new patient

GET /doctors/ → List all doctors

POST /doctors/ → Add new doctor

GET /appointments/ → List all appointments

POST /appointments/ → Create new appointment

POST /nlp/ → Process medical note

GET /nlp/ → View all saved NLP results



---

🧑‍💻 Contributing

1. Fork this repo


2. Create a new branch (feature-xyz)


3. Commit your changes


4. Push to your fork


5. Open a Pull Request 🚀




---

📜 License

This project is licensed under the MIT License – feel free to use and modify.


---

👨‍👩‍👦 Team Notes

Each module (patients, doctors, appointments) has its own HTML + JS file for easy separation of logic.
