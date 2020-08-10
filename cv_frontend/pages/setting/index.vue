<template>
    <div>
        <cli-title class="title"></cli-title>
        <div class="menu">
            <cli-menu></cli-menu>
        </div>
        <div class="center">
            <div style="margin-top: 100px">
                <div style="margin-left: 150px; width: 100px; display: inline-block;">
                    <img :size="100" src="../../assets/image/head.png"/>
                </div>
                <div style="margin-left: 50px; width: 400px; display: inline-block;">
                    <el-row>
                        <span class="text">管理员账号</span>
                    </el-row>
                    <div style="margin: 8px 0;"></div>
                    <el-row>
                        <el-input
                                type="text"
                                placeholder="管理员账号"
                                v-model="info.account"
                                maxlength="10"
                                show-word-limit
                                disabled="disabled"
                        >
                        </el-input>
                    </el-row>
                    <div style="margin: 15px 0;"></div>
                </div>
            </div>
            <div style="margin: 50px 300px 100px 100px;">
                <el-card>
                    <el-tabs :tab-position="tabPosition" style="margin-left: 50px; margin-top: 30px; width: 700px;">
                        <el-tab-pane label="账号">
                            <el-form :model="form"
                                     label-width="120px"
                                     label-position="labelPosition"
                                     :rules="rules"
                            >
                                <el-form-item label="原密码" prop="password">
                                    <el-input v-model="form.oldPassword" show-password></el-input>
                                </el-form-item>
                                <el-form-item label="新密码" prop="password">
                                    <el-input v-model="form.password" show-password></el-input>
                                </el-form-item>
                                <el-form-item label="再次输入新密码" prop="checkPass">
                                    <el-input v-model="form.checkPass" show-password></el-input>
                                </el-form-item>
                            </el-form>
                            <el-button style="margin-top: 10px; float: right" type="primary"
                                       @click="changePsw">更新密码</el-button>
                        </el-tab-pane>
                        <el-tab-pane label="通知">
                            <el-form :model="info"
                                     label-width="120px"
                                     label-position="labelPosition"
                                     :rules="rules"
                            >
                                <el-form-item label="邮箱">
                                    <el-input v-model="info.EMAIL"></el-input>
                                </el-form-item>
                                <el-form-item label="电话">
                                    <el-input v-model="info.PHONE"></el-input>
                                </el-form-item>
                                <el-form-item label="移动电话" prop="mobile">
                                    <el-input v-model="info.MOBILE"></el-input>
                                </el-form-item>
                            </el-form>
                            <el-button style="margin-top: 10px; float: right" type="primary"
                                       @click="setInfo">更新通知</el-button>
                        </el-tab-pane>
                        <el-tab-pane label="信息">
                            <el-form :model="info"
                                     label-width="120px"
                                     label-position="labelPosition"
                                     :rules="rules"
                            >
                                <el-form-item label="真实姓名" prop="realname">
                                    <el-input v-model="info.REAL_NAME"></el-input>
                                </el-form-item>
                                <el-form-item label="性别" prop="sex">
                                    <el-select v-model="info.SEX" placeholder="请选择性别" value="">
                                        <el-option label="男" value="男"></el-option>
                                        <el-option label="女" value="女"></el-option>
                                    </el-select>
                                </el-form-item>
                                <el-form-item label="说明">
                                    <el-input v-model="info.DESCRIPTION"></el-input>
                                </el-form-item>
                            </el-form>
                            <el-button style="margin-top: 10px; float: right" type="primary"
                                       @click="setInfo">更新信息</el-button>
                        </el-tab-pane>
                    </el-tabs>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
    import CliTitle from "../../components/base/cliTitle";
    import CliMenu from "../../components/base/cliMenu";
    import PUT from "../../api/PUT"
    import POST from "../../api/POST"
    import Cookies from "js-cookie";

    export default {
        name: "index",
        components: {CliTitle, CliMenu},
        data() {
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    callback();
                }
            };
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.form.password) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return {
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, validator: validatePass, trigger: 'blur'}
                    ],
                    checkPass: [
                        {required: true, validator: validatePass2, trigger: 'blur'}
                    ],
                    realname: [
                        {required: true, message: '请输入真实姓名', trigger: 'blur'}
                    ],
                    sex: [
                        {required: true, message: '请选择性别', trigger: 'blur'}
                    ],
                    mobile: [
                        {required: true, message: '请输入移动电话', trigger: 'blur'},
                        {min: 11, max: 11, message: '长度为11的数字', trigger: 'blur'}
                    ],
                },
                disabled: true,
                tabPosition: 'left',
                tou:'',
                account:{
                    username: '',
                },
                token:{
                    token: '',
                },
                form: {
                    username: '',
                    oldPassword: '',
                    password: '',
                    checkPass: '',
                },
                info: {
                    "account": "",
                    "ORG_ID": null,
                    "CLIENT_ID": null,
                    "REAL_NAME": "",
                    "SEX": "",
                    "EMAIL": "",
                    "PHONE": "",
                    "MOBILE": "",
                    "DESCRIPTION": "",
                    "ISACTIVE": "",
                    "CREATED": null,
                    "CREATEBY": null,
                    "UPDATED": null,
                    "UPDATEBY": null,
                    "REMOVE": "",
                    "DATAFILTER": "",
                    "theme": "",
                    "defaultpage": "",
                    "logoimage": "",
                    "qqopenid": "",
                    "appversion": "",
                    "jsonauth": ""
                },
            }
        },
        mounted(){
            this.account = Cookies.get('info');
            this.account = JSON.parse(this.account);

            this.token = Cookies.get('token');
            this.getData();
        },
        methods: {
            getData(){
                POST.setInfo(this.account).then(res =>{
                    console.log(res);
                    this.info = res;
                })
            },
            changePsw() {
                let newForm = {
                    token: this.token,
                    username: this.account.username,
                    oldPassword: this.form.oldPassword,
                    password: this.form.password,
                };
                console.log(newForm);
                PUT.signUp(newForm).then(res => {
                    if (res.code === 200) {
                        this.$message({
                            type: 'success',
                            message: '修改密码成功'
                        });
                    } else {
                        this.$message({
                            type: 'info',
                            message: '修改密码失败,请检查密码是否正确'
                        });
                    }
                });
            },
            setInfo(){
                PUT.setInfo(this.info).then(res => {
                    if (res.code === 200) {
                        this.$message({
                            type: 'success',
                            message: '个人信息已录入'
                        });
                    } else {
                        this.$message({
                            type: 'info',
                            message: '个人信息录入失败，请稍后再试'
                        });
                    }
                });
            }
        }
    }
</script>

<style scoped>
    @import "../../assets/css/page.css";
</style>
