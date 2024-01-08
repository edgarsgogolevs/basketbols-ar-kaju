import api from '@/api';

export default {
    async getAllModels() {
        try {
            const response = await api().get('/models/all');
            return response;
        } catch (error) {
            console.error(error);
        }
    },
    async getModelById(id) {
        try {
            const response = await api().get(`/models/${id}/stats`);
            return response;
        } catch (error) {
            console.error(error);
        }
    },
    async getAllTeams() {
        try {
            const response = await api().get('/teams/all');
            return response;
        } catch (error) {
            console.error(error);
        }
    }
};