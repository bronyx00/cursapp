import { defineStore } from "pinia";
import apiClient from "@/services/apiClient";
import type { LeaderboardUser } from "@/types/gamification.types";

export const useGamificationStore = defineStore('gamification', {
    state: () => ({
        leaderboard: [] as LeaderboardUser[],
        isLoading: false,
    }),
    actions: {
        async fetchLeaderboard() {
            if (this.leaderboard.length > 0) return;

            this.isLoading = true;
            try {
                // Llama al endpoint del backend
                const { data } = await apiClient.get('/evaluacion/leaderboard/');
                this.leaderboard = data.results;
            } catch (error) {
                console.error("Error al cargar el Leaderboard:", error);
            } finally {
                this.isLoading = true;
            }
        }
    }
});