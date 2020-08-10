<template>
    <el-dialog
            title=""
            :visible.sync="centerVisible"
            width="40%"
            center>
        <div style="margin: 20px;"></div>
        <el-steps :active="active" finish-status="success" class="stepCard">
            <el-step title="账号注册"></el-step>
            <el-step title="个人信息"></el-step>
        </el-steps>

        <!--        账号注册-->
        <div v-if="active===0" class="form">
            <div style="margin-left: 30px; margin-right: 50px">
                <el-form :model="form"
                         label-width="120px"
                         label-position="labelPosition"
                         :rules="rules"
                >
                    <el-form-item label="用户名" prop="username">
                        <el-input v-model="form.username"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input v-model="form.password" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="再次输入密码" prop="checkPass">
                        <el-input v-model="form.checkPass" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="身份验证码" prop="verificationID">
                        <el-input v-model="form.verificationID"></el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button style="position:absolute;left: 200px;bottom: 30px" @click="setHide">取 消</el-button>
                <el-button style="position:absolute;right: 200px;bottom: 30px" type="primary"
                           @click="signUp">注册</el-button>
            </span>
            </div>
        </div>

        <!--        个人信息-->
        <div v-if="active===1" class="form">
            <div style="margin-left: 30px; margin-right: 50px">
                <el-form :model="info"
                         label-width="120px"
                         label-position="labelPosition"
                         :rules="rules"
                >
                    <el-form-item label="用户名">
                        <el-input v-model="info.account" disabled="disabled"></el-input>
                    </el-form-item>
                    <el-form-item label="真实姓名" prop="realname">
                        <el-input v-model="info.REAL_NAME"></el-input>
                    </el-form-item>
                    <el-form-item label="性别" prop="sex">
                        <el-select v-model="info.SEX" placeholder="请选择性别" value="">
                            <el-option label="男" value="男"></el-option>
                            <el-option label="女" value="女"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="邮箱">
                        <el-input v-model="info.EMAIL"></el-input>
                    </el-form-item>
                    <el-form-item label="电话">
                        <el-input v-model="info.PHONE"></el-input>
                    </el-form-item>
                    <el-form-item label="移动电话" prop="mobile">
                        <el-input v-model="info.MOBILE"></el-input>
                    </el-form-item>
                    <el-form-item label="说明">
                        <el-input v-model="info.DESCRIPTION"></el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button style="position:absolute;left: 200px;bottom: 30px" @click="setHide">取 消</el-button>
                <el-button style="position:absolute;right: 200px;bottom: 30px" type="primary"
                           @click="setInfo">录 入</el-button>
            </span>
            </div>
        </div>
    </el-dialog>
</template>

<script>
    import POST from "../../api/POST";
    import PUT from "../../api/PUT";
    import Cookies from "js-cookie";

    export default {
        name: "signupWindow",
        data() {
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    // if (this.form.checkPass !== '') {
                    //     this.$refs.form.validateField('checkPass');
                    // }
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
                    verificationID: [
                        {required: true, message: '请输入身份验证码', trigger: 'blur'}
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
                centerVisible: false,
                disabled: true,
                checkPass: '',
                form: {
                    username: '',
                    password: '',
                    checkPass: '',
                    verificationID: '',
                },
                active: 0,
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
        methods: {
            setVisible() {
                this.centerVisible = true;
                console.log('come out')
            },
            setHide() {
                this.centerVisible = false
            },
            signUp() {
                let newForm = {
                    username: this.form.username,
                    password: this.form.password,
                };
                console.log(newForm);
                POST.signUp(newForm).then(res => {
                    if (res.code === 200) {
                        Cookies.set('token', res.token);
                        this.$message({
                            type: 'success',
                            message: '注册成功！请填写个人信息'
                        });
                        this.active = 1;
                        this.info.account = this.form.username;
                    } else {
                        this.$message({
                            type: 'info',
                            message: '注册失败，请稍后再试'
                        });
                    }
                });
            },
            setInfo() {
                this.info.account = this.form.username;
                console.log(this.info);
                PUT.setInfo(this.info).then(res => {
                    if (res.code === 200) {
                        this.$message({
                            type: 'success',
                            message: '个人信息已录入'
                        });
                        let info = {
                            username: this.form.username,
                        };
                        Cookies.set('info', info);
                        this.$router.push({path: `/camera`});
                    } else {
                        this.$message({
                            type: 'info',
                            message: '个人信息录入失败，请稍后再试'
                        });
                    }
                });
            },
        }
    }
</script>

<style scoped>
    .stepCard {
        width: 30%;
        height: 60%;
        position: absolute;
        top: 50px;
        right: 0;
        left: 20px;
        margin: auto;
    }

    .form {
        margin-top: 100px;
        margin-bottom: 80px;
    }
</style>
