<template>
    <div class="text-start mx-auto mp-auto overflow-scroll" style="border: 0.01rem solid; height: 10.0rem; width: 40.0rem; font-family: 'LeferiPoint-WhiteObliqueA'; font-size: 1.0rem;">
        "영상을 시작합니다.." <br />
        <span v-for="log in logs">{{format(log)}}<br /></span>
    </div>

    <!--div class="text-start mx-auto mp-auto overflow-scroll" style="border: 0.1rem solid #f00; height: 20.0rem; width: 20.0rem;">
        <span v-for="info in log">{{info}}<br /></span>
    </div-->

</template>

<script lang="ts">
export default {
    "name": "Description",
}
</script>

<script lang="ts" setup>
import {Ref, inject, ref, watch} from 'vue';
import {Socket} from '../modules/axios';

import { RawVideo, Log, Result} from '../types';

const socket: Socket = inject("socket", new Socket(""));
const video: Ref<RawVideo | null> = inject("video", ref(null));
const logs: Ref<Log[]> = ref([]);

// watch(video, (currentVideo:Ref<RawVideo | null>, oldVideo:Ref<RawVideo | null>) => {
//     if(currentVideo) {
//        startLogStreaming();
//     }
// });

// const startLogStreaming = async () => {
//     // console.log("Enter!!");
//     while(true) {
//         if(video.value) {
//             if(socket.isConnected()) {
//                 const ret = await socket.run("GET", `/log/${video.value?.title}/streaming`, (ret:Result) => {
//                     logs.value.push(ret.data);
//                 })
//                 .then((ret:boolean) => {
//                     if(ret) {
//                         // console.log(logs.value);
//                         return true
//                     } else {
//                         console.log("로그를 받아오는데 실패했습니다. 연결을 확인해주세요.");
//                         return false;
//                     }
//                 });
//                 if(ret == false) {
//                     break;
//                 }
//             } else {
//                 console.log("로그를 받아오던 중, 서버와의 연결이 끊겼습니다.");
//                 break;
//             }
//         } else {
//             console.log("로그를 받아오던 중, 서버와의 연결이 끊겼습니다.");
//             break;
//         }
//         setTimeout(() => {}, 3000);
//     }
// };

const format = (log:Log):string => {
    log.objects;
    log.recorded;
    log.risk;
    log.risked;
    msg1 = "날짜: {log.recorded}";
    msg2 = if (log.risk == 0){
            alert("주의하세요!");
    } elif (log.risk == 1){
        alert("조심하세요!");
    } else {
        alert("위험합니다!");
    }

    /* msg2 = if (log.risk ==0):
                print("장애물이 있습니다! 주의하세요!")
            else:
                print("장애물이 접근합니다! 조심하세요!") */
    /*


    */
   
    
    cnt = objects.length
    for(cnt)
    {
        i = 0
        if (log.objects.category == "bicycle"){
                msg3 = alert("자전거");
        } elif (log.objects[i].category == "motocycle"){
                msg3 = alert("오토바이");
        } else {
            msg3 = alert("킥보드");
        }
        }

        if cnt > 1:
            msg3 = alert("와");
        cnt -= 1;
        i = i + 1;
    }

            
</script>