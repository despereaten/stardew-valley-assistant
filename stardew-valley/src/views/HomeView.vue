<template>
  <nav>
        <ul>
            <img src="../assets/assistant/Main_Logo_ZH.png" alt="标识" class="logo-icon">
        </ul>
    </nav>
  <div id="loading" class="loading-container" style="display: none;">
      <img src="../assets/assistant/Dog.gif" alt="Loading" class="loading-rabbit">
      <p class="loading-text">正在回复中...</p>
    </div>
  <div>
    <div class="button-container">
      <img src="../assets/assistant/clothes.png" class="clothes-icon "></img>
      <div class="color-button white-button" @click="changeBackground('day')"></div>
      <div class="color-button black-button" @click="changeBackground('night')"></div>
      <div class="color-button blue-button" @click="changeBackground('winter')"></div>
    </div>
    <component :is="currentComponent"></component>
    <div :class="['background', currentBackground]">
      <div class="chat-container">
        <div class="left-column">
          <button class="new-session" @click="startNewSession">新会话</button>
          <div>
            <h3 class="history-chat">历史会话</h3>
            <ul class="session-list">
              <li v-for="session in sessions" :key="session" class="session-item">
                <button @click="selectSession(session)" class="session-button" :title="session">会话 {{ session }}</button>
                <button @click="deleteSession(session)" class="delete-button"></button> <!-- 添加删除按钮 -->
              </li>
            </ul>
          </div>
        </div>
        <div class="right-column">
          <div class="response-box">
            <div v-if="currentSessionId">
              <p v-for="msg in chatMessages" :key="msg.id" style="padding: 1px 2%;"
                :class="{ 'user-message': msg.isUser, 'assistant-message': !msg.isUser }">
                <img v-if="msg.sender === 'User'" class="avatar" src="../assets/assistant/Abigail_Icon.png"
                  alt="User Avatar">
                <img v-else class="avatar" src="../assets/assistant/White_Chicken.png" alt="Assistant Avatar">
                <!-- {{ msg.message }} -->
                <MarkdownRenderer :markdown="msg.message" />
              </p>
            </div>
          </div>

          <div class="input-box">
<<<<<<< HEAD
            <textarea v-model="userInput" placeholder="请输入文字..." @keyup.enter="sendMessage"></textarea>
=======
            <textarea v-model="userInput" placeholder="请输入文字..."></textarea>
>>>>>>> 1e471093d7b17b2303eefb597cca11db924e7e8c
            <button @click="sendMessage">发送</button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

import snow from '../components/snow.vue'
import flower from '../components/flower.vue'
import star from '../components/star.vue'
import { MarkdownIt } from 'vue3-markdown-it'
import MarkdownRenderer from '../components/MarkdownRenderer.vue';

export default {
  components: {
    snow,
    flower,
    star,
    MarkdownIt,
    MarkdownRenderer,
  },
  data() {
    return {
      sessions: [],
      currentSessionId: null,
      userInput: '',
      chatMessages: [],  // 保存所有的聊天消息
      currentBackground: 'background-winter',
      currentComponent: 'snow'
    };
  },
  created() {
    this.loadSessions();
  },
  methods: {
    loadSessions() {
      axios
        .get('http://localhost:5000/get_sessions')
        .then(response => {
          this.sessions = response.data.sessions;
        })
        .catch(error => {
          console.error('Error loading sessions:', error);
        });
    },
    startNewSession() {
      axios
        .post('http://localhost:5000/new_session')
        .then(response => {
          const sessionId = response.data.session_id;
          this.sessions.push(sessionId);
          this.selectSession(sessionId);
          console.log("add dialog:", sessionId);
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
    deleteSession(sessionId) {  // 添加删除会话的方法
      axios
        .delete(`http://localhost:5000/delete_session/${sessionId}`)
        .then(() => {
          this.sessions = this.sessions.filter(session => session !== sessionId);
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
    sendMessage() {
      if (this.userInput.trim() === '') return;

      // 显示等待动画
      document.getElementById('loading').style.display = 'flex';

      axios
        .post('http://localhost:5000/send_message', {
          session_id: this.currentSessionId,
          message: this.userInput
        })
        .then(response => {
          this.chatMessages.push({
            id: Date.now(),
            sender: 'User',
            message: this.userInput
          });
          this.chatMessages.push({
            id: Date.now() + 1,
            sender: 'AI',
            message: response.data.response
          });
          this.userInput = '';

          // 隐藏等待动画
          document.getElementById('loading').style.display = 'none';
        })
        .catch(error => {
          console.error('Error sending message:', error);

          // 隐藏等待动画
          document.getElementById('loading').style.display = 'none';
        });
    },

    changeBackground(type) {
      if (type === 'day') {
        this.currentBackground = 'background-day';
        this.currentComponent = 'flower';
      } else if (type === 'night') {
        this.currentBackground = 'background-night';
        this.currentComponent = 'star';
      } else if (type === 'winter') {
        this.currentBackground = 'background-winter';
        this.currentComponent = 'snow';
      }
    }
  }
};
</script>

<style scoped lang="scss">
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

.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  z-index: 1000;
}

.loading-rabbit {
  width: 100px;
  height: auto;
}

.loading-text{
  color: #8a390a;
  font-weight: bold;
}

.snowflake {
  --size: 0.4vw;
  width: var(--size);
  height: var(--size);
  background-size: 100% 100%;
  position: fixed;
  top: -5vh;
  z-index: 1;
}

@keyframes snowfall {
  100% {
    transform: translate3d(var(--end), 100vh, 0);
  }
}

@for $i from 1 through 100 {
  .snowflake:nth-child(#{$i}) {
    --size: #{random(10) * 0.1}vw;
    --end: #{random(20) - 70}vw;
    left: #{random(150)}vw;
    animation: snowfall #{10 + random(20)}s linear infinite;
    animation-delay: -#{random(10)}s;
  }
}

.chat-container {
  justify-content: center;
  margin-top: 10%;
  display: flex;
  height: 80%;
  width: 65%;
  margin: 5% auto;
  flex-direction: row; //修改为水平排列
  //flex-direction: column;
  align-items: center;
  position: relative;
  padding: 20px;
  border-radius: 20px;
  background-color: #fdbc72b7;
  box-shadow:
      inset #8a390a 0 0 0 2px,
      inset #ba4d0d 0 0 0 5px,
      inset #ffa845 0 0 0 9px,
      inset #cd710f  0 0 0 12px,
      inset #ba4d0d 0 0 0 14px,
      inset #8a390a 0 0 0 16px,
}

.left-column {
  width: 30%;
  padding: 20px;
  height: 81%;
  margin-left: 35px;
  margin-right: 20px;
  border: 2px solid #cccccc00;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.833);
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2); 
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

.new-session{
  width: 94%;
  font-size: 1.02em;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2); 
}

.history-chat{
  padding-top: 6%;
  padding-left: 1%;
  color: #8a390a;
  font-size: 1.2em;
}

.session-list {
  list-style-type: none; 
  padding: 0;

}

.session-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.session-button {
  flex-grow: 1;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.833);
  color: #ba4d0d;
  border-bottom-style:2px solid #ba4d0d;;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 80%; /* 固定按钮最大宽度 */
}

.session-button:hover {
  background-color: rgba(254, 236, 216, 0.833);
}

.session-button::after {
  content: attr(title);
  position: absolute;
  white-space: nowrap;
  overflow: visible;
  max-width: none;
  text-overflow: none;
  visibility: hidden;
}

.delete-button {
  padding: 16px;
  margin-left: 10px;
  background: url('../assets/assistant/delete.png') no-repeat center center;
  
  border:2px solid#f8965eab;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button:hover {
  transform: scale(1.1); 
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
  font-weight:bold;
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

button {
  padding: 10px 20px;
  background-color: #ba4d0d;
  border-color: #e9f5ff00;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-weight:bold;
  text-shadow: 2px 2px 2px #5c190b3d;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2);  
}

button:hover {
  background-color: #99410f;
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

.button-container {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 10px;
}

.clothes-icon{
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

.markdown-it {
  font-family: Arial, sans-serif;
}
.markdown-it ul {
  list-style-type: disc;
  padding-left: 20px;
}
</style>
