<template>
  <div class="detection-system-container">
    <h2 class="detection-title">Fire Hazard Detection System</h2>
    <DetectionInfo
      :detectionStatus="detectionStatus"
      :temperature="temperature"
      :gasLevel="gasLevel"
    />
  </div>
</template>

<script>
import axios from "axios";
import DetectionInfo from "./DetectionSystem/DetectionInfo.vue";

export default {
  components: {
    DetectionInfo,
  },
  data() {
    return {
      detectionStatus: "Unknown",
      temperature: null,
      gasLevel: null,
    };
  },
  methods: {
    fetchDetectionData() {
      axios
        .get("http://localhost:5000/api/detection")
        .then((response) => {
          this.detectionStatus = response.data.danger;
          this.temperature = response.data.temperature;
          this.gasLevel = response.data.gasLevel;
        })
        .catch((error) =>
          console.error("Error fetching detection data:", error)
        );
    },
  },
  mounted() {
    this.fetchDetectionData();
    setInterval(this.fetchDetectionData, 1000);
  },
};
</script>

<style scoped>
.detection-system-container {
  background-color: #e0f7fa; 
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.detection-title {
  color: black;
}
</style>
