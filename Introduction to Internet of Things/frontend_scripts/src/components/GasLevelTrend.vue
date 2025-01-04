<template>
  <div class="gas-level-trend">
    <h2 class="gas-level-trend-title">Gas Level Trend</h2>
    <canvas ref="gasLevelChart"></canvas>
    <div v-if="gasLevels.length === 0" class="no-data-message">
      No historical gas level data available.
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
} from "chart.js";

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip
);

export default {
  name: "GasLevelTrend",
  setup() {
    const gasLevels = ref([]);
    const gasLevelChart = ref(null);
    const chartInstance = ref(null); // Reference for the chart instance
    let fetchInterval = null; // Store interval ID for cleanup

    const fetchGasLevels = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/gas_history");
        if (response.ok) {
          const data = await response.json();
          gasLevels.value = data;
          renderChart(); // Re-render chart with new data
        } else {
          console.error("Failed to fetch gas level data");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    };

    const renderChart = () => {
      if (chartInstance.value) {
        chartInstance.value.destroy(); // Destroy the existing chart instance if it exists
      }

      const ctx = gasLevelChart.value.getContext("2d");
      const labels =
        gasLevels.value.length > 0
          ? gasLevels.value.map((entry) => entry.timestamp)
          : ["No Data"];
      const data =
        gasLevels.value.length > 0
          ? gasLevels.value.map((entry) => entry.value)
          : [0]; // Set a default value for the empty state

      chartInstance.value = new Chart(ctx, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Gas Level",
              data,
              borderColor:
                gasLevels.value.length > 0
                  ? "rgba(75, 192, 192, 1)"
                  : "rgba(200, 200, 200, 0.5)", // Use a lighter color if no data
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              fill: true,
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              title: { display: true, text: "Time" },
            },
            y: {
              title: { display: true, text: "Gas Level" },
              min: 0, // Set a minimum for the Y-axis
            },
          },
          interaction: {
            intersect: false,
          },
        },
      });
    };

    onMounted(() => {
      fetchGasLevels(); // Initial fetch
      fetchInterval = setInterval(fetchGasLevels, 5000); // Poll every 5 seconds
    });

    onBeforeUnmount(() => {
      clearInterval(fetchInterval); // Clear the interval when component is unmounted
      if (chartInstance.value) {
        chartInstance.value.destroy(); // Clean up the chart instance
      }
    });

    return {
      gasLevelChart,
      gasLevels,
    };
  },
};
</script>

<style scoped>
.gas-level-trend {
  background-color: #e0f7fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.gas-level-trend-title {
  color: black;
}

.no-data-message {
  text-align: center;
  color: #999;
  margin-top: 20px;
  font-size: 1.3em;
}
</style>
