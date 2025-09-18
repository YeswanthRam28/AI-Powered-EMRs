import { useEffect, useState } from "react";
import axios from "axios";

export default function Doctors() {
  const [doctors, setDoctors] = useState([]);
  const [name, setName] = useState("");
  const [specialty, setSpecialty] = useState("");
  const [editingId, setEditingId] = useState(null);

  const fetchDoctors = () => {
    axios.get("http://localhost:8000/doctors/")
      .then(res => setDoctors(res.data))
      .catch(err => console.error(err));
  };

  useEffect(() => fetchDoctors(), []);

  const handleAdd = () => {
    if (!name || !specialty) return alert("Fill all fields");
    axios.post("http://localhost:8000/doctors/", { name, specialty })
      .then(() => { setName(""); setSpecialty(""); fetchDoctors(); })
      .catch(err => console.error(err));
  };

  const handleEdit = (doctor) => {
    setName(doctor.name);
    setSpecialty(doctor.specialty);
    setEditingId(doctor.id);
  };

  const handleUpdate = () => {
    axios.put(`http://localhost:8000/doctors/${editingId}`, { name, specialty })
      .then(() => { setName(""); setSpecialty(""); setEditingId(null); fetchDoctors(); })
      .catch(err => console.error(err));
  };

  const handleDelete = (id) => {
    axios.delete(`http://localhost:8000/doctors/${id}`)
      .then(() => fetchDoctors())
      .catch(err => console.error(err));
  };

  return (
    <div>
      <h1>Doctors</h1>
      <div>
        <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
        <input placeholder="Specialty" value={specialty} onChange={e => setSpecialty(e.target.value)} />
        {editingId ? 
          <button onClick={handleUpdate}>Update</button> : 
          <button onClick={handleAdd}>Add</button>
        }
      </div>
      <table border="1" cellPadding="5" style={{ marginTop: 10 }}>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Specialty</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {doctors.map(d => (
            <tr key={d.id}>
              <td>{d.id}</td>
              <td>{d.name}</td>
              <td>{d.specialty}</td>
              <td>
                <button onClick={() => handleEdit(d)}>Edit</button>
                <button onClick={() => handleDelete(d.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
