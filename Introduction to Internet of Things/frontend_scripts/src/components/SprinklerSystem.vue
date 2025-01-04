<template>
  <div class="sprinkler-system-container">
    <h1 class="app-title">Sprinkler System</h1>
    <Status :status="status" @toggle="toggleSprinkler" />
    <Messages :messages="messages" />
  </div>
</template>

<script>
import axios from "axios";
import Status from "./Sprinkler/Status.vue";
import Messages from "./Sprinkler/Messages.vue";

export default {
  components: {
    Status,
    Messages,
  },
  data() {
    return {
      status: "OFF",
      messages: [],
    };
  },
  methods: {
    fetchStatus() {
      axios
        .get("http://localhost:5000/api/status")
        .then((response) => {
          this.status = response.data.status;
          this.$nextTick(() => {
            // console.log("UI status updated to:", this.status); // Debugging line
          });
        })
        .catch((error) => console.error("Error fetching status:", error));
    },
    toggleSprinkler() {
      const action = this.status === "OFF" ? "ON" : "OFF";
      axios
        .post("http://localhost:5000/api/activate", { action })
        .catch((error) => console.error("Error activating sprinkler:", error));
    },
    fetchMessages() {
      axios
        .get("http://localhost:5000/api/messages")
        .then((response) => {
          this.messages = response.data;
        })
        .catch((error) => console.error("Error fetching messages:", error));
    },
  },
  mounted() {
    this.fetchStatus();
    this.fetchMessages();
    setInterval(this.fetchStatus, 1000);
    setInterval(this.fetchMessages, 1000);
  },
};
</script>

<style scoped>
.sprinkler-system-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.app-title {
  text-align: center;
  color: #000000;
}
</style>
