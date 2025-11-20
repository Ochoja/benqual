<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import Navigation from '../components/SiteNavigation.vue'
import Button from '../components/TheButton.vue'
import Footer from '../components/TheFooter.vue'
import Result from '../components/DataResult.vue'
import { Icon } from '@iconify/vue'
import axios from 'axios'

const data = ref('')
let falseInput = ref(false)
let noInput = ref(false)
let values: number[] = []
let result: any = null
const showResultBtn = ref(false)
const loadingIcon = ref(false)
const showResult = ref(false)
const showFileResultBtn = ref(false)
const isFile = ref(false)
const fileName = ref('')
const isCSVFile = ref(false)
let formData = new FormData()
const column = ref('')
const isColumnEmpty = ref(false)
const loadingIconFile = ref(false)
const fileError = ref(false)

// Get values by ignoring commas and whitespace in input
const dataSet = computed(() => {
  return data.value.split(/[ ,]+/)
})

// print error message based on state
watch(dataSet, () => {
  let val = dataSet.value.join('').trim()
  val = val.replace(/[\s.]/g, '')
  if (isNaN(Number(val)) && val !== '') {
    falseInput.value = true
  } else {
    falseInput.value = false
    noInput.value = false
  }
})

// analyze input and send to backend
function analyzeData(vals: string[]) {
  if (falseInput.value || data.value.trim() === '') {
    noInput.value = true
    return
  } else {
    values = []
    for (let i of vals) {
      if (i != '') {
        values.push(parseInt(i))
      }
    }
  }
  loadingIcon.value = true
  axios
    .get(`https://benqual.onrender.com/api/benford_test/?data=[${values}]`)
    .then((response) => {
      result = response.data
      loadingIcon.value = false
      showResultBtn.value = true
      showFileResultBtn.value = false // Clear uploads
      console.log(result)
    })
    .catch((error) => {
      console.error('Error fetching data:', error)
    })
}

function checkFileType(event: any) {
  const file = event.target.files[0]
  fileName.value = file.name
  isFile.value = true
  const str = file.name.toLowerCase()

  if (
    str.endsWith('.csv') ||
    str.endsWith('.xls') ||
    str.endsWith('.xlsx') ||
    file.type === 'text/csv'
  ) {
    isCSVFile.value = true
    formData.append('file', file)
  } else {
    isCSVFile.value = false
  }
}

// analyze file
formData.append('column', column.value)
async function analyzeFile() {
  if (isCSVFile.value && isFile.value && column.value != '') {
    formData.set('column', column.value)

    try {
      loadingIconFile.value = true
      const response = await axios.post(
        'https://benqual.onrender.com/api/benford_test/upload/?file',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
      loadingIconFile.value = false
      isColumnEmpty.value = true
      showResultBtn.value = false
      result = response.data
      console.log(result)

      if (result.error) {
        fileError.value = true
        result = null
      } else {
        showFileResultBtn.value = true
        fileError.value = false
      }
    } catch (error) {
      console.log('Error uploading file')
    } // end try-catch
  } else {
    isColumnEmpty.value = true
    console.log('Upload File and Input column name')
  }
}
</script>

<template>
  <Teleport to="body">
    <div v-if="showResult" class="result">
      <Result :result="result" @close-modal="showResult = false"></Result>
    </div>
  </Teleport>
  <Navigation></Navigation>

  <main>
    <h2>Analyze Data</h2>

    <form>
      <h3>Input Data input</h3>
      <textarea v-model="data" placeholder="Input some numbers" class="values"></textarea>
      <!-- <input type="text" v-model="data" class="values" placeholder="Input some numbers" /> -->
      <p>Note: numbers should be seperated by commas or spaces</p>
      <p v-show="falseInput" class="warning">Only Numbers are allowed</p>
      <p v-show="noInput" class="warning">Please input some numbers</p>

      <div class="test">
        <Button :icon="`ph:play-fill`" @click.prevent="analyzeData(dataSet)">Test</Button>
        <Icon icon="eos-icons:loading" v-if="loadingIcon" class="loading" />
        <Button :icon="`carbon:result`" v-if="showResultBtn" @click.prevent="showResult = true">
          View Result
        </Button>
      </div>
    </form>

    <form>
      <h3>Upload Document</h3>
      <div class="upload">
        <input type="file" id="file-upload" accept=".csv, .xls, .xlsx" @change="checkFileType" />
        <label for="file-upload" class="upload-label" v-if="isFile">
          {{ fileName }} <Icon :icon="`ep:upload-filled`" class="icon"></Icon>
        </label>
        <label for="file-upload" class="upload-label" v-else>
          Upload CSV File <Icon :icon="`ep:upload-filled`" class="icon"></Icon>
        </label>
        <input type="text" v-model="column" placeholder="Type Column name to be Analyzed" />
      </div>
      <p v-show="!isCSVFile && fileName != ''" class="warning">
        Only Excel Files and CSV files Allowed
      </p>
      <p v-if="fileError" class="warning">Error Processing File. Check column name</p>
      <p v-if="isColumnEmpty" class="warning">Upload File and Input column name</p>
      <div class="test">
        <Button :icon="`ph:play-fill`" @click.prevent="analyzeFile">Test</Button>
        <Icon icon="eos-icons:loading" v-if="loadingIconFile" class="loading" />
        <Button :icon="`carbon:result`" v-if="showFileResultBtn" @click.prevent="showResult = true">
          View Result
        </Button>
      </div>
    </form>
  </main>

  <Footer></Footer>
</template>

<style lang="scss" scoped>
main {
  margin: 30px 50px;
  overflow-x: hidden;
  // min-height: 70vh;

  h2 {
    margin-bottom: 10px;
    text-align: center;
  }

  form {
    margin-bottom: 30px;

    h3 {
      font-weight: 500;
      margin-bottom: 10px;
    }

    p {
      padding: 5px 0;
    }

    p.warning {
      font-weight: 500;
      color: red;
      padding-top: 0;
    }

    .values {
      padding: 10px;
      border: 1px solid;
      width: 45%;
      height: 7em;
    }

    @media screen and (max-width: 1050px) {
      .values {
        width: 80%;
      }
    }

    @media screen and (max-width: 800px) {
      .values {
        width: 100%;
      }
    }

    .upload {
      display: flex;
      gap: 10px;
      margin-bottom: 10px;

      #file-upload {
        display: none;
      }

      .upload-label {
        padding: 10px;
        border: 1px solid;
        display: flex;
        gap: 8px;
        align-items: center;

        .icon {
          font-size: 1.5em;
          color: #00a650;
        }
      }

      input {
        border: 1px solid;
        padding: 10px 5px;
      }
    }

    @media screen and (max-width: 582px) {
      .upload {
        flex-direction: column;

        .upload-label {
          width: 45%;
          justify-content: space-between;
          gap: 0;
        }

        input {
          width: 80%;
        }
      }
    }

    @media screen and (max-width: 550px) {
      .upload {
        flex-direction: column;

        .upload-label {
          width: 60%;
          justify-content: space-between;
          gap: 0;
        }

        input {
          width: 95%;
        }
      }
    }

    .test {
      display: flex;
      gap: 10px;
      align-items: center;

      .loading {
        font-size: 1.5em;
        color: #00a650;
      }
    }
  }
}

@media screen and (max-width: 650px) {
  main {
    margin: 30px 25px;
  }
}
</style>
