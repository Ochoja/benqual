<script setup lang="ts">
import { reactive } from 'vue'
import { Bar, Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement
)

const props = defineProps({
  actual_values: Object,
  expected_values: Object
})

const actualChartData = reactive({
  labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
  datasets: [{ data: props.actual_values, backgroundColor: '#201c70', label: 'Actual Percentage' }]
})

const expectedChartData = reactive({
  labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
  datasets: [
    { data: props.expected_values, backgroundColor: '#00a650', label: 'Expected Percentage' }
  ]
})

const allChartData = reactive({
  labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
  datasets: [
    { data: props.expected_values, backgroundColor: '#00a650', label: 'Expected Percentage' },
    { data: props.actual_values, backgroundColor: '#201c70', label: 'Actual Percentage' }
  ]
})

const chartOptions = reactive({ responsive: true })
</script>

<template>
  <Bar id="expected-chart" :options="chartOptions" :data="expectedChartData" />
  <br />
  <Bar id="actual-chart" :options="chartOptions" :data="actualChartData" />
  <br />
  <Line id="line-chart" :options="chartOptions" :data="actualChartData" />
  <br />
  <Bar id="actual-chart" :options="chartOptions" :data="allChartData" />
</template>
