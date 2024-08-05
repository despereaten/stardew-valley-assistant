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
        <img src="../assets/assistant/Haley_Icon.png" class="user-image" />
        <div v-if="showProfile" class="profile-details">
          <img src="../assets/assistant/Haley_Icon.png" class="profile-image" />
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
          <div class="top-box box-two">
            <img src="../assets/guesslike/TV.png" class="icon" />
            <p class="suggestion-text">猜你喜欢</p>
          </div>
          <div class="top-box box-three" @click="goto('/RoleShow')">
            <img src="../assets/role/Speech_bubble.png" class="icon" />
            <p class="suggestion-text">角色对话</p>
          </div>
          <div class="top-box box-four" @click="goto('/RoleMatching')">
            <img src="../assets/guesslike/Love_Icon.png" class="icon" />
            <p class="suggestion-text">伴侣匹配</p>
          </div>
        </div>

        <div class="response-box" ref="responseBox">
          <button class="refresh" @click="updateLinks">
          <img :class="{'refresh-icon': true, 'loading': loading}" src="../assets/guesslike/refresh.png" />
          刷新
          </button>
          <h2>猜你喜欢</h2>
          <p>以下网址是根据您的提问来推荐的网站，欢迎您的访问！</p>
          <div class="card-container">
            <div v-for="(link, index) in links" :key="index" class="card">
              <!-- <img src="../assets/guesslike/link.png" class="link-icon" /><a :href="link" target="_blank">{{ link }}</a>
              <img src="../assets/assistant/Haley_Icon.png" class="card-image" /> -->
              <!-- 在这里使用 LinkPrevue 组件 -->
              <linkprevue :url="link" />
            </div>
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
import linkprevue from '../components/linkprevue.vue';

export default {
components: {
  snow,
  flower,
  star,
  linkprevue
},
data() {
  return {
    links: [],
    showProfile: false,
    username: localStorage.getItem('username'),
    currentBackground: 'background-winter',
    currentComponent: 'snow',
    loading: false, 
  };
},
methods: {
  goto(route) {
      this.$router.push(route);
    },
  async fetchLinks() {
    try {
      //我希望在这里添加一步检查localStorage的userID对应的
      const response = await axios.get('/get_links');
      this.links = response.data.links;
      console.log("fetch links:",this.links);
      if(this.links.length===0){
        const generateResponse = await axios.post('/generate_links');
        this.links = generateResponse.data.links;
        console.log("first Generated links: ",this.links);
      }
    } catch (error) {
      console.error('Error fetching links:', error);
    }
  },
  async updateLinks(){
    this.loading = true;
    try{
    const response = await axios.post('/generate_links');
    this.links = response.data.links;
    console.log("update links:",this.links);
    }catch (error){
      console.log('Error updating links:', error);
    }finally {
        this.loading = false;  //new set
      }
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
},
mounted() {
  this.fetchLinks();
},
};

</script>

<style scoped lang="scss">
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
  bottom: 100%; /* 调整这个控制与 chat-container 顶部的距离 */
  left: 0;
  right: 0;
  padding: 0 20%;
  gap: 10px; /* 添加方框之间的间距 */
}

.top-box {
  width: 30%;
  height: 35px;
  background-color: #fcc587fe;
  box-shadow:
  -1px 0px 0 0 #8a390a,
  -2px 0px 0 0 #cd710f, /* 左边阴影 */
  -3px 0px 0 0 #ffa845,
  -4px 0px 0 0 #cd710f,
  -5px 0px 0 0 #8a390a, 

  1px 0px 0 0 #8a390a,/* 右边阴影 */
  2px 0px 0 0 #cd710f, 
  3px 0px 0 0 #ffa845,
  4px 0px 0 0 #cd710f,
  5px 0px 0 0 #8a390a, 


  inset 0px 1px 0 0 #8a390a,/* 上边阴影 */
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

.box-two {
  cursor:auto;
  height: 51px;

}

.icon{
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
  padding:30px;
  margin: 30px;
  background-color: rgba(255, 255, 255, 0.9);
  overflow-y: auto;
  height: 85%;
  font-size: 1.2em;
  color: #9c3f0a;
  font-weight: bold;
  text-shadow: 2px 2px 2px #5c190b3d;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2);
  scrollbar-color: #8a390a rgba(255, 255, 255, 0.9);
  position: relative; 
}

.refresh {
  position: absolute;
  top: 20px;
  right: 20px;
  border-radius: 10%;
  width: 80px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-color: #ba4d0d;
  border-color: #e9f5ff00;
  color: white;
  font-size: 0.8em;
  font-weight: bold;
  text-shadow: 2px 2px 2px #5c190b3d;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s;
}

.refresh-icon{
  width: 40%;
}

.loading {
  animation: rotate 1s linear infinite;  // Only apply animation when loading
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.refresh:hover .refresh-icon {
  animation: none;  // No animation 
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

.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: space-between;
  position: relative;

}

.card {
  background: #fff;
  border: 1px solid #8b4513;
  border-radius: 4px;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 48%;
  box-sizing: border-box;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 15px;

  display: flex;
  flex-direction: column;
  align-items: center;
}

.link-section {
  display: flex;
  align-items: center;
}

.link-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
  vertical-align: middle;
}


.card a {
  text-decoration: none;
  color: #8b4513;
  display: inline-flex;
  align-items: center;
  margin-bottom: 10px;
}

.card a:hover {
  text-decoration: underline;
}

.card-image {
  width: 50px;
  height: 50px;
  margin-top: 10px;
  margin-left: 10px;
}
</style>
