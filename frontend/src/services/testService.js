import api from '@/api';

export default {
    async getTest() {
        try {
            const response = await api().get('/models/all');
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }
};