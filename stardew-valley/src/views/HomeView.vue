<template>
  <div>
    <div class="button-container">
      <div class="color-button white-button" @click="changeBackground('day')"></div>
      <div class="color-button black-button" @click="changeBackground('night')"></div>
      <div class="color-button blue-button" @click="changeBackground('winter')"></div>
    </div>
    <component :is="currentComponent"></component>
    <div :class="['background', currentBackground]">
      <div class="chat-container">
        <div class="left-column">
          <button @click="startNewSession">开始新会话</button>
          <div>
            <h3>选择会话</h3>
            <ul class="session-list">
              <li v-for="session in sessions" :key="session" class="session-item">
                <button @click="selectSession(session)" class="session-button" :title="session">会话 {{ session }}</button>
                <button @click="deleteSession(session)" class="delete-button">删除</button> <!-- 添加删除按钮 -->
              </li>
            </ul>
          </div>
        </div>
        <div class="right-column">
          <div class="response-box">
            <div v-if="currentSessionId">
              <p v-for="msg in chatMessages" :key="msg.id"
                :class="{ 'user-message': msg.isUser, 'assistant-message': !msg.isUser }">
                <img v-if="msg.sender === 'User'" class="avatar" src="../assets/assistant/Abigail_Icon.png"
                  alt="User Avatar">
                <img v-else class="avatar" src="../assets/assistant/White_Chicken.png" alt="Assistant Avatar">
                {{ msg.message }}
              </p>
            </div>
          </div>

          <div class="input-box">
            <textarea v-model="userInput" placeholder="Type your message here..."></textarea>
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

export default {
  components: {
    snow,
    flower,
    star
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
        })
        .catch(error => {
          console.error('Error sending message:', error);
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

@for $i from 2 through 100 {
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
  width: 60%;
  margin: 5% auto;
  flex-direction: row; //修改为水平排列
  //flex-direction: column;
  align-items: center;
  position: relative;
  padding: 20px;
  border: 2px solid #3894d5af;
  border-radius: 5px;
  background-color: #d3ebffc7;

}

.left-column {
  width: 30%;
  padding: 20px;
  // border-right: 1px solid #ddd;
}

.session-list {
  list-style-type: none; //移除了圆点
  padding: 0;
}

.session-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.session-button {
  flex-grow: 1;
  padding: 10px;
  background-color: #026ee3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 150px; /* 固定按钮最大宽度 */
}

.session-button:hover {
  background-color: #0056b3;
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
  padding: 10px;
  margin-left: 10px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #e60000;
}



.right-column {
  width: 70%;
  display: flex;
  flex-direction: column;
  row-gap: 20px;
  justify-content: space-between;
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
  width: 80%;
  height: 300%;
  border: 2px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  margin-top: 2%;
  overflow-y: auto;
  background-color: rgba(255, 255, 255, 0.9);
  overflow-y: auto;
}

.input-box {
  display: flex;
  align-items: center;
  width: 80%;
  height: 100%;
}

textarea {
  height: 10%;
  flex-grow: 1;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
  min-width: 200px;
}

button {
  padding: 10px 20px;
  background-color: #026ee3;
  border-color: #e9f5ff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.user-message {

  text-align: right;
  border: 1px solid #0062ff;
  border-radius: 4px;
  padding: 5px;
  margin: 10px 10px;
  background-color: #e9f5ff;
  display: flex;
  align-items: center;
}

.assistant-message {
  text-align: left;
  border: 1px solid #ccc;
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
</style>
