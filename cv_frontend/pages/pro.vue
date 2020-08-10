<template>
    <div>
        <el-container style="height:100%">
            <el-header class="header-wrapper">
                <div class="logo">
                    <img src="../assets/image/logo.png">
                </div>
                <div class="logoText">
                    <img src="../assets/image/logot1.png">
                </div>
            </el-header>
            <el-container style="height:100%">
                <el-main>
                    <div class="main">
                        <div style="height: 400px">
                            <div class="slide">
                                <el-carousel height="400px">
                                    <el-carousel-item>
                                        <el-image
                                                style="width: 100px; height: 100px"
                                                :src="proInfo[0].pic1"
                                                :fit="fit">
                                        </el-image>
                                    </el-carousel-item>
                                    <el-carousel-item>
                                        <el-image
                                                style="width: 100px; height: 100px"
                                                :src="proInfo[0].pic2"
                                                :fit="fit">
                                        </el-image>
                                    </el-carousel-item>
                                </el-carousel>
                            </div>
                            <div class="rightPart">
                                <div class="buy">
                                    <el-card class="buyCard" shadow="hover">
                                        <el-form :model="proForm" ref="proForm" :label-position="labelPosition">
                                            <el-form-item prop="name" style="margin-top: 10px;margin-bottom: 0px">
                                                <span v-model="proForm.name" style="font-size: 30px">{{proInfo[0].productname}}</span>
                                            </el-form-item>
                                            <el-form-item prop="sname" style="margin-top: 10px;margin-bottom: 0px">
                                                <span v-model="proForm.sname" style="font-size: 20px"><img src="../assets/image/storeIcon.png">{{proInfo[0].storename}}</span>
                                            </el-form-item>
                                            <el-form-item prop="price" style="margin-top: 10px;margin-bottom: 0px">
                                                <div style="height: 100px;background-color: rgba(216,255,238,0.28)">
                                                    <span>价格：</span><span v-model="proForm.price" style="margin-top:20px;font-size: 30px;color: #dd6161">{{proInfo[0].unitprice+'￥'}}</span>
                                                </div>
                                            </el-form-item>
                                            <el-form-item prop="num" style="margin-top: 10px;margin-bottom: 0px">
                                                <el-input-number v-model="proForm.num" :step="1" @change="handleChange" :min="1" :max="100" label="描述文字"></el-input-number>
                                            </el-form-item>
                                            <el-form-item style="margin-top: 20px">
                                                <el-row>
                                                    <el-col>
                                                        <el-button @click="carForm('proForm')" class="carBtn"
                                                                   onmouseover="this.style.backgroundColor='transparent';this.style.color='#494949'"
                                                                   onmouseout="this.style.backgroundColor='#ff7a88';this.style.color='#fff'"
                                                                   round >加入购物车</el-button>
                                                        <el-button @click="buyForm('proForm')" class="buyBtn"
                                                                   onmouseover="this.style.backgroundColor='#ff7a88';this.style.color='#fff'"
                                                                   onmouseout="this.style.backgroundColor='transparent';this.style.color='#494949'"
                                                                   round >立即购买</el-button>
                                                    </el-col>
                                                </el-row>
                                            </el-form-item>
                                        </el-form>
                                    </el-card>
                                </div>
                                <div class="guide">
                                    <el-tabs v-model="activeName" @tab-click="handleClick" :tab-position="tabPosition" style="height: 130px">
                                        <el-tab-pane label=" " name="first"></el-tab-pane>
                                        <el-tab-pane label="产品评价" name="second"></el-tab-pane>
                                        <el-tab-pane label="联系客服" name="third"></el-tab-pane>
                                    </el-tabs>
                                </div>
                                <!--评论抽屉-->
                                <el-drawer
                                        title="商品评论"
                                        :visible.sync="drawer"
                                        size="50%">
                                    <div style="overflow-y:auto;height: 95%">
                                        <el-card v-for="(item,i) in procomment" :key="i" shadow="hover" style="margin-top: 2%">
                                            <div style="float: left">
                                                <div style="float: left">
                                                    <img style="margin-top: 2%" src="../assets/image/icon.png">
                                                </div>
                                                <div style="float: right">
                                                    <h3>{{item.customername}}</h3>
                                                </div>
                                            </div>
                                            <div style="margin-top: 8%">
                                                <el-divider content-position="center">
                                                </el-divider>
                                            </div>
                                            <span style="font-size: 20px">{{item.procomment}}</span>
                                        </el-card>
                                    </div>
                                </el-drawer>
                            </div>
                        </div>
                        <div style="margin-top: 5%;margin-bottom: 5%">
                            <el-divider content-position="center">
                                <div style="float: top;margin-left: 30%">
                                    <img src="../assets/image/icon.png">
                                </div>
                                <div style="float: bottom">
                                    <h2 style="color:rgb(22, 22, 22)">产品详情</h2>
                                </div>
                            </el-divider>
                        </div>
                        <div>
                            <span>{{proInfo[0].productintroduction}}</span>
                        </div>
                    </div>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>
<script>
    import API from "../api"
    import POST from "../api/POST"
    export default {
        data () {
            return {
                fits: 'cover',
                activeName: 'first',
                tabPosition: 'left',
                drawer: false,
                labelPosition: 'left',
                stoName:'',
                proName:'',
                proForm: {
                    name: '',
                    sname: '',
                    price: '',
                    num: ''
                },
                proInfo:[
                    {
                    pic1:'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
                    pic2:'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
                    productname:'333',
                    unitprice:'333',
                    storename:'333',
                    productintroduction: '2313131321312313113131321323213131321312'
                   }
                ],
                procomment:[
                    {
                        customername:'111',
                        procomment:'1234567890'
                    },
                    {
                        customername:'111',
                        procomment:'1234567890'
                    },
                    {
                        customername:'111',
                        procomment:'1234567890'
                    },{
                        customername:'111',
                        procomment:'1234567890'
                    },{
                        customername:'111',
                        procomment:'1234567890'
                    },{
                        customername:'111',
                        procomment:'1234567890'
                    },{
                        customername:'111',
                        procomment:'1234567890'
                    },{
                        customername:'111',
                        procomment:'1234567890'
                    },
                    {
                        customername:'111',
                        procomment:'1234567890'
                    }
                ]
            }
        },
        created () {
            this.getDataList()
        },
        methods: {
            getDataList() {
                var sto = this.$route.query.search
                var pro = this.$route.query.search
                // 将数据放在当前组件的数据内
                this.stoName = sto
                this.proName = index
                let data = {
                    productname: this.proName,
                    storeName: this.stoName
                }
                POST.allProduct(data).then(res => {
                    this.proInfo = res
                    console.log(res)
                })
            },
            async carForm (proForm) {
                let data={
                    saleraccount:11,
                    customeraccount:11,
                    productno:12,
                    quantity:1
                };
                POST.uniproduct(data).then(res=>{
                    console.log(res);
                })
            },
            async buyForm (proForm) {
                let data={
                    saleraccount:11,
                    customeraccount:11,
                    productno:12,
                    quantity:1
                };
                POST.uniproduct(data).then(res=>{
                    console.log(res);
                })
            },
            handleChange(value) {
                console.log(value);
            },
            handleClick(tab, event) {
                console.log(tab, event);
                if(tab.name == 'second'){
                    // 触发‘产品评论’事件
                    this.second();
                }else{
                    // 触发‘联系客服’事件
                    this.third();
                }
            },
            second () {
                this.drawer = true
            },
            third () {
                console.log('联系客服')
            }
        }
    }
</script>
<style scope>
    .header-wrapper {
        width: 100%;
        height: 20%;
        background-color: rgb(22, 22, 22);
        position: fixed;
        overflow-y: hidden;
        z-index: 3;
    }
    .logo {
        float: left;
        margin-top: 5px;
    }
    .logoText {
        float: left;
        margin-top: 10px;
    }
    .main {
        width: 100%;
        position: absolute;
        right: 0;
        left: 0;
        top: 65px;
        margin: auto;
    }
    .slide {
        float: left;
        margin-left: 12%;
        margin-top: 1%;
        width: 30%;
    }
    .rightPart {
        float: right;
        margin-top: 1%;
        width: 55%;
    }
    .buy {
        float: left;
        /*margin-right: 22%;*/
        width: 60%;
    }
    .guide {
        float: right;
        margin-right: 2%;
        width: 30%;
    }
    .el-carousel__item h3 {
        color: #475669;
        font-size: 18px;
        opacity: 0.75;
        line-height: 500px;
        margin: 0;
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }
    .carBtn {
        width: 40%;
        border-radius: 20px;
        margin-bottom: 0px;
        background-color: #ff7a88;
        color: #ffffff;
        border:solid 2px #ff7a88;
    }
    .buyBtn{
        width: 40%;
        border-radius: 20px;
        margin-bottom: 0px;
        background-color: transparent;
        border:solid 2px #ff7a88;
    }
    .el-drawer__body{
        height: 0;
    }

</style>
