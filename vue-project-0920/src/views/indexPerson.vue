<template>
    <main class="main">
      <section class="personal-intro">
        <div class="avatar">
          <!-- 使用了相对路径来引用图片，请确保路径与您的项目结构匹配 -->
          <img src="@/img/indexPerson.jpg" alt="Avatar" />
        </div>
        <h2>你好，我是[你的名字]</h2>
        <p>我是一名[职业]，专注于[专业领域]。我在[公司/学校]工作，并且热爱[爱好或兴趣]。</p>
        <p>[一些关于你的详细信息，可以包括你的工作理念、职业目标等。]</p>
      </section>
      <section class="skills">
        <h3>技能</h3>
        <ul class="skills-list">
          <li>技能一：[技能描述]</li>
          <li>技能二：[技能描述]</li>
          <li>技能三：[技能描述]</li>
          <!-- 更多技能 -->
        </ul>
      </section>
      <section class="experience">
        <h3>工作经历</h3>
        <ul class="experience-list">
          <li>
            <strong>[公司名称]</strong> — [职位] <span>[年份]</span>
            <p>[工作描述]</p>
          </li>
          <!-- 更多工作经历 -->
        </ul>
      </section>
      <section class="education">
        <h3>教育背景</h3>
        <ul class="education-list">
          <li>
            <strong>[学校名称]</strong> — [专业] <span>[年份]</span>
            <p>[学习或成就描述]</p>
          </li>
          <!-- 更多教育背景 -->
        </ul>
      </section>
    </main>
  </template>
  
  <script>
  export default {
    name: "PersonalIntro"
  };
  </script>
  
  <style scoped>
  .main {
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    background-color: #ffffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin: 20px auto;
    max-width: 800px;
    text-align: center;
  }
  
  .personal-intro, .skills, .experience, .education {
    flex: 1;
    margin: 10px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;
  }
  
  .avatar img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin-bottom: 20px;
  }
  
  h2 {
    margin-top: 0;
    color: #333;
    font-size: 24px;
  }
  
  h3 {
    margin-top: 20px;
    color: #5b67d5;
    font-size: 20px;
  }
  
  .skills-list, .experience-list, .education-list {
    list-style: none;
    padding: 0;
  }
  
  .skills-list li, .experience-list li, .education-list li {
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eaeaea;
  }
  
  /* 响应式设计 */
  @media (max-width: 768px) {
    .main {
      flex-direction: column;
    }
    .personal-intro, .skills, .experience, .education {
      margin: 10px 0;
    }
  }
  </style>