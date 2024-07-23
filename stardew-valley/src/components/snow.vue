
<template>
  <div v-for="item of 100" :key="item" class="snowflake"></div>
</template>

<script >

</script>

<style scoped lang="scss">
.snowflake {
  --size: 0.4vw;
  width: var(--size);
  height: var(--size);
  background: url('../assets/assistant/snow.png') no-repeat;
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

@for $i from 0 through 100 {
  .snowflake:nth-child(#{$i}) {
    //每个雪花的大小
    --size: #{random(10) * 0.1}vw;
    //雪花移动目标点 -70后是负数 这样雪花会向左下方飘落
    --end: #{random(20) - 10}vw;
    left: #{random(150)}vw;
    animation: snowfall #{10 + random(20)}s linear infinite;
    animation-delay: -#{random(10)}s;
  }
}</style>
