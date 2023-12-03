const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '/sandbox',
        name: 'sandbox',
        component: () => import('@/views/Sandbox.vue')
      },
      {
        path: '/models',
        name: 'models',
        component: () => import('@/views/predictions/ModelsList.vue')
      }
    ]
  },  
]

export default routes;