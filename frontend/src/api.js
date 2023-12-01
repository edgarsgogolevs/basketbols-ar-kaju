import axios from 'axios';

export default () => {
    const http = axios.create({
        baseURL: "http://localhost:8069/"

    });
    return http;
};