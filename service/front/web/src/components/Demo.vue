<template>
<main class="px-3 text-center">
    <h1>{{video.title}}</h1>
    <div class="embed-responsive embed-responsive-1by1">
        <video autoplay controls preload="none" class=”embed-responsive-item“ poster="public/favicon.svg" style='border: 0.1rem solid #fff; height: 20.0rem; width: 20.0rem;'>
            <source :src="video.url" :type="video.type">
        </video>
    </div>
    <div class="text-start mx-auto mp-auto overflow-scroll" style="border: 0.1rem solid #f00; height: 20.0rem; width: 20.0rem;">
        <span v-for="info in log">{{info}}<br /></span>
    </div>
</main>
</template>

<script lang="ts">
export default {
    name: 'Demo',
}
</script>

<script lang="ts" setup>
import {reactive, ref, Ref, onMounted,} from 'vue';
import {Socket} from '../modules/axios';
import {Result, Video} from '../types';

const socket:Socket = new Socket("http://localhost:8000");

const video:Ref<Video> = ref({title:"", url:"", type:""});
const log:string[] = reactive(["start video..."]);

onMounted(() => {
    socket.run('GET', '/video', (res:Result) => {
        video.value = res.data;
    })
        .then((res:boolean) => {
            if(res == true) {
                console.log("Successfully connecting...\n");
            } else {
                video.value = {
                    title: "default video",
                    url: 'src/assets/video/default.mp4',
                    type: "media/mp4",
                };
            }
        })
        .catch((err) => {
            console.log(err);
        })
});



</script>

<style scoped>

</style>