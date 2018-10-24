<template>
  <div class="container">
    <!-- <el-dialog
        title="提示"
        :visible.sync="dialogVisible"
        width="30%"
    >
        <span>{{ msg }}</span>
        <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
        </span>
    </el-dialog> -->
    <el-form label-width="100px">
      <el-form-item label="投票链接">
        <el-input type="text" v-model.trim="link" auto-complete="on"></el-input>
      </el-form-item>
      <el-form-item label="期望总票数">
        <el-input v-model="counts"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
      </el-form-item>
  </el-form>
  </div>
</template>

<script>
import axios from 'axios'
// import { Dialog } from 'element-ui'
import { setCookie, getCookie } from '../utils/cookies.js'

export default {
    data() {
        return {
            link: '',
            counts: '',
            msg: '',
            // dialogVisible: false
        }
    },
    methods: {
        submitForm() {
            let self = this;
            let params = new URLSearchParams();
            let user = self.link.split('userId=')[1].split('@')[0];
            let new_link= 'https://ppssp.xdf.cn/Mobile_Teacher_Home/like?u=' + user + '%40xdf.cn&protocol=https%3A';
            let info = new_link + '|' + self.counts;
            setCookie('x', info, 60*60*24*30);
            params.append('link', new_link);
            params.append('counts', self.counts);
            axios.post('http://localhost:5000/work', params)
            // .then((response) => {
            //     self.msg = response.data.msg;
            //     self.dialogVisible = true;
            // })
            .then(function() {
                self.$router.push('/progress');
            })
            .catch((err) => {
                console.log(err);
            })
        },
    }
}
</script>
