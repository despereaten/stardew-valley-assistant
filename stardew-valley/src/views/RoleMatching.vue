<template>
  <nav>
    <ul>
      <img src="../assets/assistant/Main_Logo_ZH.png" alt="标识" class="logo-icon">
    </ul>
  </nav>

  <div>
    <div class="button-container">
      <img src="../assets/assistant/clothes.png" class="clothes-icon" />
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

      <div class="chat-container">

        <div class="top-boxes">
          <div class="top-box box-one" @click="goto('/Assistant')">
            <img src="../assets/assistant/robot_icon.png" class="icon" />
            <p class="suggestion-text">智能助手</p>
          </div>
          <div class="top-box box-two" @click="goto('/GuessLike')">
            <img src="../assets/guesslike/TV.png" class="icon" />
            <p class="suggestion-text">猜你喜欢</p>
          </div>
          <div class="top-box box-three" @click="goto('/RoleShow')">
            <img src="../assets/role/Speech_bubble.png" class="icon" />
            <p class="suggestion-text">角色对话</p>
          </div>
          <div class="top-box box-four">
            <img src="../assets/guesslike/Love_Icon.png" class="icon" />
            <p class="suggestion-text">伴侣匹配</p>
          </div>
        </div>

        <div class="right-column">
          <div class="response-box" ref="responseBox">
            <div>
              <p v-for="msg in chatMessages" :key="msg.id" style="padding: 1px 2%;"
                :class="{ 'user-message': msg.isUser, 'assistant-message': !msg.isUser }">
                <img v-if="msg.sender === 'User'" class="avatar" src="../assets/role/The_Player_Icon.png"
                  alt="User Avatar">
                <img v-else class="avatar" src="../assets/assistant/White_Chicken.png" alt="Assistant Avatar">
                <span v-if="msg.sender !== 'User' && msg.message === ''" class="loading-dots">
                  <span class="dot"></span>
                  <span class="dot"></span>
                  <span class="dot"></span>
                </span>
                <MarkdownRenderer :markdown="msg.message" />
                <img v-if="msg.sender !== 'User'" src="../assets/assistant/copy.png" class="copy-icon"
                  @click="copyToClipboard(msg.message)" alt="Copy Icon">
              </p>
            </div>

          </div>

          <div class="input-box">
            <textarea v-model="userInput" placeholder="请输入你的答案..." @keydown.enter="sendMessage"
              :disabled="inputDisabled"></textarea>
            <button v-if="!isStreaming" @click="sendMessage">发送</button>
            <button v-else @click="stopStreaming">暂停</button>
            <button v-if="showCompleteButton" @click="restartTest">测试已完成，点击重新开始</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import snow from '../components/snow.vue';
import flower from '../components/flower.vue';
import star from '../components/star.vue';
import MarkdownRenderer from '../components/MarkdownRenderer.vue';

export default {
  components: {
    snow,
    flower,
    star,
    MarkdownRenderer,
  },
  data() {
    return {
      links: [],
      showProfile: false,
      username: localStorage.getItem('username'),
      currentBackground: 'background-winter',
      currentComponent: 'snow',
      currentSessionId: Date.now(),
      chatMessages: [],
      userInput: '',
      isStreaming: false,
      isStopped: false,
      response: '',
      controller: null,
      isWaitingForResponse: false, // 控制等待动画的显示
      showCompleteButton: false,//完成重新开始按钮
      inputDisabled: false,//控制输入框是否允许输入
      questions: [
        "你的性取向是？",
        "你有什么觉得最能代表自己的兴趣爱好吗？",
        "不考虑收入，你最想做哪种职业？",
        "在星露谷中，你更倾向于做什么？去未知的地方探险还是平静地闲逛？",
        "更害怕别人如何称呼你？无知、胆小、懒惰、平庸抑或其他？",
        "你在选择交友对象时最主要考虑的因素是？外表形象、脾气性格、文化水平、工作能力、兴趣爱好……？",
        "假如你在joja公司工作，你的工作压力很大，每天都过得很辛苦，但有稳定的收入来源，在这种情况下，你是会选择辞职还是继续工作？",
        "你更倾向于独处还是与朋友一起度过时间？",
        "你如何看待艺术和创造力在你的生活中的作用？",
        "你是否喜欢参与户外活动或自然探险？",
        "你最喜欢的季节是什么？",
      ]
    };
  },
  methods: {
    sendInitialQuestion() {
      const initialQuestion = "欢迎来到伴侣匹配模块！🥰🥰我们将会向您进行一系列的问题的提问，请认真回答以下问题，以便我们得到更准确的分析与结果，现在！🙌🙌提问开始！\n\n" + this.questions[0];
      console.log(this.questions[0])
      this.chatMessages.push({
        id: Date.now(),
        sender: 'AI',
        message: initialQuestion
      });
      console.log(initialQuestion)
      // 向后端发送请求，通知重新开始
      fetch('http://localhost:5000/role_match_send_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ message: '', restart: true })
      });
    },
    async sendMessage() {
      if (this.userInput.trim() === '') return;
      const messageToSend = this.userInput;
      console.log("messageToSend", messageToSend);
      this.controller = new AbortController();
      this.response = '';
      this.isStopped = false;
      this.isStreaming = true;
      this.userInput = '';


      // 添加用户消息
      const userMessageId = Date.now();
      this.chatMessages.push({
        id: userMessageId,
        sender: 'User',
        message: messageToSend
      });

      // 初始化 AI 消息
      const aiMessageId = userMessageId + 1;
      this.chatMessages.push({
        id: aiMessageId,
        sender: 'AI',
        message: ''
      });

      this.isWaitingForResponse = true; // 显示等待动画

      this.$nextTick(() => {
        this.scrollToBottom();
      });

      try {
        const response = await fetch('http://localhost:5000/role_match_send_message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({ message: messageToSend }),
          signal: this.controller.signal
        });
        console.log(response)
        const reader = response.body.getReader();
        const aiMessageIndex = this.chatMessages.findIndex(msg => msg.id === aiMessageId);
        while (true) {
          if (this.isStopped) break;
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = new TextDecoder().decode(value);
          this.response += chunk;

          // 检查是否接收到完成标志
          if (chunk.includes('__COMPLETE__')) {
            this.showCompleteButton = true; // 显示完成按钮
            this.inputDisabled = true; // 禁用输入框
            break;
          }

          // 更新 AI 消息内容
          if (aiMessageIndex !== -1) {
            console.log(this.response)
            this.chatMessages[aiMessageIndex].message = this.response;
          }
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        }

        this.isWaitingForResponse = false; // 隐藏等待动画
        this.isStreaming = false;
        // 在消息完全接收后或流式输出停止后保存答案
        if (!this.isStopped) {
          this.saveAnswer(this.response);
        }
        this.userInput = '';
      } catch (error) {
        console.error('Error:', error);
        this.isWaitingForResponse = false; // 隐藏等待动画
      }
    },
    restartTest() {
      this.chatMessages = [];
      this.response = '';
      this.isStopped = true;
      this.isStreaming = false;
      this.showCompleteButton = false;
      this.inputDisabled = false; // 重新启用输入框
      this.isWaitingForResponse = false; // 隐藏等待动画
      this.sendInitialQuestion(); // 重新开始测试
    },
    scrollToBottom() {
      const responseBox = this.$refs.responseBox;
      responseBox.scrollTop = responseBox.scrollHeight;
    },
    saveAnswer(answer) {
      console.log('保存回答:', answer);
    },
    goto(route) {
      this.$router.push(route);
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
    },
    hideProfile() {
      setTimeout(() => {
        this.showProfile = false;
      }, 1000);
    },
    logout() {
      localStorage.removeItem('username');
      localStorage.removeItem('token');
      window.location.href = '/';
    },
    switchAccount() {
      localStorage.removeItem('username');
      localStorage.removeItem('token');
      window.location.href = '/login';
    },
    copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        alert('复制成功');
      }).catch(err => {
        console.error('复制失败', err);
      })
    }
  },
  mounted() {
    this.sendInitialQuestion();
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

//用户头像
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
  box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.2);
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

.chat-container {
  justify-content: center;
  margin-top: 10%;
  display: flex;
  height: 80%;
  width: 65%;
  margin: 5% auto;
  flex-direction: row;
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

.box-four {
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
  border-radius: 10px;
  padding: 10px;
  margin-top: 0%;
  background-color: rgba(255, 255, 255, 0.9);
  overflow-y: auto;
  height: 85%;
  font-size: 1.2em;
  color: #9c3f0a;
  font-weight: bold;
  text-shadow: 2px 2px 2px #5c190b3d;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2);
  scrollbar-color: #8a390a rgba(255, 255, 255, 0.9);
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
  margin: 0.5%;
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