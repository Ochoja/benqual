<script setup lang="ts">
import { Icon } from '@iconify/vue'
import Chart from '../components/BarChart.vue'

const props = defineProps<{
  result?: any
}>()

const actual_percentage = props.result.actual_percentages
const expected_percentage = props.result.expected_percentages
let pValue: string | number = Number(props.result['p-value']).toFixed(4)
let chi2_stat: string | number = Number(props.result['chi2_stat']).toFixed(4)
pValue = parseFloat(pValue)

const actual_values: number[] = []
const expected_values: number[] = []

for (let i = 1; i <= 9; i++) {
  actual_values.push(actual_percentage[i])
  expected_values.push(expected_percentage[i])
}
</script>

<template>
  <div class="main">
    <div class="container">
      <Icon :icon="`carbon:close-filled`" class="close" @click="$emit('close-modal')"></Icon>
      <h3>Results</h3>

      <p v-if="pValue >= 0.05" class="green">Data conforms with Benford’s Law</p>
      <p v-else class="red">Data does not conform with Benford’s law</p>

      <div class="table">
        <div class="heading">
          <div>Number</div>
          <div>Expected %</div>
          <div>Actual %</div>
        </div>

        <div class="row" v-for="i in 9" :key="i">
          <div>{{ i }}</div>
          <div>{{ expected_percentage[i] }}</div>
          <div>{{ actual_percentage[i] }}</div>
        </div>
      </div>

      <div class="other">
        <div><span class="bold">P-Value: </span>{{ pValue }}</div>
        <div><span class="bold">Chi-square value : </span>{{ chi2_stat }}</div>
      </div>

      <div>
        <Chart :actual_values :expected_values></Chart>
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
