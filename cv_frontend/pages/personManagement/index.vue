<template>
    <div>
        <cli-title class="title"></cli-title>
        <div class="menu">
            <cli-menu page-index="2"></cli-menu>
        </div>
        <div class="center">
<!--            <el-card>-->
                <el-button class="add_button" type="success" @click="handleAdd">
                    <i class="el-icon-circle-plus"></i>  添加{{typeName}}</el-button>

                <el-tabs v-model="type" type="border-card" @tab-click="handleClick">

                    <el-tab-pane label="老人管理" name="0">
                        <person-list ref="oldList" @getData="getData"></person-list>
                    </el-tab-pane>

                    <el-tab-pane  label="工作人员" name="1">
                        <person-list ref="employList" @getData="getData"></person-list>
                    </el-tab-pane>

                    <el-tab-pane label="义工管理" name="2">
                        <person-list ref="volList" @getData="getData"></person-list>
                    </el-tab-pane>

                </el-tabs>
<!--            </el-card>-->
            <person-detail ref="detail" ></person-detail>
        </div>
    </div>
</template>

<script>
    import CliTitle from "../../components/base/cliTitle";
    import CliMenu from "../../components/base/cliMenu";
    import PersonList from "../../components/personManagement/personList";
    import GET from "../../api";
    import PersonDetail from "../../components/personManagement/personDetail";
    import CliUpload from "../../components/base/cliUpload";
    export default {
        name: "index",
        components: {CliUpload, PersonDetail, PersonList, CliMenu, CliTitle},
        data(){
            return{
                type:'0',
                typeName:'老人',
            }
        },
        methods:{
            handleClick() {
                console.log(this.type);
                if (this.type == '0'){
                    this.typeName= '老人';
                }
                else if (this.type == '1'){
                    this.typeName = '员工';
                }
                else {
                    this.typeName = "义工";
                }
                this.getData()
            },
            getData(){
                if(this.type == '0' ){
                    GET.oldPersonList().then(res=>{
                        this.$refs.oldList.setData(res)
                        this.$refs.oldList.setType(this.type)
                    })
                }
                else if (this.type == '1'){
                    console.log('我佛了')
                    GET.employeeList().then(res=>{
                        this.$refs.employList.setData(res);
                        this.$refs.employList.setType(this.type)
                    })
                }
                else if (this.type == '2'){
                    console.log('我傻了')
                    GET.volunteerList().then(res=>{
                        this.$refs.volList.setData(res);
                        this.$refs.volList.setType(this.type)
                    })
                }
            },
            handleAdd(){
                let data = {
                    type: this.type,
                    edit: true   //可编辑
                }
                this.$refs.detail.setTypeEdit(data)
                this.$refs.detail.setAdd()
                this.$refs.detail.setVisible()
            },
        },
        mounted() {
            this.getData()
        }
    }
</script>

<style scoped>
    @import "../../assets/css/page.css";
    .add_button{
        position: absolute;
        right: 100px;
        margin-right: 140px;
        font-weight: bold;
        /*margin-bottom: 100px;*/
        z-index: 20
    }

</style>
