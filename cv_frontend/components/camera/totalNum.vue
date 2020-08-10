<template>
    <div>
        <el-row style="margin-left:80px; width: 1200px" type="flex" justify="space-between">
            <el-col :span="15" class="card">
                <el-card shadow="hover" :body-style="{padding: '0px'}">
                    <div class="grid-content grid-con-1">
                        <i class="el-icon-user grid-con-icon"></i>
                        <div class="grid-cont-right">
                            <div class="grid-num">{{total.elderNum}}</div>
                            <span class="subtext">{{currentTime}}</span>
                            <div class="maintext">老人数量</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="15" class="card">
                <el-card shadow="hover" :body-style="{padding: '0px'}">
                    <div class="grid-content grid-con-2">
                        <i class="el-icon-user grid-con-icon"></i>
                        <div class="grid-cont-right">
                            <div class="grid-num">{{total.staffNum}}</div>
                            <span class="subtext">{{currentTime}}</span>
                            <div class="maintext">工作人员数量</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="15" class="card">
                <el-card shadow="hover" :body-style="{padding: '0px'}">
                    <div class="grid-content grid-con-4">
                        <i class="el-icon-user grid-con-icon"></i>
                        <div class="grid-cont-right">
                            <div class="grid-num">{{total.volunteerNum}}</div>
                            <span class="subtext">{{currentTime}}</span>
                            <div class="maintext">义工数量</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="15" class="card">
                <el-card shadow="hover" :body-style="{padding: '0px'}">
                    <div class="grid-content grid-con-3">
                        <i class="el-icon-user grid-con-icon"></i>
                        <div class="grid-cont-right">
                            <div class="grid-num">{{total.strangerNum}}</div>
                            <span class="subtext">{{currentTime}}</span>
                            <div class="maintext">陌生人数量</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    export default {
        name: "totalNum",
        data(){
            return{
                total:{
                    elderNum: "0",
                    staffNum:"0",
                    volunteerNum: "0",
                    strangerNum:"0",
                },
                timer: "",
                currentTime: new Date(),
                websock:null
            }
        },methods:{
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
                console.log(typeof(res))
                if(res != 'refresh'){
                    this.total = JSON.parse(res)
                }
            },
            websocketsend(Data){//数据发送
                this.websock.send(Data);
            },
            websocketclose(e){  //关闭
                console.log('断开连接',e);
            },
        },
        created() {
            var _this = this; //声明一个变量指向Vue实例this，保证作用域一致
            this.timer = setInterval(function () {
                _this.currentTime = //修改数据date
                    new Date().getFullYear() +
                    "-" +
                    (new Date().getMonth() + 1) +
                    "-" +
                    new Date().getDate() +
                    " " +
                    new Date().getHours() +
                    ":" +
                    new Date().getMinutes() +
                    ":" +
                    new Date().getSeconds();
            }, 1000);
            this.initWebSocket();
        },
        beforeDestroy() {
            if (this.timer) {
                clearInterval(this.timer); // 在Vue实例销毁前，清除我们的定时器
            }
            this.websock.close()
        }
    }
</script>

<style scoped>
    .maintext {
        font-size: 16px;
        text-align: center;
    }


    .subtext {
        font-size: 14px;
        text-align: center;
    }

    .card {
        text-align: center;
        margin-top: 20px;
        width: 250px;
    }

    .grid-content {
        display: flex;
        align-items: center;
        height: 100px;
    }

    .grid-cont-right {
        flex: 1;
        text-align: center;
        font-size: 14px;
        color: #999;
    }

    .grid-num {
        font-size: 30px;
        font-weight: bold;
    }

    .grid-con-icon {
        font-size: 50px;
        width: 100px;
        height: 100px;
        text-align: center;
        line-height: 100px;
        color: #fff;
    }
    .grid-con-1 .grid-con-icon {
        background: rgb(45, 140, 240);
    }

    .grid-con-1 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-2 .grid-con-icon {
        background: rgb(100, 213, 114);
    }

    .grid-con-2 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-3 .grid-con-icon {
        background: rgb(242, 94, 67);
    }

    .grid-con-3 .grid-num {
        color: rgb(242, 94, 67);
    }

    .grid-con-4 .grid-con-icon {
        background: rgb(242, 229, 87);
    }

    .grid-con-4 .grid-num {
        color: rgb(45, 140, 240);
    }

</style>
