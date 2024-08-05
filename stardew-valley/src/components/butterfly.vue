<template>
  <div>
    <img v-for="(image, index) in images" :key="index" :src="image.src" :class="['floating-image', image.class]" />
    <div class="click-area" @click="showImages"></div>
  </div>
</template>

<style scoped>
.floating-image {
  position: absolute;
  bottom: 50px;
  left: 30px;
  width: 40px; 
  height: 40px;
  animation: float 4s forwards;
}

@keyframes float {
  0% {
    opacity: 0;
    transform: translate(0, 0);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translate(var(--move-x), var(--move-y));
  }
}
</style>

<script>
import Butterfly from "../assets/homeview/ButterflyAnimated.gif";
import GreenButterfly from "../assets/homeview/GreenButterflyAnimated.gif";
import OrangeButterfly from "../assets/homeview/OrangeButterflyAnimated.gif";
import PinkButterfly from "../assets/homeview/PinkButterflyAnimated.gif";
import PurpleButterfly from "../assets/homeview/PurpleButterflyAnimated.gif";
import YellowButterfly from "../assets/homeview/YellowButterflyAnimated.gif";

export default {
  data() {
    return {
      images: []
    };
  },
  methods: {
    showImages() {
      this.images = [];
      setTimeout(() => {
        this.images = [
          { src: Butterfly, class: 'move-up' },
          { src: GreenButterfly, class: 'move-right-up' },
          { src: OrangeButterfly, class: 'move-right' },
          { src: PinkButterfly, class: 'move-right-down' },
          { src: PurpleButterfly, class: 'move-down' },
          { src: YellowButterfly, class: 'move-left-down' }
        ];
      }, 0);
    }
  }
};
</script>

<style scoped>
.move-up {
  --move-x: 0px;
  --move-y: -250px;
}
.move-right-up {
  --move-x: 70px;
  --move-y: -220px;
}
.move-right {
  --move-x: 130px;
  --move-y: -180px;
}
.move-right-down {
  --move-x: 190px;
  --move-y: -140px;
}
.move-down {
  --move-x: 220px;
  --move-y: -70px;
}
.move-left-down {
  --move-x: 250px;
  --move-y: 0px;
}
.click-area {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 120px;
  height: 120px;
  cursor: pointer;
  z-index: 10;
}
</style>
