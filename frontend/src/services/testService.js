import api from '@/api';

export default {
    async getTest() {
        try {
            const response = await api().get('/predictions/predict_games/1');
            return response.data;
        } catch (error) {
            console.error(error);
        }
    }
};