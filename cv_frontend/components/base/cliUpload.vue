<template>
    <div style="display: block;margin-top: 10px">
        <div>
            <div class="filelabel"><p>上传附件:  </p></div>
            <div class="filename" ><p>{{filename}}</p></div>
            <div class="fileinput">
                <a href="javascript:;" class="file">浏览
                    <input type="file" name="" id="upload" @change="Upload" >
                </a>
            </div>

        </div>
    </div>
</template>

<script>
    import PRO from '../../api/API_PRO.js'
    import API from '../../api'
    import Cookies from 'js-cookie'
    import axios from 'axios'
    import { Loading } from 'element-ui'

    export default {
        props:{
            /**
             * 用户申报项目时上传附件 declare  管理员发布通知和项目发布的上传附件：notify
             * 校级管理员导入辅导员：import_instructor
             * */
            urltype: '',
            msg:{}, //传入的其他参数
        },

        data () {
            return {
                config: {
                    headers: {
                        'token': Cookies.get('token'),
                        'Content-Type': 'multipart/form-data'
                    }
                },
                filename:'',
                publicurl:PRO.uploadURL+'common/upload/file',
                peopelurl:PRO.uploadURL+'_paperId/information/import',
                specialurl:PRO.uploadURL+'notify/notify/import',
                import_instructor_url:PRO.baseURL+'_paperId/manage/import-instructor',
                upurl:''

            }
        },
        components: {
        },
        mounted: function () {

        },
        methods: {

            Upload () {

                if(this.urltype === 'notify' || this.urltype === 'zhengji'){
                    this.upurl = this.publicurl
                }else if(this.urltype ==='person'){
                    this.upurl = this.peopelurl
                }else if (this.urltype === 'special'){
                    this.upurl = this.specialurl
                }else if(this.urltype ==='attachment'){
                    this.upurl = this.publicurl
                }



                var file = document.getElementById('upload').files[0]
                let param = new FormData()
                param.append('file',file,file.name)

                if(this.urltype === 'notify'){
                    param.append('asset', 'notify')
                } else if(this.urltype === 'zhengji'){
                    param.append('asset', 'zhengji')
                } else if(this.urltype ==='attachment'){
                    param.append('asset', 'project')
                }

                this.filename =file.name
                const loading = Loading.service({
                    lock: true,
                    text: '文件上传中',
                    spinner: 'el-icon-loading'
                })

                if(this.urltype === 'notify' || this.urltype === 'zhengji'){
                    axios.post(this.upurl, param, this.config)
                        .then(response => {
                            loading.close()
                            if (response.data.code !== 0) {
                                alert('上传失败，请重新上传')
                                console.log(response)
                                alert(response.data.message)
                            } else {
                                this.$emit('notifyurl', {url:response.data.data.url,filename:this.filename})
                                alert('上传成功！')
                            }
                        })

                }
                else if(this.urltype==='person')
                {
                    axios.post(this.upurl, param, this.config)
                        .then(response => {
                            loading.close()
                            if (response.data.code !== 0) {
                                alert('上传失败，请重新上传')
                                console.log(response)
                                alert(response.data.message)
                            } else {
                                //传递给父组件
                                this.$emit('notifyurl', {url: response.data.data.url, filename: this.filename})
                                alert('上传成功！请刷新页面')
                            }
                        })
                }else if(this.urltype==='special')
                {
                    axios.post(this.upurl, param, this.config)
                        .then(response => {
                            loading.close()
                            if (response.data.code !== 0) {
                                alert('上传失败，请重新上传')
                                console.log(response)
                                alert(response.data.message)
                            } else {
                                //传递给父组件
                                this.$emit('notifyurl', {data: response.data.data.data})
                                alert('上传成功！')
                            }
                        })
                }else if(this.urltype==='attachment')
                {
                    axios.post(this.upurl, param, this.config)
                        .then(response => {
                            loading.close()
                            if (response.data.code !== 0) {
                                alert('上传失败，请重新上传')
                                console.log(response)
                                alert(response.data.message)
                            } else {
                                this.$emit('notifyurl', {url:response.data.data.url,filename:this.filename})
                                alert('上传成功！')
                            }
                        })
                }
            }

        }
    }
</script>

<style>
    .file {
        width: 70px;
        position: relative;
        display: inline-block;
        height: 30px;
        background: rgba(87, 173, 202, 0.82);
        padding: 4px 12px;
        overflow: hidden;
        color: #ffffff;
        text-decoration: none;
        text-indent: 0;
        line-height: 20px;
        cursor: pointer;
        font-size: 16px;
    }
    .file input {
        position: absolute;
        font-size: 16px;
        right: 0;
        top: 0;
        height: 30px;
        width: 70px;
        opacity: 0;
        cursor: pointer;
    }
    .file:hover {
        background: #5EBBDA;
        border-color: #5EBBDA;
        text-decoration: none;
    }

    .fileinput{
        float: left;
    }

    .filename {
        float: left;
        margin-left: 5px;
        height: 30px;
        width: 200px;
        background: #ffffff;
        border: 1px solid rgba(87, 173, 202, 0.82);
    }

    .filename p{
        white-space:nowrap;
        text-overflow:ellipsis;
        overflow:hidden;
        width: 100%;
        line-height: 30px;
        max-lines: 1;
        font-size: 16px;
        vertical-align: center;
    }

    .filelabel{
        float: left;
        height: 30px;
    }

    .filelabel p{
        white-space:nowrap;
        text-overflow:ellipsis;
        overflow:hidden;
        line-height: 30px;
        max-lines: 1;
        font-size: 16px;
        color:rgba(87, 173, 202, 0.82) ;
        text-align: center;
    }


</style>
