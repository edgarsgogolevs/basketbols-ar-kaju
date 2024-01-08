import axios from 'axios';

export default () => {
    const https = axios.create({
        baseURL: "https://basketball-api.wittyhill-90bf33eb.westeurope.azurecontainerapps.io"
    });
    return https;
};