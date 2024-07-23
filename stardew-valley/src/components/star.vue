<template>
  <div v-for="item of 80" :key="item" class="snowflake"></div>
</template>

<script >

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
@keyframes snowfall {
  100% {
    transform: translate3d(var(--end), 100vh, 0);
  }
}

@for $i from 0 through 80 {
  .snowflake:nth-child(#{$i}) {
    --size: #{random(10) * 0.1}vw;
    --end: #{random(20) - 70}vw;
    left: #{random(150)}vw;
    animation: snowfall #{10 + random(20)}s linear infinite;
    animation-delay: -#{random(10)}s;
  }
}</style>
