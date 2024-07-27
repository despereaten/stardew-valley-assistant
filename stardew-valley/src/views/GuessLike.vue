<template>
    <div class="guesslike-container">
        <h2>Guess You Like</h2>
        <div class="card-container">
            <div v-for="(link, index) in links" :key="index" class="card">
                <a :href="link" target="_blank">{{ link }}</a>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const links = ref([]);

const fetchLinks = async () => {
    try {
        const response = await axios.get('/get_links');
        links.value = response.data.links;
    } catch (error) {
        console.error('Error fetching links:', error);
    }
};

onMounted(() => {
    fetchLinks();
});
</script>
  
<style scoped lang="scss">
.guesslike-container {
    padding: 20px;
}

.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.card {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: calc(33.333% - 10px);
    box-sizing: border-box;
}

.card a {
    text-decoration: none;
    color: #007bff;
}

.card a:hover {
    text-decoration: underline;
}
</style>
  