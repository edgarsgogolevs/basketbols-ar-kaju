import { useNavigatingStore } from '@/stores/useNavigatingStore'

export default (router) => {
    router.beforeEach(async (to, from, next) => {
        const navigatingStore = useNavigatingStore();
        await navigatingStore.startNavigation();
        next();
    });
    
    router.afterEach(async () => {
        const navigatingStore = useNavigatingStore();
        await navigatingStore.stopNavigation();
    });
}