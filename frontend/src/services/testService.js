import api from '@/api';

export default {
    async getTest() {
        try {
            const response = await api().get('/');
            return response.data;
        } catch (error) {
            console.log(error);
        }
    }
};