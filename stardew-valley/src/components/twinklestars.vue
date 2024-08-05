<template>
  <div v-for="item in 80" :key="item" class="snowflake"></div>
</template>

<script>
export default {
  name: 'Snowflakes'
};
</script>

<style scoped lang="scss">
.snowflake {
  --size: 0.4vw;
  width: var(--size);
  height: var(--size);
  background: url('../assets/assistant/stars.png') no-repeat;
  background-size: 100% 100%;
  position: fixed;
  top: -5vh;
  z-index: 1;
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

@for $i from 0 through 80 {
  .snowflake:nth-child(#{$i}) {
    --size: #{random(10) * 0.1}vw;
    --end: #{random(20) - 70}vw;
    top: #{random(60)}vh;  /* 随机在页面的上半部分 */
    left: #{random(100)}vw;
    animation: blink #{1 + random(3)}s linear infinite;  /* 闪烁动画 */
    animation-delay: -#{random(3)}s;
  }
}

</style>