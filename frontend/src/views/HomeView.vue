<script setup lang="ts">
import Navigation from '../components/SiteNavigation.vue'
import Button from '../components/TheButton.vue'
import Footer from '../components/TheFooter.vue'
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="bg"></div>
  <header>
    <Navigation></Navigation>
    <div class="text">
      <div class="logo">BenQual</div>
      <p>A Data Quality Tool Based on Benford’s Law</p>

      <RouterLink to="/analyze">
        <Button>Analyze data</Button>
      </RouterLink>
    </div>
  </header>

  <main>
    <section>
      <h2>What is Benford Law</h2>
      <p>
        Benford's Law, also known as the First-Digit Law, is a statistical principle proposed by
        physicist Frank Benford in 1938. It reveals that in many datasets, the distribution of
        leading digits follows a non-uniform pattern, with smaller digits occurring more frequently
        than larger ones.
      </p>
      <br />
      <p>
        This phenomenon has broad applications across various fields like finance, accounting, and
        scientific research. By leveraging Benford's Law, analysts can detect anomalies, identify
        potential fraud, and validate data integrity with ease.
      </p>
      <br />
      <p>
        In essence, Benford's Law provides a powerful heuristic for uncovering hidden insights in
        numerical data, offering valuable perspectives that can enhance data analysis across diverse
        disciplines.
      </p>
    </section>

    <section>
      <h2>How To Analyze Data Using BenQual</h2>

      <div class="method">
        <h3>Method 1: Inputting Number Values</h3>
        <p>
          <span class="bold">Step 1:</span> Go to the
          <RouterLink to="/analyze">Analysis page</RouterLink>
        </p>
        <p>
          <span class="bold">Step 2:</span> Input data using the text field. Numbers should be
          seperated by space or commas.
        </p>
        <p><span class="bold">Step 3:</span> Click on the test button</p>
      </div>

      <div class="method">
        <h3>Method 2: Uploading a Document</h3>
        <p>
          <span class="bold">Step 1:</span> Go to the
          <RouterLink to="/analyze">Analysis page</RouterLink>
        </p>
        <p>
          <span class="bold">Step 2:</span> Click on Upload Document and select a
          <a
            href="https://en.wikipedia.org/wiki/Comma-separated_values#:~:text=Comma-separated%20values%20%28CSV%29%20is%20a%20text%20file%20format,of%20the%20file%20typically%20represents%20one%20data%20record."
            >CSV</a
          >
          file which contains data to be analyzed
        </p>
        <p>
          <span class="bold">Step 3:</span>Type name of Column to be analyzed in the input field.
        </p>
        <p><span class="bold">Step 4:</span> Click on the test button</p>
      </div>
    </section>
  </main>

  <Footer></Footer>
</template>

<style lang="scss" scoped>
.bg {
  height: 70vh;
  width: 100%;
  position: absolute;
  top: 0;
  background: url('../assets/bg.png') no-repeat;
  background-size: cover;
  background-position: center;
  z-index: 1;
}

header {
  color: #fff;
  width: 100%;
  height: 70vh;
  position: relative;
  background: rgba(32, 28, 112, 0.6);
  backdrop-filter: blur(4px);
  top: 0;
  z-index: 2;

  .text {
    height: 75%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 10px;

    .logo {
      font-family: 'Paytone One', sans-serif;
      font-size: 2em;
    }

    a {
      text-decoration: none;
    }
  }
}

main {
  padding: 0 25px;
  margin-bottom: 50px;

  section {
    margin-top: 50px;

    h2 {
      text-align: center;
      margin-bottom: 10px;
    }

    h3 {
      margin-bottom: 5px;
    }

    .method {
      margin-bottom: 20px;

      .bold {
        font-weight: 500;
      }

      a {
        color: #201c70;
        font-weight: 500;
      }
    }
  }
}
</style>
