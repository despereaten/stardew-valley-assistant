<template>
  <div @click="handleClick" class="clickable-area">
    <transition-group name="fade" tag="div">
      <div
        v-for="(image, index) in images"
        :key="index"
        :style="image.style"
        class="floating-image"
      >
        <img :src="imageSrc" />
      </div>
    </transition-group>
  </div>
</template>

<script>
import leaf from "../assets/homeview/leaf.png";

export default {
  data() {
    return {
      images: [],
      imageSrc: leaf,
    };
  },
  methods: {
    handleClick(event) {
      const { clientX: x, clientY: y } = event;
      const width = window.innerWidth;
      const height = window.innerHeight;

      // 检查点击区域是否在树叶附近
      if (
        (x < width / 5 && y < height / 4) || 
        (x < width / 4 && y < height / 4) || 
        (x < width / 2 && y < height / 4) || 
        (x > (3 * width) / 5 && y < height / 4) 
      ) {
        this.createImages(x, y);
      }
    },
    createImages(x, y) {
      const maxImages = 10;
      const intervalDelay = 300; // 300ms 之后显示每个图片
      const displayDuration = 4000; // 图片显示的总时间 (ms)

      for (let i = 0; i < maxImages; i++) {
        setTimeout(() => {
          const randomX = x + Math.floor(Math.random() * 51) - 25; // 在 x ± 25 的范围内随机生成 x 坐标
          const randomRotation = Math.random() * 360; // 随机生成初始旋转角度
          const image = {
            style: {
              top: `${y}px`,
              left: `${randomX}px`,
              transform: `rotate(${randomRotation}deg)`,
            },
          };
          this.images.push(image);

          setTimeout(() => {
            this.images.splice(this.images.indexOf(image), 1); // 移除对应的图片
          }, displayDuration); // 4s 后移除图片
        }, i * intervalDelay);
      }
    },
  },
};
</script>

<style scoped>
.clickable-area {
  width: 100vw;
  height: 50vh;
  position: relative;
  overflow: hidden;
}

.floating-image {
  position: absolute;
  animation: float 4s ease-in-out forwards;
}

@keyframes float {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  100% {
    transform: translateY(300px) rotate(360deg);
    opacity: 0;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
