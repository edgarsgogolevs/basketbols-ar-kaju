import axios from 'axios';

export default () => {
    const https = axios.create({
        baseURL: "https://api.dev-goga.net"
    });
    return https;
};