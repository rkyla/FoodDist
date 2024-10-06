import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const searchRestaurant = async (restaurantName: string) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/search/${encodeURIComponent(restaurantName)}`);
    return response.data;
  } catch (error) {
    console.error('Error searching restaurant:', error);
    throw error;
  }
};

export const getMenu = async (restaurantName: string) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/menu/${encodeURIComponent(restaurantName)}`);
    return response.data;
  } catch (error) {
    console.error('Error getting menu:', error);
    throw error;
  }
};