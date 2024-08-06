<template>
  <div>
    <nav>
      <ul>
        <img src="../assets/assistant/Main_Logo_ZH.png" alt="标识" class="logo-icon">
      </ul>
    </nav>

    <div class="button-container">
      <img src="../assets/assistant/clothes.png" class="clothes-icon"></img>
      <div class="color-button white-button" @click="changeBackground('day')"></div>
      <div class="color-button black-button" @click="changeBackground('night')"></div>
      <div class="color-button blue-button" @click="changeBackground('winter')"></div>
      <div class="user-profile-container" @mouseover="showProfile = true" @mouseleave="hideProfile">
        <img src="../assets/role/The_Player_Icon.png" class="user-image" />
        <div v-if="showProfile" class="profile-details">
          <img src="../assets/role/The_Player_Icon.png" class="profile-image" />
          <p class="user-info">用户姓名: {{ username }}</p>
          <button @click="logout" class="action-button">退出登录</button>
          <button @click="switchAccount" class="action-button">切换账号</button>
        </div>
      </div>
    </div>

    <component :is="currentComponent"></component>
    <div :class="['background', currentBackground]">
      <div v-if="!isChatting" class="chat-container">
        <div class="top-boxes">
          <div class="top-box box-one" @click="goto('/Assistant')">
            <img src="../assets/assistant/robot_icon.png" class="icon" />
            <p class="suggestion-text">智能助手</p>
          </div>
          <div class="top-box box-two" @click="goto('/GuessLike')">
            <img src="../assets/guesslike/TV.png" class="icon" />
            <p class="suggestion-text">猜你喜欢</p>
          </div>
          <div class="top-box box-three">
            <img src="../assets/role/Speech_bubble.png" class="icon" />
            <p class="suggestion-text">角色对话</p>
          </div>
          <div class="top-box box-four" @click="goto('/RoleMatching')">
            <img src="../assets/guesslike/Love_Icon.png" class="icon" />
            <p class="suggestion-text">伴侣匹配</p>
          </div>
        </div>
        <div class="card">
          <img :src="currentCard.image2" class="card-image" alt="Card Image">
          <div class="card-content">
            <h2 class="card-title">{{ currentCard.name }}</h2>
            <ul>
              <li class="card-description">性别: {{ currentCard.gender }}</li>
              <li class="card-description">生日: {{ currentCard.birthday }}</li>
              <li class="card-description">{{ currentCard.description }}</li>
            </ul>
          </div>
          <button @click="startChatting" class="decide-button">确认选择该角色对话</button>
        </div>
        <div class="image-grid">
          <div v-for="character in characters" :key="character.name" class="grid-item" @click="updateCard(character)">
            <img :src="character.image" class="grid-image" :alt="character.name">
            <p>{{ character.name }}</p>
          </div>
        </div>
        <div class="test">
          <p>犹豫不决吗？点击此处测试，匹配最适合你的角色！<a href='/RoleMatching'>伴侣匹配</a></p>
        </div>
      </div>

      <div v-if="isChatting" class="chat-container">
        <div class="top-boxes">
          <div class="top-box box-one" @click="goto('/Assistant')">
            <img src="../assets/assistant/robot_icon.png" class="icon" />
            <p class="suggestion-text">智能助手</p>
          </div>
          <div class="top-box box-two" @click="goto('/GuessLike')">
            <img src="../assets/guesslike/TV.png" class="icon" />
            <p class="suggestion-text">猜你喜欢</p>
          </div>
          <div class="top-box box-three">
            <img src="../assets/role/Speech_bubble.png" class="icon" />
            <p class="suggestion-text">角色对话</p>
          </div>
          <div class="top-box box-four" @click="goto('/RoleMatching')">
            <img src="../assets/guesslike/Love_Icon.png" class="icon" />
            <p class="suggestion-text">伴侣匹配</p>
          </div>
        </div>
        <button @click="cancelChatting(currentSessionId)" class="cancel-button">取消对话</button>
        <div class="right-column">
          <div class="response-box" ref="responseBox">
            <div v-if="currentSessionId">
              <p v-for="msg in chatMessages" :key="msg.id" style="padding: 1px 2%;"
                :class="{ 'user-message': msg.isUser, 'assistant-message': !msg.isUser }">
                <img v-if="msg.sender === 'user'" class="avatar" src="../assets/role/The_Player_Icon.png"
                  alt="User Avatar">
                <img v-else class="avatar" :src="getIconForCurrentCard()" alt="Assistant Avatar">
                <span v-if="msg.sender !== 'user' && msg.message === ''" class="loading-dots">
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </span>
                <MarkdownRenderer :markdown="msg.message" />
                <img v-if="msg.sender !== 'user'" src="../assets/assistant/copy.png" class="copy-icon"
                  @click="copyToClipboard(msg.message)" alt="Copy Icon">
              </p>
            </div>
          </div>

          <div class="input-box">
            <textarea v-model="userInput" placeholder="请输入你的疑问..." @keydown.enter="sendChatMessage"></textarea>
            <button v-if="!isStreaming" @click="sendChatMessage">发送</button>
            <button v-else @click="stopStreaming">暂停</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alex_Icon from '../assets/role/Alex_Icon.png';
import Abigail_Icon from '../assets/role/Abigail_Icon.png';
import Elliott_Icon from '../assets/role/Elliott_Icon.png';
import Emily_Icon from '../assets/role/Emily_Icon.png';
import Haley_Icon from '../assets/role/Haley_Icon.png';
import Harvey_Icon from '../assets/role/Harvey_Icon.png';
import Leah_Icon from '../assets/role/Leah_Icon.png';
import Maru_Icon from '../assets/role/Maru_Icon.png';
import Penny_Icon from '../assets/role/Penny_Icon.png';
import Sam_Icon from '../assets/role/Sam_Icon.png';
import Sebastian_Icon from '../assets/role/Sebastian_Icon.png';
import Shane_Icon from '../assets/role/Shane_Icon.png';
import Alex from '../assets/role/Alex.png';
import Abigail from '../assets/role/Abigail.png';
import Elliott from '../assets/role/Elliott.png';
import Emily from '../assets/role/Emily.png';
import Haley from '../assets/role/Haley.png';
import Harvey from '../assets/role/Harvey.png';
import Leah from '../assets/role/Leah.png';
import Maru from '../assets/role/Maru.png';
import Penny from '../assets/role/Penny.png';
import Sam from '../assets/role/Sam.png';
import Sebastian from '../assets/role/Sebastian.png';
import Shane from '../assets/role/Shane.png';
import snow from '../components/snow.vue';
import flower from '../components/flower.vue';
import star from '../components/star.vue';
import MarkdownRenderer from '../components/MarkdownRenderer.vue';
import { MarkdownIt } from 'vue3-markdown-it'

axios.defaults.baseURL = 'http://localhost:5000';

axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default {
  components: {
    snow,
    flower,
    star,
    MarkdownRenderer,
    MarkdownIt,
  },
  data() {
    return {
      //wyx:
      //sessions: [],//只包含session_id和summary信息
      currentSessionId: null,
      userInput: '',
      chatMessages: [],  // 保存所有的聊天消息
      response: '',
      isStreaming: false,
      isStopped: false,

      showProfile: false,
      hideProfileTimer: null,
      username: localStorage.getItem('username'),
      currentBackground: 'background-winter',
      currentComponent: 'snow',
      controller: new AbortController(),
      currentCard: {
        image2: Alex,
        name: 'Alex',
        gender: '男',
        birthday: '春 13',
        description: '"你知道吗？我在上高中的时候，可是全明星四分卫哦。真的。看到我夹克上这颗小星星了吗？这就是证明"'
      },
      characters: [
        { name: 'Alex', image: Alex_Icon, image2: Alex, gender: '男', birthday: '春 13', description: '"你知道吗？我在上高中的时候，可是全明星四分卫哦。真的。看到我夹克上这颗小星星了吗？这就是证明"' },
        { name: 'Elliott', image: Elliott_Icon, image2: Elliott, gender: '男', birthday: '冬 5', description: '"纸与笔那美妙的摩擦声可是治愈我灵魂的音乐啊。因此我以这片海滩为家，这样我就可以静静地完成我的工作了。"' },
        { name: 'Harvey', image: Harvey_Icon, image2: Harvey, gender: '男', birthday: '冬 14', description: '"很高兴认识你。我是哈维，本地医生。我为鹈鹕镇的居民提供常规的体检和医疗服务。这是个很有意义的工作。希望有天你也会觉得自己的工作很有意义。"' },
        { name: 'Sam', image: Sam_Icon, image2: Sam, gender: '男', birthday: '夏 17', description: '"你看了昨晚的比赛吗？等等，你买了电视机吗……？"' },
        { name: 'Sebastian', image: Sebastian_Icon, image2: Sebastian, gender: '男', birthday: '冬 10', description: '"我正在为我的乐队创作新曲，但是我完全没有灵感……嘿……你觉得我的新歌该是什么主题的？随便吧。反正都是难听死的。"' },
        { name: 'Shane', image: Shane_Icon, image2: Shane, gender: '男', birthday: '春 20', description: '"我在玛妮那儿以一个很不错的价钱租到了房子。房间有点小但是我并不介意。如果我能重新安排我的生活，我可能会开一家养鸡场，当然只有自由放养的蛋 。"' },
        { name: 'Abigail', image: Abigail_Icon, image2: Abigail, gender: '女', birthday: '秋 13', description: '"今天小鸟们叫得好欢啊。它们的头脑简单，根本就不担心未来。像它们那样也挺好的，对不对？"' },
        { name: 'Emily', image: Emily_Icon, image2: Emily, gender: '女', birthday: '春 27', description: '"在格斯那工作只是为了生计…我真正喜欢的事情是裁缝。这些是我按照图样做出来的衣服。"' },
        { name: 'Haley', image: Haley_Icon, image2: Haley, gender: '女', birthday: '春 14', description: '"我今天花了3小时练习签名。我想这太蠢了是吧？"' },
        { name: 'Leah', image: Leah_Icon, image2: Leah, gender: '女', birthday: '冬 23', description: '"和树当朋友比较简单。它们没什么话讲。"' },
        { name: 'Maru', image: Maru_Icon, image2: Maru, gender: '女', birthday: '夏 10', description: '"难道只有人类的思维才配拥有自我意识吗？虽然机器人的大脑构造与我们截然不同，那也不代表我们就应该这样不尊重、不认可他们啊。"' },
        { name: 'Penny', image: Penny_Icon, image2: Penny, gender: '女', birthday: '秋 2', description: '"虽然镇里没有学校，但我一直都在努力，想要好好教导文森特与贾斯。每个孩子都应该有成功的机会才对。"' }
      ],
      isChatting: false,
      currentSessionId: null,
      chatMessages: [],
      userInput: '',
      isStreaming: false,
      textSegments: [],
      character_id: ''
    };
  },
  methods: {
    changeBackground(type) {
      switch (type) {
        case 'day':
          this.currentBackground = 'background-day';
          this.currentComponent = 'flower';
          break;
        case 'night':
          this.currentBackground = 'background-night';
          this.currentComponent = 'star';
          break;
        case 'winter':
          this.currentBackground = 'background-winter';
          this.currentComponent = 'snow';
          break;
      }
    },
    getIconForCurrentCard() {
      switch (this.character_id) {
        case 'Alex':
          return Alex_Icon;
        case 'Abigail':
          return Abigail_Icon;
        case 'Elliott':
          return Elliott_Icon;
        case 'Emily':
          return Emily_Icon;
        case 'Haley':
          return Haley_Icon;
        case 'Harvey':
          return Harvey_Icon;
        case 'Leah':
          return Leah_Icon;
        case 'Sam':
          return Sam_Icon;
        case 'Sebastian':
          return Sebastian_Icon;
        case 'Shane':
          return Shane_Icon;
        case 'Penny':
          return Penny_Icon;
        case 'Maru':
          return Maru_Icon;
      }
    },
    updateCard(character) {
      this.currentCard = character;
    },
    //wyx:创建新对话
    startChatting() {
      this.isChatting = true;
      this.character_id = this.currentCard.name;
      localStorage.setItem('character_id', this.character_id);
      console.log('this.character_id:' + this.character_id)
      localStorage.setItem('isChatting', 'true');

      axios
        .post('http://localhost:5000/new_chat_session', {
          post_character_id: this.currentCard.name
        })
        .then(response => {
          const session = response.data;//新的 session只会传入session_id的信息,前端session只包含这信息
          //this.sessions.push(session);
          this.selectSession(session.session_id);
          // 保存当前会话ID到 localStorage
          localStorage.setItem('currentSessionId', session.session_id);
          console.log("add dialog:", session.session_id);
        })
        .catch(error => {
          console.error('Error creating new session:', error);
        });
    },
    selectSession(sessionId) {
      this.currentSessionId = sessionId;
      this.loadHistory(sessionId);
      console.log("select dialog:", sessionId);
    },
    loadHistory(sessionId) {
      axios
        .get(`http://localhost:5000/get_history/${sessionId}`)
        .then(response => {
          this.chatMessages = response.data.history;
          console.log("load dialog:", sessionId);
        })
        .catch(error => {
          console.error('Error loading history:', error);
        });
    },
    scrollToBottom() {
      const responseBox = this.$refs.responseBox;
      responseBox.scrollTop = responseBox.scrollHeight;
    },
    //wyx:发送对话
    async sendChatMessage() {
      if (this.userInput.trim() === '') return;
      // 显示等待动画
      //document.getElementById('loading').style.display = 'flex';
      const messageToSend = this.userInput;
      console.log("messageToSend", messageToSend);
      this.controller = new AbortController();
      this.response = '';
      this.isStopped = false;
      this.isStreaming = true;

      this.userInput = '';

      this.chatMessages.push({
        id: Date.now(),
        sender: 'user',
        message: messageToSend
      });

      this.$nextTick(() => {
        this.scrollToBottom();
      });

      // 初始化 AI 消息
      const aiMessageId = Date.now() + 1;
      this.chatMessages.push({
        id: aiMessageId,
        sender: 'ai',
        message: ''
      });

      this.isWaitingForResponse = true;

      this.$nextTick(() => {
        this.scrollToBottom();
      });

      const response = await fetch('http://localhost:5000/send_chat_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // 添加token
        },
        body: JSON.stringify({ session_id: this.currentSessionId, message: messageToSend }),//发送到服务器的数据
        signal: this.controller.signal
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      this.userInput = '';
      // 隐藏等待动画
      //document.getElementById('loading').style.display = 'none';

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      const aiMessageIndex = this.chatMessages.findIndex(msg => msg.id === aiMessageId);

      //以下这段不正常(只运行了一次)：
      while (true) {
        //if (this.isStopped) break;
        const { done, value } = await reader.read();
        const text = decoder.decode(value);
        console.log("value:" + value)
        this.response += text
        if (done) { break; }

        // 更新 AI 消息内容
        if (aiMessageIndex !== -1) {
          this.chatMessages[aiMessageIndex].message = this.response;
          console.log("response" + this.response)
        }
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
      this.isWaitingForResponse = false;
      this.isStreaming = false;
      // 在消息完全接收后或流式输出停止后保存答案
      if (!this.isStopped) {
        this.saveAnswer(this.response);
        console.log("保存答案")
        this.isWaitingForResponse = false;
      }
    },

    async saveAnswer(answer) {
      try {
        await axios.post('http://localhost:5000/save_answer', {
          session_id: this.currentSessionId,
          answer: answer
        });
      } catch (error) {
        console.error('Error saving answer:', error);
      }
    },
    //wyx:
    cancelChatting(sessionId) {
      this.isChatting = false;
      localStorage.removeItem('isChatting');

      axios
        .delete(`http://localhost:5000/delete_session/${sessionId}`)
        .then(() => {
          if (this.currentSessionId === sessionId) {
            this.currentSessionId = null;
            this.chatMessages = [];
          }
          console.log("delete dialog:", sessionId);
        })
        .catch(error => {
          console.error('Error deleting session:', error);
        });
    },
    goto(path) {
      this.$router.push(path);
    },
    showProfile() {
      clearTimeout(this.hideProfileTimer);
      this.showProfile = true;
    },
    hideProfile() {
      this.hideProfileTimer = setTimeout(() => {
        this.showProfile = false;
      }, 1000);
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/Login');
    },
    switchAccount() {
      localStorage.removeItem('token');
      this.$router.push('/Login');
    },
    async stopStreaming() {
      if (this.controller) {
        this.controller.abort();
        this.controller = new AbortController();
        this.isStreaming = false;
      }
    },
    copyToClipboard(message) {
      navigator.clipboard.writeText(message).then(() => {
        console.log('Message copied to clipboard');
      }, (err) => {
        console.error('Could not copy text: ', err);
      });
    }
  },
  mounted() {
    if (!localStorage.getItem('token')) {
      this.$router.push('/Login');
    }

    // 检查是否处于聊天状态
    if (localStorage.getItem('isChatting')) {
      this.isChatting = true;
    }
    // 获取当前会话ID
    this.currentSessionId = localStorage.getItem('currentSessionId');
    this.character_id = localStorage.getItem('character_id') || '';

    // 如果有当前会话ID，则加载历史记录
    if (this.currentSessionId) {
      this.loadHistory(this.currentSessionId);
    }
  }
};
</script>


<style scoped lang="scss">
//呼吸灯效果
.loading-dots {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  padding-left: 5px;
  /* 调整与头像的距离 */
}

.dot {
  width: 8px;
  height: 8px;
  margin: 0 2px;
  background-color: #333;
  border-radius: 50%;
  animation: blink 1.4s infinite both;
}

.dot:nth-child(1) {
  animation-delay: 0s;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {

  0%,
  80%,
  100% {
    opacity: 0;
  }

  40% {
    opacity: 1;
  }
}

.user-profile-container {
  width: 25%;
  cursor: pointer;
}

.user-image {
  width: 100%;
  height: 100%;
}

.profile-details {
  position: absolute;
  top: 60px;
  right: 0;
  width: 200px;
  background-color: #facb95;
  border: 1px solid #8b4513;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-image {
  width: 80px;
  height: 80px;
  margin-bottom: 10px;
}

.user-info {
  margin: 5px 0;
  color: #8b4513;
}

.action-button {
  margin: 5px 0;
  padding: 5px 10px;
  background-color: #8b4513;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  text-align: center;
}

nav img {
  position: absolute;
  height: 25px;
  margin-top: 15px;
  margin-right: 15px;
  vertical-align: middle;
}

.logo-icon {
  position: absolute;
  top: 0px;
  left: 15px;
  width: 180px;
  height: auto;
  transform-origin: top left;
}

.chat-container {
  justify-content: center;
  margin-top: 10%;
  display: flex;
  height: 80%;
  width: 65%;
  margin: 5% auto;
  //修改为水平排列
  flex-direction: column;
  align-items: center;
  position: relative;
  padding: 20px;
  border-radius: 20px;
  background-color: #fcc587f0;
  box-shadow:
    inset #8a390a 0 0 0 2px,
    inset #ba4d0d 0 0 0 5px,
    inset #ffa845 0 0 0 9px,
    inset #cd710f 0 0 0 12px,
    inset #ba4d0d 0 0 0 14px,
    inset #8a390a 0 0 0 16px;
}

.top-boxes {
  display: flex;
  position: absolute;
  justify-content: space-between;
  bottom: 100%;
  /* 调整这个控制与 chat-container 顶部的距离 */
  left: 0;
  right: 0;
  padding: 0 20%;
  gap: 10px;
  /* 添加方框之间的间距 */
}

.top-box {
  width: 30%;
  height: 35px;
  background-color: #fcc587fe;
  box-shadow:
    -1px 0px 0 0 #8a390a,
    -2px 0px 0 0 #cd710f,
    /* 左边阴影 */
    -3px 0px 0 0 #ffa845,
    -4px 0px 0 0 #cd710f,
    -5px 0px 0 0 #8a390a,

    1px 0px 0 0 #8a390a,
    /* 右边阴影 */
    2px 0px 0 0 #cd710f,
    3px 0px 0 0 #ffa845,
    4px 0px 0 0 #cd710f,
    5px 0px 0 0 #8a390a,


    inset 0px 1px 0 0 #8a390a,
    /* 上边阴影 */
    inset 0px 2px 0 0 #cd710f,
    inset 0px 3px 0 0 #ffa845,
    inset 0px 4px 0 0 #cd710f,
    inset 0px 5px 0 0 #8a390a;
  cursor: pointer;
  transform: translateY(16px);


  display: flex;
  align-items: center;
  justify-content: center;
}

.box-three {
  cursor: auto;
  height: 51px;
}

.icon {
  width: 25px;
  height: 25px;
}

.suggestion-text {
  font-size: 16px;
  color: #8a390a;
  font-weight: bold;
  text-shadow: 2px 2px 2px #5c190b3d;
}

.card {
  margin: 3%;
  position: relative;
  height: 55%;
  display: flex;
  flex-direction: row;
  width: 90%;
  background-color: #f2dec9b7;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
  /* 确保内容不会溢出容器 */
}

.card-image {
  margin: 3%;
  position: relative;
  border-radius: 10px 10px 0 0;
}

.card-content {
  position: relative;
  padding: 10px;

  height: 25%;
  font-size: 1.1em;
  color: #9c3f0a;
  font-weight: bold;
  /* 使内容部分占据剩余空间 */
}

.card-title {
  font-family: Arial, sans-serif;
  margin: 1%;
  padding-bottom: 5px;
  font-size: 1.5em;
  font-weight: bold;
  color: #9c3f0a;
  text-shadow: 2px 2px 2px #5c190b3d;
}

.card-description-list {
  list-style-type: disc;
  padding-left: 20px;
}

.card-description {
  font-size: 1.2em;
  color: #9c3f0a;
  font-weight: bold;
  text-shadow: 2px 2px 2px #5c190b3d;
}

.image-grid {
  height: 40%;
  display: grid;
  margin-top: 2%;
  grid-template-columns: repeat(6, 1fr);
  /* 每行6列，宽度自动分配 */
  gap: 0px;
  width: 90%;
}

.grid-image {
  padding: 7%;
  width: 48%;
  height: auto;
  border-radius: 10%;
  //border: 2px solid #9c400a86;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2);
  background-color: #f2dec9b7;
  box-shadow:
    inset #8a390a 0 0 0 1px,
    inset #ba4d0d 0 0 0 2px,
    inset #ffa845 0 0 0 3px,
    inset #cd710f 0 0 0 4px,
    inset #ba4d0d 0 0 0 5px,
    inset #8a390a 0 0 0 6px;
}

.grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.2);
  }
}

.grid-item p {
  margin-top: 5px;
  font-size: 1.2em;
  color: #9c3f0a;
  font-weight: bold;
  text-shadow: 2px 2px 2px #5c190b3d;
}

.test {
  margin: 0.1%;
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.background-winter {
  background: url('../assets/assistant/bkgd-winter.png') no-repeat center center;
  background-size: cover;
}

.background-day {
  background: url('../assets/assistant/bkgd-day.jpg') no-repeat center center;
  background-size: cover;
}

.background-night {
  background: url('../assets/assistant/bkgd-night.jpg') no-repeat center center;
  background-size: cover;
}

.button-container {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 10px;
}

.clothes-icon {
  width: 25px;
  height: 25px;
}

.color-button {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #ccc;
}

.white-button {
  background-color: rgb(254, 250, 227);
}

.black-button {
  background-color: rgb(25, 56, 147);
}

.blue-button {
  background-color: rgb(145, 198, 244);
}

.decide-button {
  position: absolute;
  right: 3%;
  bottom: 8%;
  padding: 10px 20px;
  font-size: 0.8em;
  color: white;
  background-color: #8b4513;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 2px 2px 5px #8b4513;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.2);
  }
}

.cancel-button {
  position: absolute;
  left: 8%;
  top: 4%;
  padding: 10px 20px;
  font-size: 0.8em;
  color: white;
  background-color: #8b4513;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 2px 2px 5px #8b4513;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.2);
  }
}

.right-column {
  width: 90%;
  height: 90%;
  //border:  5px solid #e20e0e;
  display: flex;
  flex-direction: column;
  row-gap: 10px;
  justify-content: space-between;
}

.response-box {
  justify-content: center;
  width: 90%;
  //border: 2px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  margin-top: 2%;
  background-color: rgba(255, 255, 255, 0.9);
  overflow-y: auto;
  height: 100%;
  //font-family:"";
  font-size: 1.2em;
  color: #9c3f0a;
  font-weight: bold;
  text-shadow: 2px 2px 2px #5c190b3d;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2);
  scrollbar-color: #8a390a rgba(255, 255, 255, 0.9);
}


.input-box {

  display: flex;
  align-items: center;
  width: 94%;
  height: 12%;
}

textarea {
  height: 30%;
  flex-grow: 1;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
  min-width: 200px;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2);
}

.user-message {
  text-align: right;
  border: 1px solid #99410f;
  border-radius: 4px;
  padding: 5px;
  margin: 10px 10px;
  background-color: #fb955ae0;
  display: flex;
  align-items: center;

}

.assistant-message {
  position: relative;
  text-align: left;
  border: 1px solid #99410f;
  border-radius: 4px;
  padding: 5px;
  margin: 5px 0;
  background-color: #f1f1f1;
  display: flex;
  align-items: center;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.copy-icon {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 15px;
  height: 15px;
  cursor: pointer;
}

button {
  padding: 10px 20px;
  background-color: #ba4d0d;
  border-color: #e9f5ff00;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  text-shadow: 2px 2px 2px #5c190b3d;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2);
}

button:hover {
  background-color: #99410f;
}
</style>