<template>
    <el-card class="charts">
        <div id="smileBar" style="width: 600px;height:400px;"></div>
    </el-card>
</template>

<script>
    import echarts from 'echarts';
    import Vue from 'vue'

    Vue.prototype.$echarts = echarts;

    export default {
        name: "fall",
        data() {
            return {
                smileCount: [
                    ['孙小虎', 12],
                    ['林子君', 7],
                    ['陈实', 6],
                    ['王大力', 5],
                    ['孙小林', 4],
                ]
            }
        },
        mounted() {
            this.myEcharts4();
        },
        methods: {
            myEcharts4() {
                // 基于准备好的dom，初始化echarts实例
                var myChart4 = this.$echarts.init(document.getElementById('smileBar'));
                // 指定图表的配置项和数据
                var option = {
                    title: {
                        text: '微笑排行',
                    },
                    xAxis: {type: 'category'},
                    yAxis: {},
                    dataset: {
                        source: this.smileCount
                    },
                    series: [{
                        name: '微笑',
                        type: 'bar',
                        encode: {x: 0, y: 1},
                    }]
                };
                // 使用刚指定的配置项和数据显示图表。
                myChart4.setOption(option);
            },
            setData(data) {
                this.smileCount = data;
                this.myEcharts4();
            }
        }
    }
</script>

<style scoped>

</style>