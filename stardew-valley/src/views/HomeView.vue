<template>
  <twinklestars></twinklestars>
  <FloatingImage />
  <butterfly />
  <div class="background">
    <img src="../assets/homeview/stardewvalley_character.png" class="logo" />
    <img src="../assets/homeview/ballon.png" class="floating balloon" />
    <img src="../assets/homeview/mysterious_box.png" class="floating box" />
    <img src="../assets/homeview/ButterflyAnimated.gif" class="butterfly top-right" />
    <img src="../assets/homeview/green_butterfly.png" class="green-butterfly" />
    <img src="../assets/homeview/purple_butterfly.png" class="purple-butterfly" />
    <img src="../assets/homeview/start.png" class="start-button" @click="goto('/Login')" />
    <div class="click-area" @click="showbutterflies"></div>
    <butterfly ref="butterfly" />
  </div>
  
</template>

<style scoped>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  overflow-x: hidden;
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

.logo {
  position: absolute;
  max-width: 100%;
  height: auto;
  animation: shake 3s infinite;
}

.floating {
  position: absolute;
  max-width: 90%;
  height: auto;
  animation: shake 4s infinite;
}

.butterfly.top-right {
  position: absolute;
  top: 5%;
  right: 5%;
  width: 5%;
}

.green-butterfly,
.purple-butterfly{
  position: absolute;
  max-width: 90%;
  height: auto;
}
.start-button {
  position: absolute;
  bottom: 10%;
  left: 60%;
  width: 20%;
  cursor: pointer;
  transition: transform 0.3s ease;
  z-index: 100;
}

.start-button:hover {
transform: scale(1.1);
}

.click-area {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100px;
  height: 100px;
  cursor: pointer;
}

@keyframes fadeIn {
  0%{
      opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes shake {
  0%, 100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(0, 15px);
  }
}


</style>


<script>
import twinklestars from '../components/twinklestars.vue'
import FloatingImage from '../components/FloatingImage.vue';
import butterfly from '../components/butterfly.vue';

export default {
  components:{
    twinklestars,
    FloatingImage,
    butterfly,
  },
  data(){
    return {
      images: []
    };
  },
methods: {
  goto(route) {
    this.$router.push(route);
  },
  showbutterflies() {
      this.$refs.butterfly.showImages();
    }
}
}

</script>