import axios from 'axios';

export default () => {
    const http = axios.create({
        baseURL: "basketball-api.happybush-f14b687c.westeurope.azurecontainerapps.io"

    });
    return http;
};