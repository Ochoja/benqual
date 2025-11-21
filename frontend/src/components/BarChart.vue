<script setup lang="ts">
import { computed } from 'vue';
import { Bar, Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  type ChartData,
  type ChartOptions,
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
);

// Props
const props = defineProps<{
  actual_values: number[];
  expected_values: number[];
}>();

const labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];

// Chart data for Bar charts
const actualBarData = computed<ChartData<'bar', number[], string>>(() => ({
  labels,
  datasets: [
    {
      label: 'Actual Percentage',
      data: props.actual_values,
      backgroundColor: '#201c70',
    },
  ],
}));

const expectedBarData = computed<ChartData<'bar', number[], string>>(() => ({
  labels,
  datasets: [
    {
      label: 'Expected Percentage',
      data: props.expected_values,
      backgroundColor: '#00a650',
    },
  ],
}));

const allBarData = computed<ChartData<'bar', number[], string>>(() => ({
  labels,
  datasets: [
    {
      label: 'Expected Percentage',
      data: props.expected_values,
      backgroundColor: '#00a650',
    },
    {
      label: 'Actual Percentage',
      data: props.actual_values,
      backgroundColor: '#201c70',
    },
  ],
}));

// Chart data for Line chart
const actualLineData = computed<ChartData<'line', number[], string>>(() => ({
  labels,
  datasets: [
    {
      label: 'Actual Percentage',
      data: props.actual_values,
      borderColor: '#201c70',
      backgroundColor: '#201c70',
      fill: false,
    },
  ],
}));

// Chart options for Bar charts
const barOptions: ChartOptions<'bar'> = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Benford Analysis - Bar' },
  },
};

// Chart options for Line charts
const lineOptions: ChartOptions<'line'> = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Benford Analysis - Line' },
  },
};
</script>

<template>
  <div>
    <Bar :data="expectedBarData" :options="barOptions" />
    <Bar :data="actualBarData" :options="barOptions" />
    <Line :data="actualLineData" :options="lineOptions" />
    <Bar :data="allBarData" :options="barOptions" />
  </div>
</template>
