import Vue from 'vue';
import Router from 'vue-router';

// Containers
const TheContainer = () => import('@/containers/TheContainer');

// Views
const Dashboard = () => import('@/views/Dashboard');

const AnaylzeAll = () => import('@/views/anaylze/AnaylzeAll');
const OneToOne = () => import('@/views/anaylze/OneToOne');

const Overview = () => import('@/views/breakdown/Overview');
const Fundamental = () => import('@/views/breakdown/Fundamental');
const Technical = () => import('@/views/breakdown/Technical');
const Sec = () => import('@/views/breakdown/Sec');
const PriceAction = () => import('@/views/breakdown/PriceAction');

const FuturePriceAction = () => import('@/views/future/FuturePriceAction');


Vue.use(Router);

const router = new Router({
  mode: 'hash', // https://router.vuejs.org/api/#mode
  linkActiveClass: 'active',
  scrollBehavior: () => ({ y: 0 }),
  routes: configRoutes()
});

function configRoutes() {
  return [
    {
      path: '/',
      redirect: '/dashboard',
      name: 'Home',
      component: TheContainer,
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: Dashboard
        },
        {
          path: 'anaylze',
          redirect: '/anaylze',
          name: 'Anaylze',
          component: {
            render(c) { return c('router-view'); }
          },
          children: [
            {
              path: 'all',
              name: 'Anaylze',
              component: AnaylzeAll
            },
            {
              path: 'one-to-one',
              name: 'One To One',
              component: OneToOne
            }
          ]
        },
        {
          path: 'breakdown',
          redirect: '/overview',
          name: 'Breakdown',
          component: {
            render(c) { return c('router-view'); }
          },
          children: [
            {
              path: 'overview',
              name: 'Overview',
              component: Overview
            },
            {
              path: 'fundamentals',
              name: 'Fundamentals',
              component: Fundamental
            },
            {
              path: 'technicals',
              name: 'Technicals',
              component: Technical
            },
            {
              path: 'price',
              name: 'Price Action',
              component: PriceAction
            },
            {
              path: 'sec',
              name: 'SEC',
              component: Sec
            }
          ]
        },
        {
          path: 'future',
          redirect: '/price',
          name: 'Future Price Action',
          component: {
            render(c) { return c('router-view'); }
          },
          children: [
            {
              path: 'price',
              name: 'Future Price Action',
              component: FuturePriceAction
            }
          ]
        }
      ]
    }
  ];
}

export default router;

