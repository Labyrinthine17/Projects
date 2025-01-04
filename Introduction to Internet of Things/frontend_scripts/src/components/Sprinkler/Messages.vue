<template>
  <div class="messages-container">
    <h2 class="messages-title">Message History</h2>
    <div class="message-items">
      <MessageItem
        v-for="(message, index) in messages"
        :key="index"
        :message="message"
      />
    </div>
  </div>
</template>

<script>
import MessageItem from "./MessageItem.vue";

export default {
  components: {
    MessageItem,
  },
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.messages-container {
  margin-top: 20px;
  height: 300px; /* Set fixed height */
  overflow-y: auto; /* Enable vertical scrolling if content exceeds height */
  border: 3px solid black; /* Optional: Border to distinguish the area */
  padding: 10px; /* Optional: Padding inside the container */
}
.messages-title {
  font-size: 1.5em;
  margin-top: 5px;
  margin-bottom: 5px;
  color: black;
  padding: 10px;
}
.message-items {
  border: 3px solid #ccc;
  height: 230px;
  overflow-y: auto; /* Enables vertical scrolling if content exceeds height */
  padding-right: 20px; /* Optional: Adjusts space for scrollbar */
  padding-left: 10px;
  padding-top: 10px;
}
</style>
