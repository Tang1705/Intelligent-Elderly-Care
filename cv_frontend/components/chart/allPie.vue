<template>
    <el-card class="charts">
        <div id="allPie" style="width: 600px;height:400px;"></div>
    </el-card>
</template>

<script>
    import echarts from 'echarts';
    import Vue from 'vue'

    Vue.prototype.$echarts = echarts;

    export default {
        name: "allPie",
        data() {
            return {
                allEventCount: [['老人微笑', 0],
                    ['老人互动', 0],
                    ['陌生人来访', 0],
                    ['老人摔倒', 0],
                    ['禁区入侵', 0],],
                allCount: 0,
            }
        },
        mounted() {
            this.myEcharts2();
        },
        methods: {
            myEcharts2() {
                // 基于准备好的dom，初始化echarts实例
                var myChart2 = this.$echarts.init(document.getElementById('allPie'));
                // 指定图表的配置项和数据
                var option = {
                    title: {
                        text: '周事件总览',
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: " {b},{c} "
                    },
                    graphic: {
                        type: "group",
                        top: "middle",
                        left: "center",
                        height: 80,
                        children: [
                            {
                                type: "text",
                                left: "center",
                                top: "30%",
                                style: {
                                    text: "本周总事件",
                                    textAlign: "center",
                                    textVerticaAlign: "middle",
                                    fill: "#999",
                                    font: "15px 'Helvetica',sans-serif"
                                }
                            },
                            {
                                type: "text",
                                top: "60%",
                                left: "center",
                                position: [0, 10],
                                style: {
                                    text: this.allCount,
                                    textAlign: "center",
                                    textVerticaAlign: "middle",
                                    fill: "#3d383a",
                                    font: "22px 'Helvetica',sans-serif"
                                }
                            }
                        ]
                    },
                    dataset: {
                        source: this.allEventCount
                    },
                    series: [{
                        type: 'pie',
                        radius: ['30%', '50%'],
                        encode: {itemName: 0, value: 1},
                        labelLine: {    //图形外文字线
                            normal: {
                                length: 35,
                                length2: 80
                            }
                        },
                        label: {
                            normal: {
                                formatter: ' {c|{c}}  \n',       //图形外文字上下显示
                                borderWidth: 20,
                                borderRadius: 4,
                                padding: [0, -80],          //文字和图的边距
                                rich: {
                                    c: {                   //value 文字样式
                                        fontSize: 16,
                                        lineHeight: 10,
                                        color: '#4c5052',
                                        align: "center"
                                    }
                                }
                            }
                        },
                    }]
                };

                // 使用刚指定的配置项和数据显示图表。
                myChart2.setOption(option);
            },
            setData(data) {
                console.log(data);
                for (let i = 0; i < 5; i++) {
                    this.allEventCount[i][1] = data[i];
                    this.allCount += data[i];
                }
                this.myEcharts2();
            }
        }
    }
</script>

<style scoped>

</style>