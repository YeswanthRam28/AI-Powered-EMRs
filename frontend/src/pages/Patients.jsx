import { useEffect, useState } from "react";
import axios from "axios";
import Modal from "react-modal";
import { useTable, usePagination, useGlobalFilter } from "react-table";

Modal.setAppElement("#root");

export default function Patients() {
  const [patients, setPatients] = useState([]);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [form, setForm] = useState({ name: "", age: "" });
  const [editingId, setEditingId] = useState(null);
  const [search, setSearch] = useState("");

  useEffect(() => { fetchPatients(); }, []);

  const fetchPatients = () => {
    axios.get("http://localhost:8000/patients/")
      .then(res => setPatients(res.data))
      .catch(console.error);
  };

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const openModal = (patient = null) => {
    if (patient) { setForm({ name: patient.name, age: patient.age.toString() }); setEditingId(patient.id); }
    else { setForm({ name: "", age: "" }); setEditingId(null); }
    setModalIsOpen(true);
  };

  const closeModal = () => setModalIsOpen(false);

  const handleSubmit = e => {
    e.preventDefault();
    const request = editingId 
      ? axios.put(`http://localhost:8000/patients/${editingId}`, form)
      : axios.post("http://localhost:8000/patients/", form);

    request.then(() => { fetchPatients(); closeModal(); })
           .catch(console.error);
  };

  const handleDelete = id => { axios.delete(`http://localhost:8000/patients/${id}`).then(fetchPatients); };

  const data = patients.filter(p => p.name.toLowerCase().includes(search.toLowerCase()));
  const columns = [
    { Header: "Name", accessor: "name" },
    { Header: "Age", accessor: "age" },
    { Header: "Actions", Cell: ({ row }) => (
      <>
        <button onClick={() => openModal(row.original)}>Edit</button>
        <button onClick={() => handleDelete(row.original.id)}>Delete</button>
      </>
    )}
  ];

  const tableInstance = useTable({ columns, data, initialState: { pageSize: 5 } }, useGlobalFilter, usePagination);
  const { getTableProps, getTableBodyProps, headerGroups, page, prepareRow, nextPage, previousPage, canNextPage, canPreviousPage, state } = tableInstance;

  return (
    <div>
      <h1>Patients</h1>
      <button onClick={() => openModal()}>Add Patient</button>
      <input placeholder="Search..." value={search} onChange={e => setSearch(e.target.value)} />

      <table {...getTableProps()} style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(col => <th {...col.getHeaderProps()} style={{ border: "1px solid #ddd", padding: "8px" }}>{col.render("Header")}</th>)}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map(row => { prepareRow(row); return (
            <tr {...row.getRowProps()}>
              {row.cells.map(cell => <td {...cell.getCellProps()} style={{ border: "1px solid #ddd", padding: "8px" }}>{cell.render("Cell")}</td>)}
            </tr>
          ); })}
        </tbody>
      </table>

      <div>
        <button onClick={() => previousPage()} disabled={!canPreviousPage}>Previous</button>
        <button onClick={() => nextPage()} disabled={!canNextPage}>Next</button>
        <span>Page: {state.pageIndex + 1}</span>
      </div>

      <Modal isOpen={modalIsOpen} onRequestClose={closeModal} contentLabel="Patient Form">
        <h2>{editingId ? "Edit Patient" : "Add Patient"}</h2>
        <form onSubmit={handleSubmit}>
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
          <input name="age" type="number" placeholder="Age" value={form.age} onChange={handleChange} required />
          <button type="submit">{editingId ? "Update" : "Add"}</button>
          <button type="button" onClick={closeModal}>Cancel</button>
        </form>
      </Modal>
    </div>
  );
}
