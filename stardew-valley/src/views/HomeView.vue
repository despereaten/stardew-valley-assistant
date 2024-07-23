<template>
  <div>
    <div>
      <button @click="startNewSession">开始新会话</button>
      <div>
        <h3>选择会话</h3>
        <ul>
          <li v-for="session in sessions" :key="session">
            <button @click="selectSession(session)">会话 {{ session }}</button>
            <button @click="deleteSession(session)">删除</button> <!-- 添加删除按钮 -->
          </li>
        </ul>
      </div>
    </div>
    <div v-if="currentSessionId">
      <h3>当前会话: {{ currentSessionId }}</h3>
      <div>
        <ul>
          <li v-for="message in messages" :key="message.id">
            <b>{{ message.sender }}:</b> {{ message.message }}
          </li>
        </ul>
      </div>
      <div>
        <input v-model="newMessage" placeholder="输入消息" @keyup.enter="sendMessage">
        <button @click="sendMessage">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sessions: [],
      currentSessionId: null,
      messages: [],
      newMessage: ''
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
          })
          .catch(error => {
            console.error('Error creating new session:', error);
          });
    },
    selectSession(sessionId) {
      this.currentSessionId = sessionId;
      this.loadHistory(sessionId);
    },
    loadHistory(sessionId) {
      axios
          .get(`http://localhost:5000/get_history/${sessionId}`)
          .then(response => {
            this.messages = response.data.history;
          })
          .catch(error => {
            console.error('Error loading history:', error);
          });
    },
    sendMessage() {
      if (this.newMessage.trim() === '') return;
      axios
          .post('http://localhost:5000/send_message', {
            session_id: this.currentSessionId,
            message: this.newMessage
          })
          .then(response => {
            this.messages.push({
              sender: 'User',
              message: this.newMessage
            });
            this.messages.push({
              sender: 'AI',
              message: response.data.response
            });
            this.newMessage = '';
          })
          .catch(error => {
            console.error('Error sending message:', error);
          });
      axios
          .post('http://localhost:5000/send_message', {
            session_id: this.currentSessionId,
            message: this.newMessage
          })
          .then(response => {
            this.chatMessages.push({
              id: Date.now(),
              sender: 'User',
              message: this.newMessage
            });
            this.chatMessages.push({
              id: Date.now()+1,
              sender: 'AI',
              message: response.data.response
            });
            this.newMessage = '';
          })
          .catch(error => {
            console.error('Error sending message:', error);
          });
    },
    deleteSession(sessionId) {  // 添加删除会话的方法
      axios
          .delete(`http://localhost:5000/delete_session/${sessionId}`)
          .then(() => {
            this.sessions = this.sessions.filter(session => session !== sessionId);
            if (this.currentSessionId === sessionId) {
              this.currentSessionId = null;
              this.messages = [];
            }
          })
          .catch(error => {
            console.error('Error deleting session:', error);
          });
    }
  }
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>