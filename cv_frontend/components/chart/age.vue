<template>
    <div id="age" style="width: 600px;height:400px;"></div>
</template>

<script>
    import echarts from 'echarts';
    import Vue from 'vue'

    Vue.prototype.$echarts = echarts;

    export default {
        name: "age",
        data() {
            return {
                allEventCount: [['<60岁', 0],
                    ['60~70岁', 0],
                    ['70~80岁', 0],
                    ['80~90岁', 0],
                    ['>90岁', 0],],
                allCount: 0,
            }
        },
        mounted() {
            this.myEcharts2();
        },
        methods: {
            myEcharts2() {
                // 基于准备好的dom，初始化echarts实例
                var myChart2 = this.$echarts.init(document.getElementById('age'));
                // 指定图表的配置项和数据
                var option = {
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
                                    text: "老人总数",
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
                this.allCount = 0;
                this.allEventCount = data.data;
                for (let i = 0; i < 5; i++) {
                    this.allCount += this.allEventCount[i][1];
                }
                this.myEcharts2();
            }
        }
    }
</script>

<style scoped>

</style>