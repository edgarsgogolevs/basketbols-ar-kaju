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
      },
      {
        path: '/teams',
        name: 'teams',
        component: () => import('@/views/Teams.vue')
      },
      {
        path: '/model/:id',
        name: 'model.view',
        props: (route) => ({ id: Number(route.params.id) }),
        component: () => import('@/views/predictions/ModelView.vue')
      }
    ]
  },  
]

export default routes;