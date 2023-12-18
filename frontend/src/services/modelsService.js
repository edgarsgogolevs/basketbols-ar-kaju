import api from '@/api';

export default {
    async getAllModels() {
        try {
            const response = await api().get('/models/all');
            return response;
        } catch (error) {
            console.error(error);
        }
    }
};