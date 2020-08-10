<template>
    <el-dialog
            :title="title"
            v-if="centerDetailVisible"
            :visible.sync="centerDetailVisible"
            :before-close="handleClose"
            width="60%"
            center
    >

        <div style="text-align: center" v-if="!add">
            <el-avatar :size="100" :src="tou"></el-avatar>
            <div>
            <cli-avatar v-if="edit" ref="av" :pam="param2" @setHide="setHide" @fresh="fresh"></cli-avatar>
            </div>
        </div>
        <div style="margin: 20px;text-align: center">
        <el-steps :active="active" simple style="width:600px;margin: 0 auto" v-if="add">
            <el-step title="信息填写" icon="el-icon-edit"></el-step>
            <el-step title="人脸录入" icon="el-icon-camera-solid"></el-step>
        </el-steps>
        </div>
<!--        <el-button @click="change" v-if="add&&type==0"> 临时切换器</el-button>-->
            <div v-if="baseInfoVisable">
                <el-form :model="form"
                     label-width="130px"
                     label-position="labelPosition">

                    <el-form-item label="姓名" >
                        <el-input v-model="form.username" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="性别">
                        <el-select  v-model="form.gender" :disabled="!edit">
                            <el-option label="男" value="男"></el-option>
                            <el-option label="女" value="女"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="身份证">
                        <el-input v-model="form.id_card" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="出生日期">
                        <el-date-picker
                                v-model="form.birthday"
                                type="date"
                                placeholder="选择日期"
                                :disabled="!edit"
                                format="yyyy 年 MM 月 dd 日"
                                value-format="yyyy-MM-dd">
                        </el-date-picker>
                    </el-form-item>

                    <el-form-item :label="checkInName">
                        <el-date-picker
                                v-model="form.checkin_date"
                                type="date"
                                placeholder="选择日期"
                                :disabled="!edit"
                                format="yyyy 年 MM 月 dd 日"
                                value-format="yyyy-MM-dd">
                        </el-date-picker>
                    </el-form-item>

                    <el-form-item :label="checkOutName">
                        <el-date-picker
                                v-model="form.checkout_date"
                                type="date"
                                placeholder="选择日期"
                                :disabled="!edit"
                                format="yyyy 年 MM 月 dd 日"
                                value-format="yyyy-MM-dd">
                        </el-date-picker>
                    </el-form-item>


                    <el-form-item label="电话">
                        <el-input v-model="form.phone" :disabled="!edit"></el-input>
                    </el-form-item>

                    <!--            老人特有-->
                <div v-if="type==0">

                    <el-form-item label="房间号" >
                        <el-input v-model="form.room_number" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="第一监护人姓名" >
                        <el-input v-model="form.firstguardian_name" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="与第一监护人关系" >
                        <el-input v-model="form.firstguardian_relationship" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="第一监护人电话" >
                        <el-input v-model="form.firstguardian_phone" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="第一监护人微信" >
                        <el-input v-model="form.firstguardian_wechat" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="第二监护人姓名" >
                        <el-input v-model="form.secondguardian_name" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="与第二监护人关系" >
                        <el-input v-model="form.secondguardian_relationship" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="第二监护人电话" >
                        <el-input v-model="form.secondguardian_phone" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="第二监护人微信" >
                        <el-input v-model="form.secondguardian_wechat" :disabled="!edit"></el-input>
                    </el-form-item>

                    <el-form-item label="健康状态" >
                        <el-radio-group v-model="form.health_state" size="medium" :disabled="!edit">
                            <el-radio-button label="不健康" ></el-radio-button>
                            <el-radio-button label="稍不健康"></el-radio-button>
                            <el-radio-button label="一般健康"></el-radio-button>
                            <el-radio-button label="良好健康"></el-radio-button>
                            <el-radio-button label="非常健康"></el-radio-button>
                        </el-radio-group>
                    </el-form-item>

                </div>

        <!--            这里是大家公有的-->

                    <el-form-item label="描述">
                        <el-input v-model="form.DESCRIPTION" :disabled="!edit"></el-input>
                    </el-form-item>
                    <el-form-item label="是否有效">
                        <el-switch
                                v-model="form.ISACTIVE"
                                active-text="是"
                                inactive-text="否"
                                :disabled="!edit"
                                active-value="1"
                                inactive-value="0">
                        >
                        </el-switch>
                    </el-form-item>
                    <div v-if="!edit">
                    <el-form-item label="创建时间">
                        <el-input v-model="form.CREATED" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="创建人">
                        <el-input v-model="form.CREATEBY" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="更新时间">
                        <el-input v-model="form.UPDATED" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="更新人">
                        <el-input v-model="form.UPDATEBY" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="删除标志">
                        <el-input v-model="form.REMOVE" :disabled="!edit"></el-input>
                    </el-form-item>
                    </div>
                </el-form>
                <div style="margin-bottom: 60px"></div>
          <span slot="footer" class="dialog-footer" v-if="edit">
            <el-button style="position:absolute;left: 260px;bottom: 30px" @click="setHide">取 消</el-button>
            <el-button v-if="!add"  style="position:absolute;right: 260px;bottom: 30px" type="primary" @click="sendEdit">更新</el-button>
            <el-button v-if="add" style="position:absolute;right: 260px;bottom: 30px" type="primary" @click="sendAdd">下一步</el-button>
          </span>
        </div>
    <div style="text-align: center" v-if="takePhoto">
        <video-box></video-box>
        <div style="margin-top: 30px"></div>
        <el-button type="primary" @click="takePhotos">拍照</el-button>


    </div>

    </el-dialog>

</template>

<script>
    import POST from "../../api/POST";
    import PUT from "../../api/PUT";
    import GET from "../../api";
    import Cookies from "js-cookie"
    import pro from "../../pages/pro";
    import API_PRO from "../../api/API_PRO";
    import CliAvatar from "../base/cliAvatar";
    import VideoBox from "./videoBox";
    export default {
        name: "personDetail",
        components: {VideoBox, CliAvatar},
        data(){
            return{
                turnOff:true,
                active: 1,
                baseInfoVisable:true,
                takePhoto:false,
                imgURL:API_PRO.imageURL,
                param2:{
                },
                count:0,
                tou:'',
                info:'',
                title:"",
                type:"",
                phone:'',
                typeName:"",
                edit:false,
                add:false,
                checkInName:'',
                checkOutName:'',
                centerDetailVisible: false,
                form:{id: "",
                    ORG_ID: null,
                    CLIENT_ID: null,
                    username: "",
                    gender: "",
                    phone: "",
                    id_card: "",
                    checkin_date:'',
                    checkout_data:'',
                    birthday: null,
                    room_number:'',
                    firstguardian_name:'',
                    firstguardian_relationship:'',
                    firstguardian_phone:'',
                    firstguardian_wechat:'',
                    secondguardian_name:'',
                    secondguardian_relationship:'',
                    secondguardian_phone:'',
                    secondguardian_wechat:'',
                    health_state:'',
                    DESCRIPTION:'',
                    ISACTIVE: '',
                    CREATED: null,
                    CREATEBY: null,
                    UPDATED: null,
                    UPDATEBY: null,
                    REMOVE:''
                }

            }
        },
        methods:{
            handleClose(done){
                if (this.add){
                    this.$confirm('确认关闭？所有表单和数据将丢失')
                        .then(_ => {
                            done();
                            Object.assign(this.$data, this.$options.data())
                        })
                        .catch(_ => {});
                }
                else {
                    done()
                }

            },
            takePhotos(){
                if (this.count>=7){
                    this.$notify({
                        title: '提示',
                        message: '人脸信息录入完毕',
                    });
                    Object.assign(this.$data, this.$options.data())
                    this.setHide()
                }else {
                    GET.takePhoto().then(res=>{
                        this.$message({
                            type: 'success',
                            message: res+'还需要： '+(7-this.count)+'张照片'
                        });
                        this.count++
                    })
                }

            },
            change(){
                this.active++;
                this.baseInfoVisable = !this.baseInfoVisable;
                this.takePhoto = !this.takePhoto;
            },
            setVisible(){
                this.centerDetailVisible = true
            },
            setHide(){
                this.centerDetailVisible = false
            },
            setData(data){
                this.form = data;
                this.tou = this.imgURL+this.form.profile_photo;
                this.param2['id'] = this.form.id;
            },
            setAdd(){
              this.add = true;
              this.title = '添加'+this.typeName
            },
            fresh(){
                this.$parent.getFuckingData();
            },
            sendEdit(){
                for (let prop in this.form)
                {
                    if (this.form[prop] == null||this.form[prop] == ''){
                        delete this.form[prop]
                    }

                }
                this.form['UPDATED'] = this.getFormatDate()
                this.form['UPDATEBY'] = this.info.username
                let token = Cookies.get('token')
                this.form['token'] = token
                if (this.type == '0'){
                    PUT.oldPersonDetail(this.form).then(res=>{
                        this.$notify({
                            title: '提示',
                            message: '更新成功',
                        });
                        this.edit = false;
                        this.fresh()
                    })
                }
                else if (this.type == '1'){
                    PUT.employeeDetail(this.form).then(res=>{
                        this.$notify({
                            title: '提示',
                            message: '更新成功',
                        });
                        this.edit = false;
                        this.fresh()
                    })
                }
                else {
                    PUT.volunteerDetail(this.form).then(res=>{
                        this.$notify({
                            title: '提示',
                            message: '更新成功',
                        });
                        this.edit = false;
                        this.fresh()
                    })
                }


            },
            entering(data){

                POST.entering(data).then(res=>{
                    this.$notify({
                        title: '提示',
                        message: '相机已启动，请拍照',
                    });
                    this.active++;
                    this.baseInfoVisable = !this.baseInfoVisable;
                    this.takePhoto = !this.takePhoto;
                })
            },
            sendAdd(){
                // let token = Cookies.get('token')
                // this.form['token'] = token
                for (let prop in this.form)
                {
                    if (this.form[prop] == null||this.form[prop] == ''){
                        delete this.form[prop]
                    }
                }
                this.form['CREATED'] = this.getFormatDate();
                this.form['CREATEBY'] = this.info.username;
                if(this.type == '0'){
                    POST.oldPersonList(this.form).then(res=>{
                        this.$notify({
                            title: '提示',
                            message: '信息添加成功，请录入人脸信息',
                        });
                        this.edit = false;
                        this.$parent.getData();
                        let data = {
                            type:this.type,
                            id:res.id
                        }
                        this.entering(data)
                    })
                }
                else if (this.type == '1'){
                    POST.employeeList(this.form).then(res=>{
                        this.$notify({
                            title: '提示',
                            message: '添加成功',
                        });
                        this.edit = false;
                        this.$parent.getData();
                        let data = {
                            type:this.type,
                            id:res.id
                        }
                        this.entering(data);
                    })
                }
                else {
                    POST.volunteerList(this.form).then(res=>{
                        this.$notify({
                            title: '提示',
                            message: '信息添加成功，请录入人脸信息',
                        });
                        this.edit = false;
                        this.$parent.getData();
                        let data = {
                            type:this.type,
                            id:res.id
                        }
                        this.entering(data);
                    })
                }


            },
            setTypeEdit(data){ //设置 种类及
                console.log(data)
                this.type = data.type;
                this.edit = data.edit;
                this.param2['type'] = this.type;

                if (this.type == '0'){
                    this.typeName= '老人';
                    this.checkInName = '入养老院日期';
                    this.checkOutName = '离开养老院日期';
                }
                else if (this.type == '1'){
                    this.typeName = '员工';
                    this.checkInName = '入职日期';
                    this.checkOutName = '离职日期';
                }
                else {
                    this.typeName = "义工";
                    this.checkInName = '访问日期';
                    this.checkOutName = '离开日期';
                }
                console.log(this.typeName)
                if (this.edit == true){
                    this.title = this.typeName+"编辑"
                }else {
                    this.title = this.typeName+"详情"
                }
            },
            getFormatDate(){
                let date = new Date();
                let seperator1 = "-";
                let year = date.getFullYear();
                let month = date.getMonth() + 1;
                let strDate = date.getDate();
                let hour = date.getHours();//得到小时
                let minu = date.getMinutes();//得到分钟
                let sec = date.getSeconds();//得到秒

                if (month < 10) month = "0" + month;
                if (date < 10) date = "0" + date;
                if (hour < 10) hour = "0" + hour;
                if (minu < 10) minu = "0" + minu;
                if (sec < 10) sec = "0" + sec;
                let currentDate = year + seperator1 + month + seperator1 + strDate+'T'+ hour + ":" + minu + ":" + sec;
                return currentDate;
            }


        },
        mounted() {
            this.info = Cookies.get('info');
            this.info = JSON.parse(this.info);

        }
    }
</script>

<style scoped>


</style>
<style>
    .el-input.is-disabled .el-input__inner{
        background-color: white;
        font-weight: bold;
        color: #777b83;
    }

</style>
