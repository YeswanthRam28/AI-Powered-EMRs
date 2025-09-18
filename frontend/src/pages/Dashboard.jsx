import { useEffect, useState } from "react";
import axios from "axios";
import Modal from "react-modal";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell, Legend } from "recharts";

Modal.setAppElement("#root");

export default function Dashboard() {
  const [stats, setStats] = useState({ total_patients: 0, total_doctors: 0, total_appointments: 0, appointments_per_doctor: [], patients_per_doctor: [] });
  const [modalIsOpen, setModalIsOpen] = useState(false);

  useEffect(() => { fetchStats(); }, []);

  const fetchStats = () => {
    axios.get("http://localhost:8000/dashboard/")
      .then(res => setStats(res.data))
      .catch(console.error);
  };

  const openModal = () => setModalIsOpen(true);
  const closeModal = () => setModalIsOpen(false);

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#AA00FF", "#FF0066"];

  return (
    <div>
      <h1>Dashboard</h1>
      <div style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
        <div>Total Patients: {stats.total_patients}</div>
        <div>Total Doctors: {stats.total_doctors}</div>
        <div>Total Appointments: {stats.total_appointments}</div>
      </div>

      <button onClick={openModal}>Filter Charts</button>

      <div style={{ display: "flex", gap: "50px", flexWrap: "wrap", marginTop: "20px" }}>
        <BarChart width={400} height={300} data={stats.appointments_per_doctor}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="doctor_name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="appointments" fill="#8884d8" />
        </BarChart>

        <PieChart width={400} height={300}>
          <Pie
            data={stats.patients_per_doctor}
            dataKey="patients"
            nameKey="doctor_name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#82ca9d"
            label
          >
            {stats.patients_per_doctor.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>

      <Modal isOpen={modalIsOpen} onRequestClose={closeModal} contentLabel="Filter Charts">
        <h2>Filter Charts</h2>
        {/* Add your filter inputs here */}
        <p>Example: Filter by date range, doctor, or patient type.</p>
        <button onClick={closeModal}>Close</button>
      </Modal>
    </div>
  );
}
