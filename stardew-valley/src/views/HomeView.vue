<template>
  <div class="chat-container">
    <div class="response-box">
      <p v-for="msg in chatMessages" :key="msg.id"
        :class="{ 'user-message': msg.isUser, 'assistant-message': !msg.isUser }">
        {{ msg.content }}
      </p>
    </div>
    <div class="input-box">
      <textarea v-model="userInput" placeholder="Type your message here..."></textarea>
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: '',
      chatMessages: []  // 保存所有的聊天消息
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === '') return;

      // 添加用户输入到聊天记录中
      this.chatMessages.push({ id: Date.now(), content: `${this.userInput}:你`, isUser: true });
      try {
        const messageToSend = this.userInput;
        this.userInput = '';

        const response = await fetch('http://127.0.0.1:5000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: messageToSend })
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.chatMessages.push({ id: Date.now() + 1, content: `星露谷小助手: ${data.response}`, isUser: false });

      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.response-box {
  width: 100%;
  height: 300px;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 20px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.input-box {
  display: flex;
  align-items: center;
  width: 100%;
}

textarea {
  flex-grow: 1;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.user-message {
  text-align: right;
  border: 1px solid #007bff;
  border-radius: 4px;
  padding: 5px;
  margin: 5px 0;
  background-color: #e9f5ff;
}

.assistant-message {
  text-align: left;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 5px;
  margin: 5px 0;
  background-color: #f1f1f1;
}
</style>
