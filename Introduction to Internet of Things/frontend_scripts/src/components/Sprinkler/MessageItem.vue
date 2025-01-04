<template>
  <div class="message-item">
    {{ message }}
  </div>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.message-item {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 10px;
  background-color: #fff;
  transition: background-color 0.3s;
  color: black;
}
.message-item:hover {
  background-color: #f1f1f1;
}
</style>
