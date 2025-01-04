<template>
  <header class="header-bar">
    <h1 class="header-title">PyroShield</h1>
  </header>
  <div class="system-container">
    <DetectionSystem class="detection-system" />
    <SprinklerSystem class="sprinkler-system" />
    <GasLevelTrend class="gas-level-trend" />
  </div>
</template>

<script>
import DetectionSystem from "./components/DetectionSystem.vue";
import SprinklerSystem from "./components/SprinklerSystem.vue";
import GasLevelTrend from "./components/GasLevelTrend.vue";

export default {
  components: {
    DetectionSystem,
    SprinklerSystem,
    GasLevelTrend,
  },
};
</script>

<style scoped>
.header-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background-color: purple;
  color: white;
  border-radius: 20px;
  margin: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.header-title {
  font-size: 1.8em;
  margin: 0;
}

.system-container {
  display: grid;
  gap: 20px;
  padding: 20px;
  grid-template-columns: minmax(300px, 1fr) 1fr; /* Left column minimum width */
  grid-template-rows: 1fr 1fr; /* Equal height for rows */
  height: calc(
    100vh - 160px
  ); /* Full viewport height minus header and padding */
}

.detection-system {
  grid-column: 1;
  grid-row: 1;
  align-self: stretch; /* Allow component to fill available space */
  justify-self: stretch;
}

.sprinkler-system {
  grid-column: 2;
  grid-row: 1 / span 2; /* Span both rows */
  align-self: stretch;
  justify-self: stretch;
}

.gas-level-trend {
  grid-column: 1;
  grid-row: 2;
  align-self: stretch;
  justify-self: stretch;
}

@media (max-width: 900px) {
  .system-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
  }
  .sprinkler-system {
    grid-column: 1;
    grid-row: 3;
  }
}
</style>
