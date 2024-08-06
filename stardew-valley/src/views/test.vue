<template>
  <div>
    <input v-model="query" placeholder="Enter your query" />
    <button @click="startStream">Start Streaming</button>
    <div v-for="(chunk, index) in responseChunks" :key="index">
      {{ chunk }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      responseChunks: []
    };
  },
  methods: {
    startStream() {
      const eventSource = new EventSource(`http://localhost:5000/stream?query=${encodeURIComponent(this.query)}`);
      
      eventSource.onmessage = (event) => {
        this.responseChunks.push(event.data);
        console.log("get data", event.data);
      };
      
      eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        eventSource.close();
      };
    }
  }
};
</script>
