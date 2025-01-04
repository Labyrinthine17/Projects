<template>
  <div class="detection-info">
    <p>
      Status:
      <span :class="detectionStatus === 'Unknown' ? 'Unknown': detectionStatus === 'False' ? 'Safe' : 'Danger'">
        {{
          detectionStatus === "Unknown"
            ? "Unknown"
            : detectionStatus === "False"
            ? "Safe"
            : "Danger"
        }}
      </span>
    </p>
    <p>
      Temperature:
      <span class="temperature">{{ temperature !== null ? `${temperature} °C` : "NA" }}</span>
    </p>
    <p>
      Gas Level:
      <span class="gas-level">{{ gasLevel !== null ? `${gasLevel} ppm` : "Unknown" }}</span>
    </p>
  </div>
</template>

<script>
export default {
  props: {
    detectionStatus: {
      type: String,
      required: true,
    },
    temperature: {
      type: [Number,null],
      required: true,
    },
    gasLevel: {
      type: [Number,null],
      required: true,
    },
  },
};
</script>

<style scoped>
.detection-info {
  color: #333;
}

.Safe {
  font-weight: bold;
  color: #388e3c; /* Green for safe status */
}

.Danger {
  font-weight: bold;
  color: #c62828; /* Red for danger status */
}
</style>
