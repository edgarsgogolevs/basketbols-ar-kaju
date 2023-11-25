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
      }
    ]
  },

  //Stable
  // {
  //   path: '/',
  //   name: 'welcome',
  //   component: () => import('@/views/Welcome.vue'),
  //   // component: () => import('@/layouts/MainLayout.vue'),

  // },
  // {
  //   path: '/sandbox',
  //   name: 'sandbox',
  //   component: () => import('@/views/Sandbox.vue')
  // }
  
]


export default routes;