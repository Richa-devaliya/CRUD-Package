// frontend/src/hooks/useUsers.js
import { useState, useEffect, useCallback } from 'react';
import apiClient from '../api/apiClient';

const useUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchUsers = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.get('/users/');
      setUsers(response.data);
    } catch (err) {
      setError('Failed to fetch users.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const addUser = async (user) => {
    try {
      const response = await apiClient.post('/users/', user);
      setUsers((prevUsers) => [...prevUsers, response.data]);
    } catch (err) {
        setError('Failed to add user.');
        console.error(err);
    }
  };

  const updateUser = async (id, updatedUser) => {
    try {
      const response = await apiClient.put(`/users/${id}`, updatedUser);
      setUsers((prevUsers) =>
        prevUsers.map((user) => (user.id === id ? response.data : user))
      );
    } catch (err) {
        setError('Failed to update user.');
        console.error(err);
    }
  };

  const deleteUser = async (id) => {
    try {
      await apiClient.delete(`/users/${id}`);
      setUsers((prevUsers) => prevUsers.filter((user) => user.id !== id));
    } catch (err) {
        setError('Failed to delete user.');
        console.error(err);
    }
  };

  return { users, addUser, updateUser, deleteUser, loading, error };
};

export default useUsers;