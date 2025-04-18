import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    headers: {
        'Content-Type': 'application/json',
    }
});

// Set up a function to call the backend for logging in a user
export const loginUser = async (email, password) => {
    try {
        const response = await api.post('/login', {email, password});
        return response.data;
    } catch (error) {
        throw new Error('Login failed');
    }
};

// TODO Add more API calls
