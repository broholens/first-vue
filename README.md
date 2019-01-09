# zz-vue

## 这个项目是一个练手项目，把给新东方老师刷票的脚本写成了网页版，脚本扩展成了API

### 开发过程中遇到的问题：
1. jsonp去请求自己服务器上的API
2. 页面刷新需要投票数据也刷新，在刷新时采用的方式是客户浏览器主动请求投票网站
3. 页面上的数据不是实时刷新的，每3秒刷新

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
