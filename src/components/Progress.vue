<template>
  <div class="container">
    <el-progress type="circle" :stroke-width="18" :percentage="percentage"></el-progress>
    <p>票数:  {{ current_count }} / {{ expect_count }}</p>
    <p v-text="remaining_time"></p>
  </div>
</template>

<script>
import { getCookie } from '../utils/cookies.js'
import jsonp from 'jsonp'


export default {
    data() {
        return {
            percentage: 0,
            link: '',
            expect_count: 0,
            current_count: 0,
            remaining_time: ''
        }
    },
    created() {
        this.getPercentage();
        this.calculateRemainingTime();
    },
    methods: {
        getPercentage: function() {
            let self = this;
            let cookie = getCookie('x').split('|');
            self.link = cookie[0];
            self.expect_count = cookie[1];
            let clearInt = setInterval(function() {
                console.log(self.link, self.expect_count);
                jsonp(self.link, null, function(err, data) {
                    if (err) {
                        console.log(err);
                    } else {
                        self.current_count = data.Count;
                        self.percentage = parseFloat((self.current_count/self.expect_count*100).toFixed(2));
                    }
                    if (self.current_count >= self.expect_count) {
                        self.percentage = 100;
                        self.current_count = self.expect_count;
                        clearInterval(clearInt);
                    }
                })
            }, 3000)
        },
        calculateRemainingTime() {
            let self = this;
            let clearInt = setInterval(function() {
                let count = self.expect_count - self.current_count;
                if (count <= 0) {
                    self.remaining_time = '';
                    clearInterval(clearInt);
                } else {
                    let hour = Math.floor(count / 60 / 60);
                    let minute = Math.floor(count / 60) % 60;
                    let second = count % 60;
                    let msg = '';
                    if (second > 0) {
                        msg = second + '秒';
                    }
                    if (minute > 0){
                        msg = minute + '分钟' + msg;
                    }
                    if (hour > 0) {
                        msg = hour + '小时' + msg;
                    }
                    self.remaining_time = '预计剩余时间： ' + msg;
                    if (count >= self.expect_count) {
                        self.remaining_time = '';
                    }
                }
            }, 1000);
        }
    },
}
</script>
