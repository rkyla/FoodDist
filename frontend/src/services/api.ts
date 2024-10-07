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

export const computeSimilarities = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/compute_similarities`);
    console.log('Computed similarities:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error computing similarities:', error);
    throw error;
  }
};

export const analyzeMatches = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/analyze_matches`);
    console.log('Match analysis:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error analyzing matches:', error);
    throw error;
  }
};