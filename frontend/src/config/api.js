// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// API endpoints
export const API_ENDPOINTS = {
  // Chatbot endpoints
  CHATBOT_CHAT: `${API_BASE_URL}/api/chatbot/chat`,
  CHATBOT_PLACE_ORDER: `${API_BASE_URL}/api/chatbot/place-order`,
  
  // Recommendations endpoints
  TRENDING_BOOKS: `${API_BASE_URL}/api/recommendations/trending-books`,
  INITIAL_RECOMMENDATIONS: `${API_BASE_URL}/api/recommendations/initial-recommendations`,
  USER_PREFERENCES: `${API_BASE_URL}/api/recommendations/preferences`,
  
  // User endpoints (placeholder - these seem to be from old API)
  USER_INFO: `${API_BASE_URL}/api/v1/get-user-information`,
  UPDATE_ADDRESS: `${API_BASE_URL}/api/v1/update-address`,
  ORDER_HISTORY: `${API_BASE_URL}/api/v1/get-order-history`,
  FAVOURITE_BOOKS: `${API_BASE_URL}/api/v1/get-favourite-books`,
  USER_CART: `${API_BASE_URL}/api/v1/get-user-cart`,
  REMOVE_FROM_CART: (id) => `${API_BASE_URL}/api/v1/remove-from-cart/${id}`,
  PLACE_ORDER: `${API_BASE_URL}/api/v1/place-order`,
  ALL_BOOKS: `${API_BASE_URL}/api/v1/get-all-books`
};

export default API_BASE_URL;
