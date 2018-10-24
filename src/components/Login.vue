<template>
  <!-- <el-form :model="loginForm" ref="loginForm" status-icon :rules="rules2" label-width="100px"> -->
  <el-form status-icon label-width="100px">
    <el-form-item label="账号">
      <el-input type="text" v-model.trim="username" autocomplete="on"></el-input>
    </el-form-item>
    <!-- <el-form-item label="密码" prop="password"> -->
    <el-form-item label="密码">
      <el-input type="password" v-model.trim="password" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm">登录</el-button>
    </el-form-item>
  </el-form>
</template>


<script>
  import sha256 from 'js-sha256'
  import axios from 'axios'
  import { Message } from 'element-ui'

  export default {
    data() {
      // var validateUser = (rule, value, callback) => {
      //   if (value === '') {
      //     callback(new Error('请输入账号'));
      //   } else {
      //     callback();
      //   }
      // };
      // var validatePass = (rule, value, callback) => {
      //   if (value === '') {
      //     callback(new Error('请输入密码'));
      //   } else {
      //     callback();
      //   }
      // };
      return {
          username: '',
          password: '',
        // rules2: {
        //   username: [
        //     { validator: validateUser, trigger: 'blur' }
        //   ],
        //   password: [
        //     { validator: validatePass, trigger: 'blur' }
        //   ]
        // }
      };
    },

    methods: {
      toMainPage() {
        this.$router.push("/");
      },

      submitForm() {
        // this.$refs[formName].validate((valid) => {
        //   if (valid) {
        // this.$refs[formName].password = sha256(this.$refs[formName].password)
        let params = new URLSearchParams();
        params.append('username', this.username);
        params.append('password', sha256(this.password));
        axios.post('http://localhost:5000/validateUser', params)
        .then((response) => {                           //  should use =>
          var msg = response.data.msg;
          if (msg.indexOf('success') != -1) {
            this.$router.push("/main");
          } else {
            this.$message({
              showClose: true,
              message: msg,
              type: 'error',
              center: true
            });
          }
        })
        .catch(function (error) {
          console.log(error);
        })
      },
    }
  }
</script>