<template>
  <div class="main">
    <div class="card">
      <input v-model="age" placeholder="年龄">
      <input v-model="gender" placeholder="性别">
      <input v-model="height" placeholder="身高">
      <input v-model="weight" placeholder="体重">
    </div>

    <div class="card">
      <textarea v-model="symptom" placeholder="症状描述"></textarea>
      <button @click="submit">开始分析</button>
    </div>

    <div class="card">
      <pre>{{result}}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const age = ref("");
const gender = ref("");
const height = ref("");
const weight = ref("");
const symptom = ref("");
const result = ref("");

function submit(){
  fetch("http://127.0.0.1:5000/ask",{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify({ question: symptom.value })
  })
  .then(r=>r.json())
  .then(d=>result.value=d.answer);
}
</script>
