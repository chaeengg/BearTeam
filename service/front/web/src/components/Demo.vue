<template>
<main class="px-3 text-center">
    <!--h1>{{video.title}}</h1-->
    <h1>서비스 시연</h1>
    <!--div class="embed-responsive embed-responsive-1by1">
         <video autoplay muted controls preload="none" class=”embed-responsive-item“ poster="public/favicon.svg" style='border: 0.1rem solid #fff; height: 18.0rem; width: 32.0rem;'>
            <source src="src/assets/Cycling.mp4" type="video/mp4">
        </video>
    </div-->
    <div class="text-center">
        <MyCanvas :radius="radius"/>
        <!--img src="src\assets\profiles\KakaoTalk_20220823_113458238.jpg" class="rounded" alt="..."-->
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

//import {reactive, ref, Ref, onMounted,} from 'vue';
//import {Socket} from '../modules/axios';
//import {Result, Video} from '../types';

//const socket:Socket = new Socket("http://localhost:8000");

</script>

<style scoped>

</style>