<template>
    <el-card class="charts">
        <div id="allLine" style="width: 600px;height:400px;"></div>
    </el-card>
</template>

<script>
    import echarts from 'echarts';
    import Vue from 'vue'

    Vue.prototype.$echarts = echarts;

    export default {
        name: "allLine",
        data() {
            return {
                allEvent: [
                    // ['07-01', 3, 2, 4, 6, 6],
                    // ['07-02', 4, 2, 6, 8, 2],
                    // ['07-03', 12, 24, 5, 6, 2, 6],
                    // ['07-04', 8, 3, 5, 7, 2],
                    // ['07-05', 4, 3, 5, 7, 2],
                    // ['07-06', 8, 2, 4, 6, 7],
                    // ['07-07', 12, 2, 4, 7, 2],
                ],
            }
        },
        mounted() {
            this.myEcharts1();
        },
        methods: {
            myEcharts1() {
                // 基于准备好的dom，初始化echarts实例
                var myChart1 = this.$echarts.init(document.getElementById('allLine'));
                // 指定图表的配置项和数据
                var option = {
                    title: {
                        text: '周事件趋势',
                    },
                    tooltip: {},
                    legend: {
                        data: ['事件数量']
                    },
                    xAxis: {type: 'category'},
                    yAxis: {},
                    dataset: {
                        source: this.allEvent
                    },
                    series: [{
                        name: '老人微笑',
                        type: 'line',
                        encode: {x: 0, y: 1},
                    }, {
                        name: '老人互动',
                        type: 'line',
                        encode: {x: 0, y: 2},
                    }, {
                        name: '陌生人来访',
                        type: 'line',
                        encode: {x: 0, y: 3},
                    }, {
                        name: '老人摔倒',
                        type: 'line',
                        encode: {x: 0, y: 4},
                    }, {
                        name: '禁区入侵',
                        type: 'line',
                        encode: {x: 0, y: 5},
                    }]
                };
                // 使用刚指定的配置项和数据显示图表。
                myChart1.setOption(option);
            },
            setData(data) {
                let tmp = data.concat();
                for (let i = 0; i < 7; i++) {
                    tmp[i] = data[6-i];
                }
                console.log(tmp);
                this.allEvent = tmp;
                console.log(this.allEvent)
                this.myEcharts1();
            }
        }
    }
</script>

<style scoped>

</style>
