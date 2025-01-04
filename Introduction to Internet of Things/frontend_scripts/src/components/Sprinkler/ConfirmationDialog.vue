<template>
    <div v-if="show" class="dialog-overlay">
      <div class="dialog">
        <p>{{ message }}</p>
        <button @click="confirm" class="confirm-btn">Confirm</button>
        <button @click="cancel" class="cancel-btn">Cancel</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      show: {
        type: Boolean,
        default: false,
      },
      message: {
        type: String,
        default: "Are you sure you want to proceed?",
      },
    },
    emits: ["confirm", "cancel"],
    methods: {
      confirm() {
        this.$emit("confirm");
      },
      cancel() {
        this.$emit("cancel");
      },
    },
  };
  </script>
  
  <style scoped>
  .dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .dialog {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
  }
  .confirm-btn {
    margin: 5px;
    padding: 10px 15px;
    background-color: red;
    color: white;
    border: none;
    cursor: pointer;
  }
  .cancel-btn {
    margin: 5px;
    padding: 10px 15px;
    background-color: gray;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>
  