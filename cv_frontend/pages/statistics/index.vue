<template>
    <div>
        <cli-title class="title"></cli-title>
        <div class="menu">
            <cli-menu page-index="3"></cli-menu>
        </div>
        <div class="center">
            <div>
                <div style="display:flex;justify-content:center;">
                    <el-card shadow="hover" style="width: 500px; margin-bottom: 30px">
                        <el-row class="text" type="flex" justify="center">
                            <h3>敬老院</h3>
                        </el-row>
                        <el-row type="flex" justify="center">
                            <el-col :span="15" class="card">
                                <el-row><img src="../../assets/image/elder.png" alt=""></el-row>
                                <el-row><span class="subtext">老人数量</span></el-row>
                                <el-row>
                                    <el-button type="text" class="text" @click="showAge">{{elderNum}}</el-button>
                                </el-row>
                            </el-col>
                            <el-col :span="15" class="card">
                                <el-row><img src="../../assets/image/people.png" alt=""></el-row>
                                <el-row><span class="subtext">工作人员数量</span></el-row>
                                <el-row>
                                    <el-button type="text" class="text" :disabled="buttonDisabled">{{staffNum}}</el-button>
                                </el-row>
                            </el-col>
                            <el-col :span="15" class="card">
                                <el-row><img src="../../assets/image/people.png" alt=""></el-row>
                                <el-row><span class="subtext">义工数量</span></el-row>
                                <el-row>
                                    <el-button type="text" class="text" :disabled="buttonDisabled">{{volunteerNum}}</el-button>
                                </el-row>
                            </el-col>
                        </el-row>
                    </el-card>
                </div>
            </div>
            <div class="Echarts">
                <el-row style="margin-left:50px; width: 1200px" type="flex" justify="space-between">
                    <el-col>
                        <all-pie ref="allPieRef"></all-pie>
                    </el-col>
                    <el-col>
                        <all-line ref="allLineRef"></all-line>
                    </el-col>
                </el-row>
                <el-row style="margin-left:50px; width: 1200px" type="flex" justify="space-between">
                    <el-col>
                        <interaction ref="interaction"></interaction>
                    </el-col>
                    <el-col>
                        <smile ref="smile"></smile>
                    </el-col>
                </el-row>
                <el-dialog
                        title="老人年龄分布"
                        :visible.sync="showAgeOption"
                        width="40%"
                        center>
                        <age ref="ageRef"></age>
                    <span slot="footer" class="dialog-footer">
                        <el-button @click="showAgeOption = false">取 消</el-button>
                        <el-button type="primary" @click="showAgeOption = false">确 定</el-button>
                    </span>
                </el-dialog>
            </div>
            <el-button style="position:absolute;right: 180px " type="primary"
                       @click="download">下载总报表</el-button>
            <div style="height: 30px">

            </div>
        </div>
    </div>
</template>

<script>
    import CliTitle from "../../components/base/cliTitle";
    import CliMenu from "../../components/base/cliMenu";
    import allPie from "../../components/chart/allPie";
    import allLine from "../../components/chart/allLine";
    import interaction from "../../components/chart/interaction";
    import smile from "../../components/chart/smile";
    import age from "../../components/chart/age";
    import echarts from 'echarts';
    import Vue from 'vue'
    import GET from "../../api";
    import API_PRO from "../../api/API_PRO";

    Vue.prototype.$echarts = echarts;

    export default {
        name: "index",
        components: {allLine, CliTitle, CliMenu, allPie, interaction, smile, age},
        data() {
            return {
                buttonDisabled: true,
                elderNum: 0,
                staffNum: 0,
                volunteerNum: 0,
                allEventNum: '0',
                showAgeOption: false,
            }
        },
        mounted() {
            this.getPeopleCount();
            this.getPast7Data();
            this.getSmileOld();
            this.getCommunicationOld();
        },
        methods: {
            getPeopleCount: function () {
                let data = {};
                GET.peopleCount(data).then(res => {
                    console.log(res);
                    this.elderNum = res.old;
                    this.staffNum = res.employee;
                    this.volunteerNum = res.volunteer;
                })
            },
            getPast7Data() {
                let data = {};
                GET.eventCount(data).then(res => {
                    console.log(res);
                    this.$refs.allLineRef.setData(res);

                    let allPieData = [0, 0, 0, 0, 0];
                    for (let i = 0; i < 5; i++) {
                        for (let j = 0; j < 7; j++) {
                            allPieData[i] += res[j][i + 1];
                        }
                    }
                    this.$refs.allPieRef.setData(allPieData);
                })
            },
            getSmileOld() {
                let data = {};
                GET.smileOld(data).then(res => {
                    console.log(res);
                    this.$refs.smile.setData(res);
                })
            },
            getCommunicationOld() {
                let data = {};
                GET.communicateOld(data).then(res => {
                    console.log(res);
                    this.$refs.interaction.setData(res);
                })
            },
            getAge() {
                let data = {};
                GET.age(data).then(res => {
                    console.log(res);
                    this.$refs.ageRef.setData(res);
                })
            },
            showAge() {
                this.showAgeOption = true;
                this.getAge();
            },
            download() {
                window.open(API_PRO.baseURL+'statistics/excel')

            }
        }
    }
</script>

<style scoped>
    @import "../../assets/css/page.css";

    .charts {
        width: 600px;
        height: 400px;
        margin-left: 10px;
        margin-right: 10px;
        margin-bottom: 30px;
    }

    .text {
        font-size: 20px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .subtext {
        font-size: 16px;
        text-align: center;
    }

    .card {
        text-align: center;
        margin-top: 20px;
        width: 250px;
    }
</style>
