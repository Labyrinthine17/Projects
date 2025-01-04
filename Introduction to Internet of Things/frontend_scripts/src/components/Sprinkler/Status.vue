<template>
  <div class="status-container">
    <p class="status-text">
      Current Status:
      <span :class="status === 'OFF' ? 'status-off' : 'status-on'">
        {{ status }}
      </span>
    </p>
    <button @click="showConfirmationDialog = true" class="toggle-button">
      {{ status === "OFF" ? "Activate" : "Deactivate" }} Sprinkler
    </button>

    <!-- Confirmation Dialog -->
    <ConfirmationDialog
      v-if="showConfirmationDialog"
      :show="showConfirmationDialog"
      :message="`Are you sure you want to ${
        status === 'OFF' ? 'activate' : 'deactivate'
      } the sprinkler?`"
      @confirm="confirmToggle"
      @cancel="showConfirmationDialog = false"
    />
  </div>
</template>

<script>
import ConfirmationDialog from "./ConfirmationDialog.vue";

export default {
  components: {
    ConfirmationDialog,
  },
  props: {
    status: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showConfirmationDialog: false,
    };
  },
  methods: {
    confirmToggle() {
      this.$emit("toggle");
      this.showConfirmationDialog = false;
    },
  },
};
</script>

<style scoped>
.status-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.status-text {
  color: black;
  font-size: 1.2em;
  font-weight: bold;
}
.status-on {
  color: green;
}
.status-off {
  color: red;
}
.toggle-button {
  padding: 10px 20px;
  font-size: 1em;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.toggle-button:hover {
  background-color: #0056b3;
}
</style>
