<template>
    <div>
        <link href="https://vjs.zencdn.net/7.3.0/video-js.min.css" rel="stylesheet">
        <script src="https://vjs.zencdn.net/7.3.0/video.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/videojs-flash@2/dist/videojs-flash.min.js"></script>
        <div style="display:flex;justify-content:center;">
            <video id="liveVideo" class="video-js" controls autoplay preload="auto" width="600"
                   height="400" data-setup="{}">
                <source :src="mainSrc" type="rtmp/flv">
            </video>
        </div>
    </div>
</template>

<script>
    export default {
        name: "videoBox",
        data() {
            return {
                mainSrc: "rtmp://39.97.124.237:1984/wodelive/",
            }
        }
    }
</script>

<style scoped>

</style>
