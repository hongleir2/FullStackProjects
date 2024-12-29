import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
})

api.interceptors.request.use((config)=>{
    const token = localStorage.getItem('token');
    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('Request:', config);
    return config;
})

api.interceptors.response.use((response)=>{
    console.log('Response:', response);
    return response;
}, (error)=>{
    console.log('Error:', error);
    return Promise.reject(error);
});

export default api;