// frontend/src/App.jsx
import React, { useState } from 'react';
import useUsers from './hooks/useUsers';
import UsersTable from './components/UsersTable';
import UserForm from './components/UserForm';
import './App.css';

function App() {
  const { users, addUser, updateUser, deleteUser, loading, error } = useUsers();
  const [editingUser, setEditingUser] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleEdit = (user) => {
    setEditingUser(user);
    setIsModalOpen(true);
  };

  const handleDelete = (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      deleteUser(userId);
    }
  };

  const handleSave = (user) => {
    if (user.id) {
      updateUser(user.id, user);
    } else {
      addUser(user);
    }
    closeModal();
  };
  
  const openModal = () => {
    setEditingUser(null);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingUser(null);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">User Management</h1>
      <button
        onClick={openModal}
        className="bg-blue-500 text-white px-4 py-2 rounded mb-4 hover:bg-blue-600"
      >
        Add User
      </button>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      
      {!loading && !error && (
        <UsersTable users={users} onEdit={handleEdit} onDelete={handleDelete} />
      )}

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-8 rounded-lg shadow-lg w-1/3">
            <h2 className="text-xl font-bold mb-4">{editingUser ? 'Edit User' : 'Add User'}</h2>
            <UserForm user={editingUser} onSave={handleSave} onCancel={closeModal} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;