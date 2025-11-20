<script setup lang="ts">
import { Icon } from '@iconify/vue';
import Chart from '../components/BarChart.vue';

interface BenfordResult {
  actual_percentages: Record<number, number>;
  expected_percentages: Record<number, number>;
  'p-value': number;
  chi2_stat: number;
}

const props = defineProps<{
  result?: BenfordResult;
}>();

// Safely extract values or default to empty objects
const actual_percentage = props.result?.actual_percentages ?? {};
const expected_percentage = props.result?.expected_percentages ?? {};

// Safe p-value and chi-square formatting
const pValue: number = props.result
  ? parseFloat(props.result['p-value'].toFixed(4))
  : 0;
const chi2_stat: number = props.result
  ? parseFloat(props.result.chi2_stat.toFixed(4))
  : 0;

// Prepare arrays for chart
const actual_values: number[] = [];
const expected_values: number[] = [];

for (let i = 1; i <= 9; i++) {
  actual_values.push(actual_percentage[i] ?? 0);
  expected_values.push(expected_percentage[i] ?? 0);
}
</script>

<template>
  <div class="main">
    <div class="container">
      <!-- Close button -->
      <Icon
        :icon="'carbon:close-filled'"
        class="close"
        @click="$emit('close-modal')" />

      <h3>Results</h3>

      <!-- Conformance message -->
      <p v-if="pValue >= 0.05" class="green">
        Data conforms with Benford’s Law
      </p>
      <p v-else class="red">Data does not conform with Benford’s Law</p>

      <!-- Results table -->
      <div class="table">
        <div class="heading">
          <div>Number</div>
          <div>Expected %</div>
          <div>Actual %</div>
        </div>

        <div class="row" v-for="i in 9" :key="i">
          <div>{{ i }}</div>
          <div>{{ expected_percentage[i] ?? 0 }}</div>
          <div>{{ actual_percentage[i] ?? 0 }}</div>
        </div>
      </div>

      <!-- P-value and Chi-square -->
      <div class="other">
        <div><span class="bold">P-Value: </span>{{ pValue }}</div>
        <div><span class="bold">Chi-square value: </span>{{ chi2_stat }}</div>
      </div>

      <!-- Chart -->
      <div>
        <Chart
          :actual_values="actual_values"
          :expected_values="expected_values" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.main {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;

  .container {
    background: #fff;
    min-width: 50%;
    max-height: 90%;
    overflow: auto;
    padding: 20px;
    position: relative;

    h3 {
      text-align: center;
    }

    .close {
      position: absolute;
      top: 10px;
      right: 10px;
      color: red;
      font-size: 1.5em;
      cursor: pointer;
    }

    .red,
    .green {
      text-align: center;
      font-weight: 500;
    }

    .red {
      color: red;
    }

    .green {
      color: #00a650;
    }

    .table {
      margin-top: 10px;

      .heading {
        font-weight: 500;
      }

      .row,
      .heading {
        display: flex;
        justify-content: space-between;

        div {
          height: 2.3em;
          min-width: 6em;
          padding: 5px;
          text-align: center;
        }
      }
    }

    .other {
      margin: 10px auto 25px auto;
      display: flex;
      justify-content: center;
      gap: 10px;

      .bold {
        font-weight: 600;
        color: #201c70;
      }
    }
  }

  @media screen and (max-width: 750px) {
    .container {
      height: 95%;
      width: 95%;
      padding: 10px;
    }
  }
}
</style>
