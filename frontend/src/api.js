import axios from 'axios';

export default () => {
    const https = axios.create({
        baseURL: "https://basketball-api.happybush-f14b687c.westeurope.azurecontainerapps.io"
    });
    return https;
};