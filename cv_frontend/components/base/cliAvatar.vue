<template>
    <div style="display: block;margin-top: 10px">
        <a href="javascript:;" class="file">上传
            <input type="file" name="" id="upload" @change="Upload" >
        </a>
    </div>

</template>

<script>
    import PRO from '../../api/API_PRO.js';
    import axios from 'axios';
    import { Loading } from 'element-ui'
    export default {
        name: "cliAvatar",
        props:{
            pam:{
                type:Object
            }
        },
        data(){
            return{
                config: {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                },
                filename:'',
                type:'',
                id:'',
                url:PRO.uploadURL

            }
        },
        methods:{
            setParam(data){
                this.type = data.type;
                this.id = data.id;

            },
            Upload(){
                var file = document.getElementById('upload').files[0];
                let param = new FormData();
                param.append('file',file,file.name);
                param.append('id',this.pam.id);
                param.append('type',this.pam.type);
                this.filename = file.name
                console.log(this.config)
                console.log(param.get('id'))
                console.log(param.get('type'))
                const loading = Loading.service({
                    lock: true,
                    text: '文件上传中',
                    spinner: 'el-icon-loading'
                })
                axios.post(this.url,param,this.config).then(response=>{
                    loading.close()
                    console.log(response)
                    if(response.status == 200){
                        this.$message({
                            type: 'success',
                            message: '上传成功!'
                        });
                        this.$emit('fresh');
                        this.$emit('setHide');
                    }
                })

            }
        }
    }
</script>

<style scoped>
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

</style>
