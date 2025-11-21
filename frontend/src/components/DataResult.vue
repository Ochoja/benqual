<script setup lang="ts">
import { Icon } from '@iconify/vue';
import Chart from '../components/BarChart.vue';

interface DataQuality {
  total_records: number;
  valid_records: number;
  data_completeness: number;
  ready_for_analysis: boolean;
}

interface BenfordResult {
  actual_percentages: Record<number, number>;
  expected_percentages: Record<number, number>;
  'p-value': number;
  chi2_stat: number;
  ks_statistic?: number;
  ks_p_value?: number;
  mad?: number;
  records_analyzed?: number;
  data_quality?: DataQuality;
  issues?: string[];
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

      <!-- Data Quality Summary -->
      <div v-if="props.result?.data_quality" class="quality-summary">
        <h4>Data Quality Summary</h4>
        <div class="quality-stats">
          <div class="stat">
            <span class="label">Total Records:</span>
            <span class="value">{{ props.result.data_quality.total_records }}</span>
          </div>
          <div class="stat">
            <span class="label">Valid Records:</span>
            <span class="value">{{ props.result.data_quality.valid_records }}</span>
          </div>
          <div class="stat">
            <span class="label">Data Completeness:</span>
            <span class="value">{{ props.result.data_quality.data_completeness }}%</span>
          </div>
        </div>

        <div v-if="props.result.issues && props.result.issues.length > 0" class="issues">
          <h5>Data Issues Detected:</h5>
          <ul>
            <li v-for="(issue, idx) in props.result.issues.slice(0, 5)" :key="idx">
              {{ issue }}
            </li>
            <li v-if="props.result.issues.length > 5" class="more">
              ... and {{ props.result.issues.length - 5 }} more issues
            </li>
          </ul>
        </div>
      </div>

      <!-- Conformance message -->
      <p v-if="pValue >= 0.05" class="green">
        Data conforms with Benford's Law
      </p>
      <p v-else class="red">Data does not conform with Benford's Law</p>

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

      <!-- Statistical Tests -->
      <div class="other">
        <div><span class="bold">P-Value: </span>{{ pValue }}</div>
        <div><span class="bold">Chi-square: </span>{{ chi2_stat }}</div>
        <div v-if="props.result?.ks_statistic !== undefined">
          <span class="bold">KS Statistic: </span>{{ props.result.ks_statistic.toFixed(4) }}
        </div>
        <div v-if="props.result?.mad !== undefined">
          <span class="bold">MAD: </span>{{ props.result.mad.toFixed(4) }}
        </div>
      </div>

      <div v-if="props.result?.records_analyzed" class="records-info">
        <span class="bold">Records Analyzed: </span>{{ props.result.records_analyzed }}
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

    .quality-summary {
      background: #f5f5f5;
      padding: 15px;
      margin: 15px 0;
      border-radius: 5px;

      h4 {
        margin-bottom: 10px;
        color: #201c70;
      }

      h5 {
        margin-top: 15px;
        margin-bottom: 5px;
        font-size: 0.95em;
        color: #201c70;
      }

      .quality-stats {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 10px;

        .stat {
          display: flex;
          gap: 5px;

          .label {
            font-weight: 500;
          }

          .value {
            font-weight: 600;
            color: #00a650;
          }
        }
      }

      .issues {
        margin-top: 10px;

        ul {
          margin: 5px 0;
          padding-left: 20px;
          font-size: 0.9em;

          li {
            margin: 3px 0;
            color: #d32f2f;
          }

          li.more {
            color: #666;
            font-style: italic;
          }
        }
      }
    }

    .other {
      margin: 10px auto 25px auto;
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;

      .bold {
        font-weight: 600;
        color: #201c70;
      }
    }

    .records-info {
      text-align: center;
      margin-bottom: 15px;
      font-size: 0.95em;

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
