<script setup lang="js">
import { ref } from 'vue'

const user = ref({
  "nick_name" : "",
  "real_name" : "",
  "sex" : "",
  "phone_number" : "",
  "verify_code" : "",
  "password" : ""
})

const repasswd = ref("")

</script>

<template>
  <div class="max-w-1/3 p-2 flex flex-col justify-center items-center">
    <span class="text-2xl font-semibold">用户注册</span>

    <div>
      <div class="form-item">
        <span>用户昵称：</span>
        <input v-model="user.nick_name" placeholder="Your nick name" class="form-input">
      </div>
    
      <div class="form-item">
        <span>真实姓名</span>
        <input v-model="user.real_name" placeholder="Your real name" class="form-input">
      </div>

      <span>性别</span>
      <select name="sex" v-model="user.sex">
        <option value="male">男</option>
        <option value="female">女</option>
      </select>

      <div class="form-item">
        <span>手机号：</span>
        <input v-model="user.phone_number" placeholder="123-4567-8900" class="form-input">
      </div>
      
      <div class="form-item">
        <span>验证码:</span>
        <div>
          <input v-model="user.verify_code" placeholder="0000" class="form-input">
          <button class="bg-blue-700 text-gray-50 p-1 rounded-lg text-sm">获取验证码</button>
        </div>
      </div>
    
      <div class="form-item">
        <span>密码：</span>
        <input v-model="user.password" placeholder="Your password" class="form-input">
      </div>

      <div class="form-item">
        <span>再次输入密码：</span>
        <input :value="repasswd" placeholder="Your password" class="form-input">
      </div>
      <button class="bg-blue-700 text-gray-50 p-1 rounded-lg text-sm">注册</button>
    </div>
    
  </div>
  <p>
    {{ user }}
  </p>

</template>

<style scoped>
  @reference "../style.css";
  .form-item{
    @apply flex flex-col my-1.5;
  }

  .form-input{
    @apply border border-gray-300 rounded-sm p-1
  }
</style>