<template>
    <div class="test">
    </div>


</template>

<script>
    export default {
        name: "webSocket",
        data() {
            return {
                websock: null,
            }
        },created() {
            this.initWebSocket();
        },destroyed() {
            this.websock.close() //离开路由之后断开websocket连接
        },methods: {
            initWebSocket(){ //初始化weosocket
                const wsuri = "ws://192.144.229.49:8000/api/websocket/link";
                this.websock = new WebSocket(wsuri);
                console.log('链接成功')
                this.websock.onmessage = this.websocketonmessage;
                this.websock.onopen = this.websocketonopen;
                this.websock.onerror = this.websocketonerror;
                this.websock.onclose = this.websocketclose;
            },
            websocketonopen(){ //连接建立之后执行send方法发送数据
                let actions = {"test":"测试消息"};
                this.websocketsend(JSON.stringify(actions));
            },
            websocketonerror(){//连接建立失败重连
                this.initWebSocket();
            },
            websocketonmessage(e){ //数据接收
                // const redata = JSON.parse(e.data);
                let res = e.data
                if(res == 'refresh'){
                    this.refresh()
                }
            },
            websocketsend(Data){//数据发送
                this.websock.send(Data);
            },
            websocketclose(e){  //关闭
                console.log('断开连接',e);
            },
            refresh(){
                this.$emit('getEvents')
                console.log('我刷新啦!')
                this.$message({
                    message: '有新事件,已刷新消息',
                    type: 'warning'
                });
            }
        },
    }
</script>

<style scoped>

</style>
