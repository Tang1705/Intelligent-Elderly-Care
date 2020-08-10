<template>
    <div>
        <cli-title class="title"></cli-title>
        <div class="menu">
            <cli-menu page-index="5"></cli-menu>
        </div>
        <div class="center">
            <el-card style="margin-top: 20px">
                <div>
                    <span style="margin-right: 50px">主相机功能</span>
                    <el-radio-group v-model="radio" size="medium" @change="changeFunc">
                        <el-radio-button label="0">无</el-radio-button>
                        <el-radio-button label="1">微笑检测</el-radio-button>
                        <el-radio-button label="2">交互检测</el-radio-button>
                        <el-radio-button label="3">摔倒检测</el-radio-button>
                        <el-radio-button label="4">禁区入侵</el-radio-button>
                    </el-radio-group>
                </div>
            </el-card>
            <el-card style="margin-top: 20px">
                <span style="margin-right: 50px">主相机控制</span>
                <el-button type="primary" plain @click="standard">标定</el-button>
                <el-button type="warning" plain style="margin-left: 30px" @click="reboot">重启</el-button>

            </el-card>
        </div>
    </div>


</template>

<script>
    import CliTitle from "../../components/base/cliTitle";
    import CliMenu from "../../components/base/cliMenu";
    import POST from "../../api/POST";
    import GET from "../../api"

    export default {
        name: "index",
        components: {CliTitle, CliMenu},
        data () {
            return {
                radio: '',
            };
        },
        methods:{
            changeFunc:function(val){
                this.$confirm('确认更改主相机功能?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    // todo 更改相机功能
                    switch (val) {
                        case '0':
                            this.radio = '0';
                            break;
                        case '1':
                            this.radio = '1';
                            break;
                        case '2':
                            this.radio = '2';
                            break;
                        case '3':
                            this.radio = '3';
                            break;
                        case '4':
                            this.radio = '4';
                            break;
                    }
                    let data = {
                        fuc:this.radio
                    }
                    POST.changeFuc(data).then(res=>{
                        this.$message({
                            type: 'success',
                            message: res
                        });
                    })


                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '更改删除'
                    });
                });
            }, reboot(){
                GET.reboot().then(res=>{
                    this.$message({
                        type: 'success',
                        message: res
                    });
                })

            },standard(){
                GET.standard().then(res=> {
                    this.$message({
                        type: 'success',
                        message: res
                    });
                })

            }


        }
    }
</script>

<style scoped>
    @import "../../assets/css/page.css";

</style>
