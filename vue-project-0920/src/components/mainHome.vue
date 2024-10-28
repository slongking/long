<template>
  <div class="main-container" :class="{ 'dark-mode': isDark }">
    <!-- 头部菜单栏 -->
    <header class="header">
      <div class="header-container">
        <img :src="srcPath" class="logo">
        <nav class="top-nav">
          <el-menu
            default-active="1"
            class="top-nav-menu"
            mode="horizontal"
            :collapse="false"
          >
            <el-menu-item index="/"><RouterLink to="/">首页</RouterLink></el-menu-item>
            <el-menu-item index="2">数据集</el-menu-item>
            <el-menu-item index="/Api"><RouterLink to="/Api">数据API</RouterLink></el-menu-item>
            <el-menu-item index="4">机器学习</el-menu-item>
            <el-menu-item index="5">热点新闻</el-menu-item>
            <el-menu-item index="6">推荐阅读</el-menu-item>
            <el-menu-item index="7">
              <el-button class="toggle-btn" @click="toggleTheme">{{ isDark ? '深色模式' : '浅色模式' }}</el-button>
            </el-menu-item>
            <el-menu-item index="8">联系方式</el-menu-item>
          </el-menu>
        </nav>
      </div>
    </header>
    <!-- 主要内容 -->
    <main class="main" >
     <RouterView></RouterView>
    </main> 
    <!-- 页脚 -->
    <footer class="footer">
      <p>版权所有 © OldView旧参者 2024</p>
    </footer>
  </div>
</template>

<script lang="ts" setup>
import { ElMenu, ElMenuItem, ElButton } from 'element-plus';
import { useStorage } from '@/store/themsStore';
import { onMounted } from 'vue';
import { RouterView,RouterLink } from 'vue-router';
import blackLogo from '@/img/black-logo.png'; // 导入深色模式图标
import lightLogo from '@/img/light-logo.png'; // 导入浅色模式图标
import { ref} from 'vue';

const isDark = ref(true); // 初始模式
let srcPath = ref(lightLogo)
// 切换主题
const toggleTheme = () => {
  isDark.value = !isDark.value;
  srcPath = isDark.value ? ref(blackLogo) : ref(lightLogo)
  document.documentElement.style.setProperty('--main-bg-color', isDark.value ? '#090a0f' : '#f0f4f8');
  document.documentElement.style.setProperty('--text-color', isDark.value ? '#fff' : '#333');
  document.documentElement.style.setProperty('--header-bg-color', isDark.value ? '#1a2a3a' : '#ffffff');
  document.documentElement.style.setProperty('--header-box-shadow', isDark.value ? '0 2px 4px rgba(0, 0, 0, 0.2)' : '0 2px 4px rgba(0, 0, 0, 0.1)');
  document.documentElement.style.setProperty('--btn-gradient', isDark.value ? 'linear-gradient(to right, #74b9ff, #5589ff)' : 'linear-gradient(to right, #42b983, #22a6b3)');
  document.documentElement.style.setProperty('--btn-hover-gradient', isDark.value ? 'linear-gradient(to right, #5589ff, #74b9ff)' : 'linear-gradient(to right, #22a6b3, #42b983)');
  document.documentElement.style.setProperty('--footer-bg-color', isDark.value ? '#1a2a3a' : '#e0e4e8');
  document.documentElement.style.setProperty('--shape-bg-color', isDark.value ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)');
  document.documentElement.style.setProperty('--menu-text-color', isDark.value ? '#fff' : '#333'); // 菜单文字颜色
  document.documentElement.style.setProperty('--intro-text-color', isDark.value ? '#fff' : '#666'); // 介绍文字颜色
};

// 从本地存储加载主题
const storage = useStorage('theme', 'dark');
if (storage.value === 'light') {
  isDark.value = false;
}
onMounted(() => toggleTheme());
</script>

<style scoped>
:root {
  --main-bg-color: #090a0f;
  --text-color: #fff;
  --header-bg-color: #1a2a3a;
  --header-box-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);
  --btn-gradient: linear-gradient(to right, #74b9ff, #5589ff);
  --btn-hover-gradient: linear-gradient(to right, #5589ff, #74b9ff);
  --footer-bg-color: #1a2a3a;
  --shape-bg-color: rgba(255, 255, 255, 0.904);
  --menu-text-color: #fff;
  --intro-text-color: #fff;
}
.main {
  flex: 1;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  /* flex-direction: column; */
  padding: 30px 0;
  margin: 10px ;
  border-radius: 8px;
  overflow: hidden;
}
.main-container {
  font-family: 'Segoe UI', Tahoma, Verdana, sans-serif;

  background-color: var(--main-bg-color);
  color: var(--text-color);
  display: flex;
  height: 100%;
  flex-direction: column;

}

.header {
  background: var(--header-bg-color);
  padding: 8px 0;
  display: flex;
  justify-content: center;
  width: 100%;
  height: 15%;
  position: relative;
  z-index: 10;
  box-shadow: var(--header-box-shadow);
}

.header-container {
  width: 90%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0 auto;
}

.logo {
  width: 12%; /* 设置图片宽度 */
  height: auto; /* 高度自动，保持图片宽高比 */
  object-fit: contain; /* 保证图片完整地显示在容器内 */
  transition: filter 0.3s ease; /* 平滑过渡效果，用于hover等交互 */
}

.logo:hover {
  filter: brightness(1.2); /* 鼠标悬停时提亮图片 */
}



.top-nav-menu {
  border: none;
  background: rgba(0, 0, 0, 0.2);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border-radius: 2px;
}

.el-menu-item,
.el-submenu__title{
  font-size: 14px;
  font-weight: bold; 
  color: var(--menu-text-color);
  transition: color 0.3s ease, background-color 0.3s ease;
}

.el-menu-item:hover,
.el-submenu__title:hover,
.el-menu-item.is-active,
.el-submenu.is-active .el-submenu__title {
  color: #a5d8ff;
  background-color: rgba(255, 255, 255, 0.1);
}


.footer {
background: var(--footer-bg-color);
text-align: center;
height: 5%;
font-size: 14px;
border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.toggle-btn {
border: none;
background-color: transparent;
color: var(--text-color);
font-size: 14px;
cursor: pointer;
transition: color 0.3s ease;
}

.toggle-btn:hover {
color: #a5d8ff;
}
a {
  text-decoration: none; /* 去除所有链接的下划线 */
}
.router-view{
 flex: 1;
}
</style>