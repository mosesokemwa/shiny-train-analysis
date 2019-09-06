import axios from "axios";

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL
});

api.interceptors.request.use(function (config) {
    const token = localStorage.getItem('user_token');
    if (token){
        config = {
            ...config,
            headers: {
                ...config.headers,
                'Authorization': `Bearer ${token}`
            }
        }
    }
    return config
});

export default api;