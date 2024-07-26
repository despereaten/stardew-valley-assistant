<template>
    <div v-html="renderedMarkdown"></div>
  </template>
  
  <script>
  import MarkdownIt from 'markdown-it';
  
  export default {
    name: 'MarkdownRenderer',
    props: {
      markdown: {
        type: String,
        required: true,
      },
    },
    computed: {
      renderedMarkdown() {
        const md = new MarkdownIt();
        return md.render(this.markdown);
      },
    },
  };
  </script>
  
  <style scoped>
  /* 添加一些样式来美化渲染的Markdown内容 */
  </style>
  