<template style="overflow-y: hidden; overflow-x:hidden">
    <div>
        <!--背景-->
        <div class="back-ground" style="overflow-y: hidden; z-index: -1">
            <img src="../assets/image/background.jpg">
        </div>

        <!--标题-->
        <div class="bd">
            <div style="height: auto;">
                <p style="line-height: 54px; text-align: center;">
                    <span style="font-weight: 400; font-size: 48px; color: rgb(255, 255, 255);">
                        <strong>Elder Care</strong>
                    </span>
                    <span style="font-size: 48px;"><br></span>
                    <span style="font-weight: 400; font-size: 48px; color: rgb(255, 255, 255);">
                        <strong><span class="ub-dynamic">Monitoring System</span></strong>
                    </span>
                </p>
            </div>
        </div>
        <!--按钮-->
        <div style="background-color: transparent">
            <!--登陆-->
            <div style="float: left;margin-left: 33%;">
                <el-button type="primary" @click="login()"
                           style="width: 200%;border: solid 2px #fff;background-color: transparent;letter-spacing:10px;font-size: 18px;font-weight: bold"
                           onmouseover="this.style.backgroundColor='#fff';this.style.color='#161616'"
                           onmouseout="this.style.backgroundColor='transparent';this.style.color='#fff'"
                           round>登录
                </el-button>
            </div>
            <!--注册-->
            <div style="float: right;margin-right: 37%;">
                <el-button type="primary" @click="register()"
                           style="width: 200%;border: solid 2px #fff;background-color: transparent;letter-spacing:10px;;font-size: 18px;font-weight: bold"
                           onmouseover="this.style.backgroundColor='#fff';this.style.color='#161616'"
                           onmouseout="this.style.backgroundColor='transparent';this.style.color='#fff'"
                           round>注册
                </el-button>
            </div>
        </div>
        <!--话-->
        <div style="margin-top:400px">
            <div style="height: auto;">
                <p style="line-height: 50px; text-align: center;">
                    <span style="font-weight: 400; font-size: 32px; color: rgb(43, 43, 43);">
                        <strong><span
                                style="background-color: rgb(255, 255, 255);">Senior Safety is Our First Priority</span></strong>
                    </span>
                </p>
                <p style="line-height: 50px; text-align: center;">
                    <span style="font-weight: 400; font-size: 20px; color: rgb(43, 43, 43);">
                        <span style="background-color: rgb(255, 255, 255);">As an essential service, Elder Care Monitoring System is committed to keeping seniors safe.</span>
                    </span>
                </p>
                <p style="line-height: 50px; text-align: center;">
                    <span style="font-weight: 400; font-size: 20px; color: rgb(43, 43, 43);">
                        <span style="background-color: rgb(255, 255, 255);">We provide comprehensive information analysis for monitoring.</span>
                    </span>
                </p>
            </div>
        </div>

        <div style="margin-top: 50px; display:flex; justify-content:center">
            <img style="max-width: 400px; height: auto;" src="../assets/image/monitor.png">
        </div>

        <div class="footer">
            <div id="info">
                <div id="contact">
                    <h1>Technical Support</h1>
                    <p>xxxxxxxxxxx</p>
                </div>
            </div>
        </div>
        <div style="position: absolute; height: 2rem; bottom: 2rem"></div>
        <login-window ref="login"></login-window>
        <signup-window ref="signup"></signup-window>
    </div>
</template>

<script>
    import upload from '~/components/base/cliUpload.vue'
    import SvgIcon from "../components/SvgIcon/index";
    import SignupWindow from "../components/base/signupWindow";
    import LoginWindow from "../components/base/loginWindow";

    export default {
        components: {
            LoginWindow,
            SignupWindow,
            SvgIcon,
            upload
        },

        data() {
            return {}
        },

        methods: {
            login() {
                this.$refs.login.setVisible()
            },
            register() {
                this.$refs.signup.setVisible()
            }
        }
    }
</script>

<style scoped>
    .back-ground {
        position: absolute;
        left: 0;
        top: 10%;
        width: 100%;
    }

    .back-ground > img {
        width: 100%;
        height: 100%;
    }

    .bd {
        align-items: center;
        margin: 10% auto;
        border-radius: 15px;
    }

    .login-title p {
        color: #b0e36f;
        font-weight: bold;
        font-size: 1.5rem;
    }

    .login-icon img {
        width: 100%;
    }

    .footer{
        margin-top: 50px;
        background: #a2a8a4;
        width: 100%;
        height: 120px;
        display: flex;
        align-items: center;
    }

    #info{
        margin: 0 auto;
        padding: 0 3%;
        text-align: center;
    }

    #contact> h1{
        /*margin-top: 10px;*/
        font-size: 20px;
        margin-bottom: 15px;
        color: rgb(255, 255, 255);
    }

    #contact> p{
        font-size: 14px;
        line-height: 20px;
        color: rgb(227, 227, 227);
    }

</style>

