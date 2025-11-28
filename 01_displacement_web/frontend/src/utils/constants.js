export const API_BASE_URL = process.env.REACT_APP_API_URL 
  ? `${process.env.REACT_APP_API_URL}/api`
  : 'http://127.0.0.1:5000/api';

export const BOGOTA_COORDS = [4.5981, -74.0758];

export const COLORS = {
  BOGOTA: '#E74C3C',
  SELECTED: '#2ECC71',
  OTHERS: '#D5D8DC',
  AXIS: '#34495E',
  LINE: '#7F8C8D'
};