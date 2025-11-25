import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getModels = () => api.get('/models');

export const getVariables = () => api.get('/variables');

export const getDepartments = () => api.get('/departments');

export const getDepartmentGeo = (deptName) => api.get(`/department_geo/${deptName}`);

export const validateYear = (year) => api.post('/validate_year', { year });

export const predict = (data) => api.post('/predict', data);

export const getRandomValues = () => api.get('/random');

export default api;
