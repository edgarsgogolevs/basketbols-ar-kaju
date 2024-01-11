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
            const response = await api().get(`/models/${id}`);
            return response;
        } catch (error) {
            console.error(error);
        }
    },
    async getModel(id) {
        try {
            const response = await api().get(`/models/${id}`);
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
    },
    async getUpcomingGames(count) {
        try {
            const response = await api().get(`/games/upcoming/${count}`);
            return response;
        } catch (error) {
            console.error(error);
        }
    },
    async getRecentGames(count) {
        try {
            const response = await api().get(`/games/recent/${count}`);
            return response;
        } catch (error) {
            console.error(error);
        }
    },
    async getPrediction(game, model) {
        try {
            const response = await api().get(`/predictions/predict_game/${game}/${model}`);
            return response;
        } catch (error) {
            console.error(error);
        }
    }
};