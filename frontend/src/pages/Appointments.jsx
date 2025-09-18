import { useEffect, useState } from "react";
import axios from "axios";

export default function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const [patient, setPatient] = useState("");
  const [doctor, setDoctor] = useState("");
  const [date, setDate] = useState("");
  const [editingId, setEditingId] = useState(null);

  const fetchAppointments = () => {
    axios.get("http://localhost:8000/appointments/")
      .then(res => setAppointments(res.data))
      .catch(err => console.error(err));
  };

  useEffect(() => fetchAppointments(), []);

  const handleAdd = () => {
    if (!patient || !doctor || !date) return alert("Fill all fields");
    axios.post("http://localhost:8000/appointments/", { patient, doctor, date })
      .then(() => { setPatient(""); setDoctor(""); setDate(""); fetchAppointments(); })
      .catch(err => console.error(err));
  };

  const handleEdit = (a) => {
    setPatient(a.patient);
    setDoctor(a.doctor);
    setDate(a.date);
    setEditingId(a.id);
  };

  const handleUpdate = () => {
    axios.put(`http://localhost:8000/appointments/${editingId}`, { patient, doctor, date })
      .then(() => { setPatient(""); setDoctor(""); setDate(""); setEditingId(null); fetchAppointments(); })
      .catch(err => console.error(err));
  };

  const handleDelete = (id) => {
    axios.delete(`http://localhost:8000/appointments/${id}`)
      .then(() => fetchAppointments())
      .catch(err => console.error(err));
  };

  return (
    <div>
      <h1>Appointments</h1>
      <div>
        <input placeholder="Patient" value={patient} onChange={e => setPatient(e.target.value)} />
        <input placeholder="Doctor" value={doctor} onChange={e => setDoctor(e.target.value)} />
        <input type="date" value={date} onChange={e => setDate(e.target.value)} />
        {editingId ? 
          <button onClick={handleUpdate}>Update</button> : 
          <button onClick={handleAdd}>Add</button>
        }
      </div>
      <table border="1" cellPadding="5" style={{ marginTop: 10 }}>
        <thead>
          <tr><th>ID</th><th>Patient</th><th>Doctor</th><th>Date</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {appointments.map(a => (
            <tr key={a.id}>
              <td>{a.id}</td>
              <td>{a.patient}</td>
              <td>{a.doctor}</td>
              <td>{a.date}</td>
              <td>
                <button onClick={() => handleEdit(a)}>Edit</button>
                <button onClick={() => handleDelete(a.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
