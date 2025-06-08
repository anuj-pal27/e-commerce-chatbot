import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Configure axios defaults
axios.defaults.withCredentials = true;

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor to handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 403) {
      console.error('CSRF Error:', error.response.data);
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  signup: (userData) => api.post('/auth/signup/', userData),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
};

// Chat API
export const chatAPI = {
  // Session management
  getSessions: () => api.get('/chat/sessions/'),
  createSession: () => api.post('/chat/sessions/'),
  getSession: (sessionId) => api.get(`/chat/sessions/${sessionId}/`),
  deleteSession: (sessionId) => api.delete(`/chat/sessions/${sessionId}/`),
  resetSession: (sessionId) => api.post(`/chat/sessions/${sessionId}/reset/`),
  
  // Messages
  getMessages: (sessionId) => api.get(`/chat/sessions/${sessionId}/messages/`),
  sendMessage: (sessionId, content) => api.post(`/chat/sessions/${sessionId}/messages/`, { content }),
};

// Products API
export const productsAPI = {
  getProducts: (params = {}) => api.get('/products/', { params }),
  getProduct: (id) => api.get(`/products/${id}/`),
  searchProducts: (searchData) => api.post('/products/search/', searchData),
};

export default api; 