<template>
    <div>
        <cli-title class="title"></cli-title>
        <div class="menu">
            <cli-menu page-index="1"></cli-menu>
        </div>
        <div class="center">
            <div v-if="isRouterAlive">
                <el-row>
                    <link href="https://vjs.zencdn.net/7.3.0/video-js.min.css" rel="stylesheet">
                    <script src="https://vjs.zencdn.net/7.3.0/video.min.js"></script>
                    <script src="https://cdn.jsdelivr.net/npm/videojs-flash@2/dist/videojs-flash.min.js"></script>
                    <el-col style="width: 1000px;">
                        <video id="liveVideo" class="video-js" controls autoplay preload="auto" width="960"
                               height="660" data-setup="{}">
                            <source :src="mainSrc" type="rtmp/flv">
                        </video>
                        <div class="text">{{mainSrcName}}</div>
                    </el-col>
                    <el-col style="margin-left:20px; width: 300px;">
                        <el-row>
                            <video id="liveVideo1" class="video-js" controls autoplay muted preload="auto" width="300"
                                   height="200" data-setup="{}">
                                <source :src="Src1" type="rtmp/flv">
                            </video>
                        </el-row>
                        <el-row class="subtext">
                            <el-button type="text" @click="toMain(1)">{{Src1Name}}</el-button>
                        </el-row>
                        <el-row>
                            <video id="liveVideo2" class="video-js" controls autoplay muted preload="auto" width="300"
                                   height="200" data-setup="{}">
                                <source :src="Src2" type="rtmp/flv">
                            </video>
                        </el-row>
                        <el-row class="subtext">
                            <el-button type="text" @click="toMain(2)">{{Src2Name}}</el-button>
                        </el-row>
                        <el-row>
                            <video id="liveVideo3" class="video-js" controls autoplay muted preload="auto" width="300"
                                   height="200" data-setup="{}">
                                <source :src="Src3" type="rtmp/flv">
                            </video>
                        </el-row>
                        <el-row class="subtext">
                            <el-button type="text" @click="toMain(3)">{{Src3Name}}</el-button>
                        </el-row>
                    </el-col>
                </el-row>
            </div>
            <div style="margin-top: 30px"></div>
            <total-num></total-num>
        </div>
    </div>
</template>

<script>
    import CliTitle from "../../components/base/cliTitle";
    import CliMenu from "../../components/base/cliMenu";
    import TotalNum from "../../components/camera/totalNum";

    export default {
        name: "index",
        components: {TotalNum, CliTitle, CliMenu},
        data() {
            return {
                mainSrc: "rtmp://39.97.124.237:1984/wodelive/",
                // mainSrc: 'rtmp://202.69.69.180:443/webcast/bshdlive-pc',
                Src1: "",
                Src2: "",
                Src3: "",
                mainSrcName: "房间",
                Src1Name: "走廊",
                Src2Name: "院子",
                Src3Name: "桌子",
                isRouterAlive: true,
            }
        },
        methods: {
            reload () {
                this.isRouterAlive = false;
                this.$nextTick(() => (this.isRouterAlive = true));
            },
            toMain(num){
                let tempSrc = this.mainSrc;
                let tempName = this.mainSrcName;
                console.log(num);
                switch (num) {
                    case 1:
                        this.mainSrc = this.Src1;
                        this.Src1 = tempSrc;
                        this.mainSrcName = this.Src1Name;
                        this.Src1Name = tempName;
                        break;
                    case 2:
                        this.mainSrc = this.Src2;
                        this.Src2 = tempSrc;
                        this.mainSrcName = this.Src2Name;
                        this.Src2Name = tempName;
                        break;
                    case 3:
                        this.mainSrc = this.Src3;
                        this.Src3 = tempSrc;
                        this.mainSrcName = this.Src2Name;
                        this.Src2Name = tempName;
                        break;
                    default:
                        break;
                }
                this.reload();
            }
        },

    }
</script>

<style scoped>
    @import "../../assets/css/page.css";

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


</style>
