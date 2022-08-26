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
// import {Socket} from '../modules/axios';

import { RawVideo, Log, Result, RawImage, ObjectCategory} from '../types';

import axios, {AxiosResponse} from 'axios';

// const socket: Socket = inject("socket", new Socket(""));

const server:Ref<string> = inject("server", ref(""));
const connected:Ref<boolean> = inject("connected", ref(false));

const video: Ref<RawVideo | null> = inject("video", ref(null));
const latestLog: Ref<Log| null> = inject("latestLog", ref(null));
// const sleep = inject("sleep");
const receivedImg: Ref<RawImage| null> = inject("receivedImg", ref(null));

const logs: Ref<Log[]> = ref([]);

let inferencedImg: RawImage | null;

watch(receivedImg, async (cur:Ref<RawImage|null>, prv:Ref<RawImage|null>) => {
    if(cur.value) {
        predict(cur.value)
            .then((res) => {
                if(cur.value)
                    return checkpoint(cur.value);
                else
                    return Promise.reject(`현재 이미지가 없습니다, ${cur}`);
            })
            .then((res) => console.log("Checkpoint 생성에 성공했습니다."))
            .catch((reason) => {
                console.log(reason);
            });
    }
});

const predict = async (img:RawImage) => {
    if(server.value.length > 0 && connected.value && video.value){
        axios.post(server.value + `/log/${video.value.title}/prediction`, JSON.stringify(img), {
            headers: { "Content-Type": `application/json`},
        })
        .then((res: AxiosResponse) => {
            latestLog.value = res.data;
            if(latestLog.value) {
                logs.value.push(latestLog.value)
            }
        })
        .catch((reason) => {
            console.log("추론에 실패했습니다.");
            return reason;
        });
    } else {
        return Promise.reject(`Predict: server: ${server.value}\nconnected: ${connected.value}\nvideo: ${video.value}`);
    }
};

const checkpoint = async (img:RawImage) => {
if(server.value.length > 0 && connected.value && video.value){
        axios.post(server.value + `/video/${video.value.title}/save`, JSON.stringify(img), {
            headers: { "Content-Type": `application/json`},
        })
        .then((res: AxiosResponse) => {
            return axios.post(server.value + `/log/${video.value?.title}/save`);
        })
        .catch((reason) => {
            console.log("체크포인트 생성에 실패했습니다..");
            return reason;
        });
    } else {
        return Promise.reject(`Checkpoint: server: ${server.value}\nconnected: ${connected.value}\nvideo: ${video.value}`);
    }
}


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