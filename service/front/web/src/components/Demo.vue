<template>
<main class="px-3 text-center">
    <h1>{{video.title}}</h1>
    <div class="embed-responsive embed-responsive-1by1">
         <!-- <video autoplay muted controls preload="none" class=”embed-responsive-item“ poster="public/favicon.svg" style='border: 0.1rem solid #fff; height: 20.0rem; width: 20.0rem;'>
            <source src="src/assets/Cycling.mp4" type="video/mp4">
        </video> -->
        <screen></screen>
    </div>
    <div class="text-start mx-auto mp-auto overflow-scroll" style="border: 0.1rem solid #f00; height: 20.0rem; width: 20.0rem;">
        <span v-for="info in log">{{info}}<br /></span>
    </div>
    
    <!--div class="text-start mx-auto mp-auto overflow-scroll" style="border: 0.1rem solid #f00; height: 20.0rem; width: 20.0rem;">
        <span v-for="info in log">{{info}}<br /></span>
    </div-->
    <div id="direction"></div>
</main>
</template>


<script lang="ts">
export default {
    name: 'Demo',
}

</script>

<script lang="ts" setup>
<<<<<<< HEAD
import MyCanvas from './MyCanvas.vue'
export default {
  components: {
    MyCanvas
  },
  data() {
    return {
      radius: 50
    }
  }
}
=======
import {reactive, ref, Ref, onMounted,} from 'vue';
import {Socket} from '../modules/axios';
import {Result, Video} from '../types';
import Screen from './Screen.vue';

const socket:Socket = new Socket("http://localhost:8000");

const video:Ref<Video> = ref({title:"", url:"", type:""});
const log:string[] = reactive(["start video..."]);

// onMounted(() => {
//     socket.run('GET', '/video', (res:Result) => {
//         video.value = res.data;
//     })
//         .then((res:boolean) => {
//             if(res == true) {
//                 console.log("Successfully connecting...\n");
//             } else {
//                 video.value = {
//                     title: "default video",
//                     url: 'default.mp4',
//                     type: "media/mp4",
//                 };
//             }
//         })
//         .catch((err) => {
//             console.log(err);
//         })
// });
>>>>>>> 56133134a8263eaec965c9708d9314fef6be4be1

//import {reactive, ref, Ref, onMounted,} from 'vue';
//import {Socket} from '../modules/axios';
//import {Result, Video} from '../types';

//const socket:Socket = new Socket("http://localhost:8000");

</script>

<style scoped>

</style>