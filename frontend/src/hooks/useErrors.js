import { useToast } from 'primevue/usetoast';

export default () => {
const toast = useToast();

  function pushNotification(obj) {
    toast.add({
      severity: obj?.severity,
      summary: obj?.summary,
      detail: obj?.detail,
      life: obj?.life || 3000,
    });

  }


  return {
    pushNotification 
  };
}
