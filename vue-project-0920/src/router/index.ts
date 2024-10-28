//创建一个路由器并暴漏出去
import {createRouter,createWebHistory} from  'vue-router'
import indexPerson from '@/views/indexPerson.vue'
import indexHome from '@/views/indexHome.vue' 
import indexApi from '@/views/indexApi.vue'
//创建路由器
 const router = createRouter({
     history:createWebHistory(),
     routes:[{
        name:'webHome',
        path:'/Home',
        component:indexHome,
       
    },{
        path:"/",
        redirect:'/Home'
    },{
        name:'webPerson',
        path:'/Person',
        component:indexPerson,
       
    },
    {
        name:'webApi',
        path:'/Api',
        component:indexApi,
       
    },]
 })
 //暴漏规则
 export default router