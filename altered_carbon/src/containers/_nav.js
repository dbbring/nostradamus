export default [
  {
    _name: 'CSidebarNav',
    _children: [
      {
        _name: 'CSidebarNavItem',
        _class: 'text-white',
        name: 'Dashboard',
        to: '/dashboard',
        icon: { name: 'cil-speedometer', class: 'text-white' },
      },
      {
        _name: 'CSidebarNavTitle',
        _children: ['Anaylze']
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Anaylze',
        to: '/anaylze/all',
        icon: 'cil-chart-pie'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'One To One',
        to: '/anaylze/one-to-one',
        icon: 'cil-calculator'
      },
      {
        _name: 'CSidebarNavTitle',
        _children: ['Breakdown']
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Overview',
        to: '/breakdown/overview',
        icon: 'cil-calculator',
      },
      {
        _name: 'CSidebarNavItem',
        name: 'SEC',
        to: '/breakdown/sec',
        icon: 'cil-chart-pie'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Fundamentals',
        to: '/breakdown/fundamentals',
        icon: 'cil-chart-pie'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Technicals',
        to: '/breakdown/technicals',
        icon: 'cil-chart-pie'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Price Action',
        to: '/breakdown/price',
        icon: 'cil-chart-pie'
      },
      {
        _name: 'CSidebarNavTitle',
        _children: ['Future Price Movement']
      },
      {
        _name: 'CSidebarNavItem',
        name: '5 Days From The Date',
        to: '/future/price',
        icon: 'cil-calculator'
      },
    ]
  }
];