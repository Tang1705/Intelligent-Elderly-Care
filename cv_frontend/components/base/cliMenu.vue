<template>
    <div>
        <div style="display:flex;justify-content:center;">
            <img src="../../assets/image/logo.png"
                 style="width: 80%;" alt="">
        </div>

        <!--                background-color="#324157"-->
        <el-menu
                :default-active="pageIndex"
                style="margin-left: 20px"
                background-color="#ffffff"
                text-color="#000000"
                active-text-color="#20a0ff"
                @open="handleOpen"
                @close="handleClose"
                @select="handleSelect">
<!--                background-color="#CCEEFF"-->
<!--                text-color="#003377"-->
<!--                active-text-color="#009FCC">-->
            <el-menu-item index="1">
                <i class="el-icon-menu"></i>
                <span slot="title">监控信息</span>
            </el-menu-item>
            <el-menu-item index="2">
                <i class="el-icon-user"></i>
                <span slot="title">人员管理</span>
            </el-menu-item>
            <el-menu-item index="3">
                <i class="el-icon-document"></i>
                <span slot="title">统计报表</span>
            </el-menu-item>
            <el-menu-item index="4">
                <i class="el-icon-setting"></i>
                <span slot="title">实时事件</span>
            </el-menu-item>
            <el-menu-item index="5">
                <i class="el-icon-camera"></i>
                <span slot="title">机位操控</span>
            </el-menu-item>
        </el-menu>
    </div>
</template>

<script>
    export default {
        name: "cliMenu",
        props:{
            pageIndex:{
                type:String
            }
        },
        data(){
            return{

            }
        },

        methods: {
            handleOpen(key, keyPath) {
                console.log(key, keyPath);
            },
            handleClose(key, keyPath) {
                console.log(key, keyPath);
            },
            handleSelect(key, keyPath) {
                console.log(keyPath);
                switch (keyPath[0]) {
                    case "1":
                        this.$router.push({path: `/camera`});
                        break;
                    case "2":
                        this.$router.push({path: `/personManagement`});
                        break;
                    case "3":
                        this.$router.push({path: `/statistics`});
                        break;
                    case "4":
                        this.$router.push({path: `/event`});
                        break;
                    case "5":
                        this.$router.push({path: `/control`});
                        break;
                    default:
                        break;
                }
            }
        }
    }
</script>

<style scoped>

</style>
