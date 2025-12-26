<template>
  <div class="chat-wrapper">
    <div class="chat-header">AI 中医智能问诊</div>

    <div class="chat-body">
      <div v-for="(m,i) in messages" :key="i" :class="['msg',m.role]">
        {{m.text}}
      </div>
      <div v-if="thinking" class="msg ai">🌿 正在辨证分析...</div>
    </div>

    <div class="chat-input">
      <input v-model="input" placeholder="请输入症状描述">
      <button @click="send">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const input = ref("");
const messages = ref([
  { role:"ai", text:"你好，我是你的中医智能问诊助手。" }
]);
const thinking = ref(false);
const history = ref([]);

async function send(){
  if(!input.value) return;
  messages.value.push({role:"user",text:input.value});
  thinking.value = true;

  const res = await fetch("/chat",{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify({ message: input.value, history: history.value })
  });

  const data = await res.json();
  thinking.value = false;
  messages.value.push({role:"ai",text:data.reply});
  input.value="";
}
</script>
