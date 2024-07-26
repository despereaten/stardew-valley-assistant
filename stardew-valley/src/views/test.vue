<template>
  <div class="about">
    <h1>This is an test</h1>
    <input v-model="name" placeholder="Enter your name">
    <button @click="sendPost">Send POST request</button>
    <button @click="stopGenerating">Stop Generating</button>
    <button @click="restartGenerating">Restart Generating</button>
    <pre>{{ response }}</pre>
  </div>
</template>
<script>
export default {
  data() {
    return {
      name: '',
      response: '',
      controller: new AbortController(),
      isStopped: false
    }
  },
  methods: {
    async sendPost() {
      this.controller = new AbortController()
      this.response = ''
      this.isStopped = false
      const response = await fetch('http://127.0.0.1:5000/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: this.name }),
        signal: this.controller.signal
      })
      const reader = response.body.getReader()
      while (true) {
        if (this.isStopped) break
        const { done, value } = await reader.read()
        if (done) break
        this.response += new TextDecoder().decode(value)
      }
    },

    stopGenerating() {
      this.controller.abort()
      this.isStopped = true
    },
    restartGenerating() {
      this.controller = new AbortController()
      this.sendPost()
    }
  }
}
</script>
<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
