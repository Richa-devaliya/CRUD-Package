// frontend/src/api/apiClient.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // Your backend API base URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;