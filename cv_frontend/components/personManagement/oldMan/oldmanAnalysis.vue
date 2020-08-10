<template>
    <el-dialog
            :title="title"
            :visible.sync="centerDetailVisible"
            width="70%"
            center>

        <div style="text-align: center">
        <el-card class="card">
            <div class="text">本周微笑次数</div>
            <div class="num">{{smile}}</div>

        </el-card>
            <div style="display: inline-block;width: 100px"></div>
        <el-card class="card">
            <div class="text">本周交互次数</div>
            <div class="num">{{communicate}}</div>
        </el-card>
        </div>

        <el-card class="charts">
            <div id="allLine" style="width: 850px;height:400px;"></div>
        </el-card>

        <span slot="footer" class="dialog-footer">
            <el-button  @click="setHide">关闭</el-button>
        </span>

    </el-dialog>

</template>

<script>
    import echarts from 'echarts';
    import Vue from 'vue'

    Vue.prototype.$echarts = echarts;
    export default {
        name: "oldmanAnalysis",
        data(){
            return{
                centerDetailVisible: false,
                title:'老人分析',
                smile:1,
                communicate:2,
                data:{},
                allData: []

            }
        },
        methods:{
            setVisible(){
                this.centerDetailVisible = true;
                this.$nextTick(function () {
                    // DOM is now updated
                    // `this` is bound to the current instance
                    this.myEcharts1();
                })

            },
            setHide(){
                this.centerDetailVisible = false
            },
            setData(data){
                this.smile = data.total.smile
                this.communicate = data.total.communicate
                this.title = data.name + '的分析'
                this.allData = data.detail
                console.log(this.allData)
                //TODO

            },myEcharts1() {
                // 基于准备好的dom，初始化echarts实例
                var myChart1 = this.$echarts.init(document.getElementById('allLine'));
                // 指定图表的配置项和数据
                var option = {
                    title: {
                        text: '周事件分析',
                    },
                    tooltip: {},
                    legend: {
                        data: ['事件数量']
                    },
                    xAxis: {type: 'category'},
                    yAxis: {},
                    dataset: {
                        source: this.allData
                    },
                    series: [{
                        name: '老人微笑',
                        type: 'line',
                        encode: {x: 0, y: 1},
                    }, {
                        name: '老人互动',
                        type: 'line',
                        encode: {x: 0, y: 2},
                    }]
                };
                // 使用刚指定的配置项和数据显示图表。
                myChart1.setOption(option);
            },
        },
        mounted() {

        }
    }
</script>

<style scoped>
    .text {
        font-size: 20px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .subtext {
        font-size: 14px;
        text-align: center;
    }

    .card {
        text-align: center;
        display: inline-block;
        margin-top: 20px;
        width: 400px;
    }
    .num {
        font-size: 40px;
        /*font-weight: 300;*/
        font-weight: bold;
    }
    .charts {
        width: 900px;
        height: 400px;
        margin: 20px auto;
    }



</style>
