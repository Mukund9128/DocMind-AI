import axios from 'axios';

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    'http://localhost:5000/api'
});

// Add JWT token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);


// Handle expired or invalid JWT
api.interceptors.response.use(
  (response) => response,

  (error) => {
    const status = error.response?.status;

    const message =
      error.response?.data?.msg ||
      error.response?.data?.error ||
      '';

    const authError =
      status === 401 &&
      (
        message.toLowerCase().includes('token') ||
        message.toLowerCase().includes('authorization')
      );

    if (authError) {
      localStorage.removeItem('token');

      // Return user to login screen
      window.location.href = '/';
    }

    return Promise.reject(error);
  }
);

export default api;