<template>
      <div class="content">
        <div class="quote-display" >
          <transition name="fade">
            <div v-if="show" class="quote" :style="quoteStyle" :class="quoteClass">
              {{ quote }}
            </div>
          </transition>
        </div>
        <h1 class="title" v-on:click="showQuote">探索未来科技</h1>
        <p class="subtitle" v-on:click="showQuote">引领科技前沿，探索无限可能</p>
        <el-button class="explore-btn" type="primary">探索更多</el-button>
      </div>

      <div class="background-shapes" v-on:click="showQuote">
        <div class="shape shape1"></div>
        <div class="shape shape2"></div>
        <div class="shape shape3"></div>
        <div class="shape shape4"></div>
      </div>
</template>
<script setup lang="ts">
import { useStorage } from '@/store/themsStore';
import { onMounted } from 'vue';
import blackLogo from '@/img/black-logo.png'; // 导入深色模式图标
import lightLogo from '@/img/light-logo.png'; // 导入浅色模式图标
import { ref, computed } from 'vue';
const show = ref(false);
const quote = ref('');
const quoteColor = ref('#fff');
const randomX = ref(0);
const randomY = ref(0);

const quotes = [
"人活在世，不过一场美丽的寄居。",
  "活着不一定要鲜艳，但一定要有自己的颜色。",
  "人类文化的悲哀，是流俗的易传、高雅的失传。",
  "在每个死胡同的尽头，都有另一个维度的天空。",
  "生命的意义在于付出，在于给予。",
  "善于利用零星时间的人，会做出更大的成绩来。",
  "少而好学，如日出之阳；壮而好学，如日中之光；老而好学，如炳烛之明。",
  "人生的价值，即以其人对于当代所做的工作为尺度。",
  "芸芸众生，孰不爱生？爱生之极，进而爱群。",
  "生活真象这杯浓酒，不经三番五次的提炼呵，就不会这样可口！",
  "纵使黑夜吞噬了一切，太阳还可以重新回来。",
  "一条路并不因为它路边长满荆棘而丧失其美丽。",
  "如同明日将死那样生活，如同永远不死那样求知。",
  "愿望是半个生命，淡漠是半个死亡。",
  "不存在十全十美的文章，如同不存在彻头彻尾的绝望。",
  "生命的定义就是拥有明天。",
  "开成花灾的玫瑰不是灿烂，而是荒凉。",
  "与其在绝望和挣扎中苟活，不如在希冀和盼望中死亡。",
  "在逆风里把握方向，做暴风雨中的海燕。",
  "人一辈子都在高潮——低潮中浮沉。",
  "在自己身上，克服这个时代。",
  "万人都要将火熄灭，我一人独将此火高高举起。",
  "历史是一堆灰烬，但灰烬深处有余温。",
  "此处果有可乐，我即别无所思。",
  "人要有出世的精神才可以做入世的事业。",
  "名不显时心不朽，再挑灯火看文章。",
  "教育不是注满一桶水，而是点燃一把火。",
  "不可乘快而多事，不可因倦而鲜终。",
  "一个人的行动，比他所说的话，更有详细的表现。",
  "一花凋零，荒芜不了整个春天。",
  "读书使人充实，思考使人深邃，交谈使人清醒。",
  "青春是一种持续的陶醉，是理智的狂热。",
  "只有永远躺在泥坑里的人，才不会再掉进坑里。",
  "每一个不曾起舞的日子，都是对生命的辜负。",
  "人生应该如蜡烛一样，一直都是光明的。",
  "真正的人生，只有在经过艰难卓绝的斗争之后才能实现。",
  "顽强的毅力可以征服世界上任何一座高峰。",
  "早知今日读书是，悔作从前任侠非。",
  "生活最沉重的负担不是工作，而是无聊。",
  "千里之行，始于足下。",
  "少年易学老难成，一寸光阴不可轻。",
  "敏而好学，不耻下问。",
  "天生我材必有用。",
  "人生贵相知，何用金与钱。",
  "海内存知已，天涯若比邻。",
  "月缺不改光，剑折不改刚。",
  "莫愁前路无知已，天下谁人不识君。",
  "海纳百川有容乃大；壁立千仞无欲则刚。",
  "穷则独善其身，达则兼济天下。",
  "自由自由，多少罪恶假汝之名以行。",
  "即使被关在果壳之中，我仍自以为是无限宇宙之王。",
  "我不同意你说的每一句话，但我誓死捍卫你说话权利的自由。",
  "生命，那是自然付给人类去雕琢的宝石。",
  "书是人类进步的阶梯，终生的伴侣，最诚挚的朋友。",
  "为伟大的事业捐躯，从来就不能算作失败。",
  "新的方法和概念，常常比解决问题本身更重要。",
  "成大事不在于力量的大小，而在于能坚持多久。",
  "人所缺乏的不是才干而是志向，不是成功的能力而是勤劳的意志。",
  "只有经历过地狱般的磨砺，才能练就创造天堂的力量。",
  "心若改变，你的态度跟着改变；态度改变，你的习惯跟着改变。",
  "有两件事我最憎恶：没有信仰的博才多学和充满信仰的愚昧无知。",
  "谁终将声震人间，必长久深自缄默。",
  "仿佛前世的密约，注定我们要在今生抵掌。",
  "如果是玫瑰，它总会开花的。",
  "失败是坚忍的最后考验。",
  "辛勤的蜜蜂永没有时间悲哀。",
  "冬天已经到来，春天还会远吗？",
  "生命不止，奋斗不息。",
  "人生不是一种享乐，而是一桩十分沉重的工作。",
  "时间是伟大的作者，她能写出未来的结局。",
  "志向和热爱是伟大行为的双翼。",
  "我这个人走得很慢，但是我从不后退。",
  "一个人几乎可以在任何他怀有无限热忱的事情上成功。",
  "深窥自己的心，而后发觉一切的奇迹在你自己。",
  "失败也是我需要的，它和成功对我一样有价值。",
  "人需要真理，就像瞎子需要明快的引路人一样。",
  "任何问题都有解决的办法，无法可想的事是没有的。",
  "每一种挫折或不利的突变，是带着同样或较大的有利的种子。",
  "只要朝着一个方向努力，一切都会变得得心应手。",
  "人的一生可能燃烧也可能腐朽，我不能腐朽，我愿意燃烧起来!",
  "你若要喜爱你自己的价值，你就得给世界创造价值。",
  "生活的情况越艰难，我越感到自己更坚强，甚而也更聪明。",
  "人生不是一种享乐，而是一桩十分沉重的工作。",
  "人只有献身于社会，才能找出那短暂而有风险的生命的意义。",
  "一个人能否有成就，只看他是否具备自尊心与自信心两个条件。",
  "生活在我们这个世界里，不读书就完全不可能了解人。",
  "没有目的，就做不成任何事情；目的渺小，就做不成任何大事。",
  "进步，意味着目标不断前移，阶段不断更新，它的视影不断变化。",
  "你以为挑起生活的担子是勇气，其实去过自己真正想要的生活才更需要勇气。",
  "生活赋予我们一种巨大的和无限高贵的礼品，这就是青春。",
  "感情有着极大的鼓舞力量，因此，它是一切道德行为的重要前提。",
  "只有经历过地狱般的磨砺，才能弹奏出天籁之音。",
  "有两件事我最憎恶：没有信仰的博学多才和充满信仰的愚昧无知。",
  "谁终将声震人间，必长久深自缄默；谁终将点燃闪电，必长久如云漂泊。",
  "仿佛前世的密约，注定我们要在今生抵掌，然后一起创世。",
  "如果是玫瑰，它总会开花的。",
  "失败是坚忍的最后考验。",
  "辛勤的蜜蜂永没有时间悲哀。",
  "冬天已经到来，春天还会远吗？",
  "生命不止，奋斗不息。",
  "时间是伟大的作者，她能写出未来的结局。",
  "我这个人走得很慢，但是我从不后退。",
  "一个人几乎可以在任何他怀有无限热忱的事情上成功。",
  "深窥自己的心，而后发觉一切的奇迹在你自己。",
  "失败也是我需要的，它和成功对我一样有价值。",
  "任何问题都有解决的办法，无法可想的事是没有的。",
  "每一种挫折或不利的突变，是带着同样或较大的有利的种子。",
  "只要朝着一个方向努力，一切都会变得得心应手。",
  "人的一生可能燃烧也可能腐朽，我不能腐朽，我愿意燃烧起来!",
  "你若要喜爱你自己的价值，你就得给世界创造价值。",
  "生活的情况越艰难，我越感到自己更坚强，甚而也更聪明。",
  "人只有献身于社会，才能找出那短暂而有风险的生命的意义。",
  "一个人能否有成就，只看他是否具备自尊心与自信心两个条件。",
  "生活在我们这个世界里，不读书就完全不可能了解人。",
  "没有目的，就做不成任何事情；目的渺小，就做不成任何大事。",
  "进步，意味着目标不断前移，阶段不断更新，它的视影不断变化。",
  "你以为挑起生活的担子是勇气，其实去过自己真正想要的生活才更需要勇气。",
  "生活赋予我们一种巨大的和无限高贵的礼品，这就是青春。",
];

const showQuote = (event:any) => {
  const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
  quote.value = randomQuote;

  // 随机设置字体颜色
  quoteColor.value = `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)})`;

  const x = event.clientX;
  const y = event.clientY;

  // 显示名言
  show.value = true;

  // 设置定时器，3秒后隐藏名言
  setTimeout(() => {
    show.value = false;
  }, 5000);
};

const quoteStyle = computed(() => {
  return {
    color: quoteColor.value,

    fontFamily: randomFont(),
  };
});

const quoteClass = computed(() => ({
  fade: show.value
}));

function randomFont() {
  const fonts = ['Arial', 'Verdana', 'Georgia', 'Times New Roman', 'Courier New'];
  return fonts[Math.floor(Math.random() * fonts.length)];
}
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


.content {
  z-index: 2;
  text-align: center;
  position: relative;
  color: var(--intro-text-color);
}

.title {
  font-size: 48px;
  color: #74b9ff;
  margin-bottom: 20px;
}

.subtitle {
  font-size: 18px;
  color: var(--intro-text-color);
  margin-bottom: 40px;
}

.explore-btn {
  padding: 12px 25px;
  border-radius: 4px;
  background: var(--btn-gradient);
  color: #000;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.3s ease;
}

.explore-btn:hover {
  background: var(--btn-hover-gradient);
  transform: translateY(-5px);
}

.background-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 1;
}

.shape {
  position: absolute;
  background-color: var(--shape-bg-color);
  border-radius: 50%;
  animation: moveShape 15s infinite alternate;
}

.shape1 {
  width: 20vmin;
  height: 20vmin;
  top: 5%;
  left: 10%;
  animation-delay: 1s;
}

.shape2 {
  width: 15vmin;
  height: 15vmin;
  top: 80%;
  left: 70%;
  animation-delay: 5s;
}

.shape3 {
  width: 25vmin;
  height: 25vmin;
  top: 30%;
  left: 20%;
  animation-delay: 1s;
}

.shape4 {
width: 15vmin;
height: 15vmin;
top: 90%;
left: 50%;
animation-delay: 2s;
}

@keyframes moveShape {
from {
transform: translate(-50%, -50%) scale(0);
opacity: 0.8;
}
to {
transform: translate(-50%, -50%) scale(2);
opacity: 0;
}
}


.quote-display {
  position: relative;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.quote {
  position: absolute;
  width: 180%;
  font-size: 18px;
  animation: floatQuote 5s ease-out forwards;
  pointer-events: none;
  user-select: none;
  z-index: 10;
}

/* 名人名言动画 */
@keyframes floatQuote {
  0% {
    transform: translateY(0);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100%);
    opacity: 0;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>