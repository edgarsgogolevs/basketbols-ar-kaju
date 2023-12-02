import { defineStore } from 'pinia';

export const useNavigatingStore = defineStore('navigating', {
  state: () => ({
    isNavigating: false,
  }),
  actions: {
    startNavigation() {
      this.isNavigating = true;
    },
    stopNavigation() {
      this.isNavigating = false;
    }
  }
});