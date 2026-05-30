import axios from 'axios';

// Dynamically retrieve the API base URL from the environment or default to local Django development server
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const enrichCompany = async (url, websiteName = '') => {
  try {
    const response = await apiClient.post('/api/enrich/', {
      url: url,
      website_name: websiteName,
    });
    return response.data;
  } catch (error) {
    console.error('Error in enrichCompany service:', error);
    // Propagate standard structure to prevent UI breaks
    const message = error.response?.data?.error || error.message || 'Scraping/Enrichment failed';
    throw new Error(message);
  }
};

export const getResults = async () => {
  try {
    const response = await apiClient.get('/api/results/');
    return response.data;
  } catch (error) {
    console.error('Error in getResults service:', error);
    throw new Error(error.response?.data?.error || error.message || 'Failed to retrieve results');
  }
};
