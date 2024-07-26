<template>
  <div class="background">
    <img src="../assets/homeview/ButterflyAnimated.gif" class="butterfly top-right" />

    <div class="login-container">
      <div class="back-container" @click="goto('/')">
        <img src="../assets/homeview/back.png" class="back" />
      </div>

      <h2 class="title">登 录</h2>
      <input type="text" v-model="username" placeholder="用户名" class="input-field">
      <input type="password" v-model="password" placeholder="密码" class="input-field">
      <button @click="login" class="login-button">确认</button>
      <p class="register-link">没有账户？ <router-link to="/register">注册</router-link></p>
    </div>

    <div v-if="showAlert" class="alert">
      <p>登录失败：用户名或密码错误</p>
      <button @click="closeAlert">关闭</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      showAlert: false,
    };
  },
  methods: {
    goto(route) {
      this.$router.push(route);
    },
    login() {
      axios.post('http://localhost:5000/login', {
        username: this.username,
        password: this.password,
      })
      .then(response => {
        const token = response.data.access_token;
        const username = this.username;
        localStorage.setItem('token', token);
        localStorage.setItem('username', username);
        this.$router.push('/Assistant');
      })
      .catch(error => {
        console.error('Error logging in:', error);
        this.showAlert = true;
      });
    },
    closeAlert() {
      this.showAlert = false;
    }
  },
};
</script>

<style scoped lang="scss">
h2.title {
  color: #8b4513;
  margin-top: 0px;
  font-size: 2.8em;
  font-weight: bold;
}

.back-container {
  position: absolute;
  top: 25px;
  left: 25px;
  width: 50px;
  height: 50px;
  cursor: pointer;
  transition: transform 0.3s ease;
  &:hover {
    transform: scale(1.2);
  }
  .back {
    width: 100%;
    height: 100%;
  }
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
  background: url('../assets/homeview/bkgd2.png') no-repeat center center;
  background-size: cover;
}

.login-container {
  position: relative;
  justify-content: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 40%;
  margin: 13% auto;
  height: 50%;
  padding: 20px;
  border-radius: 20px;
  background-color: #facb95e4;
  box-shadow: inset #8a390a 0 0 0 2px,
              inset #ba4d0d 0 0 0 5px,
              inset #ffa845 0 0 0 9px,
              inset #cd710f 0 0 0 12px,
              inset #ba4d0d 0 0 0 14px,
              inset #8a390a 0 0 0 16px;
}

.input-field {
  margin: 2% 0;
  padding: 10px;
  font-size: 1.2em;
  border: 2px solid #8b4513;
  background-color: #deb887;
  color: #8b4513;
  box-shadow: 2px 2px 5px #8b4513;
  border-radius: 5px;
}

.login-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1.2em;
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

.register-link {
  margin-top: 20px;
  color: #8b4513;
}

.butterfly.top-right {
  position: absolute;
  top: 5%;
  right: 5%;
  width: 5%;
}

.alert {
  position: fixed;
  top: 10%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 20px;
  background-color: #facb95e4;
  box-shadow: inset #8a390a 0 0 0 1px,
              inset #ba4d0d 0 0 0 3px,
              inset #ffa845 0 0 0 5px,
              inset #cd710f 0 0 0 7px;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.alert p {
  margin: 0;
  color: #8b4513;
}

.alert button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #8b4513;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 2px 2px 5px #8b4513;
}
</style>