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

import { RawVideo, Log, Result, RawImage, ObjectCategory} from '../types';

const socket: Socket = inject("socket", new Socket(""));
const video: Ref<RawVideo | null> = inject("video", ref(null));
const latestLog: Ref<Log| null> = inject("latestLog", ref(null));
const sleep = inject("sleep");
const receivedImg: Ref<RawImage| null> = inject("receivedImg", ref(null));

const logs: Ref<Log[]> = ref([]);

let inferencedImg: RawImage | null;
watch(receivedImg, (cur:Ref<RawImage|null>, prv:Ref<RawImage|null>) => {
    if(cur.value) {
        inferencedImg = cur.value;
        await socket.run("POST", "/log/prediction", (ret: Result) => {
        latestLog.value = ret.data;
        if(latestLog.value) {
            logs.value.push(latestLog.value);
        }
    }, undefined, undefined, inferencedImg)
    .then((ret:boolean) => {
        if(ret) {
            return await socket.run("POST", `/video/${video.value?.title}/save`, (ret:Result) => {
                if(ret.data == true) {
                    console.log("추론된 이미지가 저장되었습니다.");
                } else {
                    console.log("추론된 이미지가 저장되지 않았습니다.");
                }
            }, undefined, undefined, inferencedImg);
        }
        else {
            return Promise.reject();
        }
    })
    .then((ret:boolean) => {
        if(ret) {
            return await socket.run("POST", `/log/${video.value?.title}/save`, (ret:Result) => {});
        } else {
            return Promise.reject();
        }
    })
    .then((ret:boolean) => {
        if(ret) {
            console.log("추론된 로그가 기록되었습니다.");
        } else {
            console.log("추론된 로그가 저장되지 않았습니다.");
        }
    })
    .catch(() => {
        console.log("추론된 로그가 저장되지 않았습니다.");
    })
    }
});

const format = (log:Log):string => {
    let msg:string = "";

    msg += `[ ${log.recorded} ] `;
    msg += `[ 위험도: `;
    if(log.risk == 0) {
        msg += '낮음';
    } else if(log.risk == 1) {
        msg += '주의';
    } else {
        msg += '위험';
    }
    msg += ' ] ';

    const objCounts:{[key: string]: number} = {"bicycle": 0, "motorcycle": 0, "kickboard": 0};

    for(let obj of log.objects) {
        objCounts[obj.category] += 1;
    }
    msg += `[ 자전거: ${objCounts["bicycle"]}개, 오토바이: ${objCounts["motorcycle"]}, 킥보드: ${objCounts["kickboard"]} ] `;
    
    if(log.risked.length > 0) {
        msg += `[ 위험물:`;
        for(let idx of log.risked) {
            msg += ` ${log.objects[idx]} `;
        }
        msg += '] ';
    }
    return msg;
}
    

            
</script>