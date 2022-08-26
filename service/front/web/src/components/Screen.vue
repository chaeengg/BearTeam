<template>
    <div class="embed-responsive embed-responsive-1by1">
        <!-- <canvas id="screen" ref="canvas">
        최신 버전의 크롬을 이용해주세요!
        </canvas> -->
        <video src="../../demo/demo01.mp4" autoplay controls></video>
        
    </div>
</template>

<script lang="ts">
export default {
    name: "Screen",
}
</script>

<script lang="ts" setup>
import {ref, reactive, Ref, computed, onMounted, inject, watch} from 'vue';
// import { Socket } from '/@modules/axios';
// import { Socket } from '../modules/axios'

import axios, {AxiosResponse} from 'axios';

import {RawVideo, Path, RawImage, Result, Log} from '../types';

// const socket: Socket = inject("socket", new Socket(""));

const server:Ref<string> = inject("server", ref(""));
const connected:Ref<boolean> = inject("connected", ref(false));

const video: Ref<RawVideo | null> = inject("video", ref(null));
const latestLog: Ref<Log| null> = inject("latestLog", ref(null));
// const sleep: any = inject("sleep");
const receivedImg: Ref<RawImage| null> = inject("receivedImg", ref(null));

const canvas:Ref<HTMLCanvasElement | null> = ref(null);
const ctx:Ref<CanvasRenderingContext2D | null> = ref(null);

const imgData: Ref<ImageData> = ref(new ImageData(1, 1));

onMounted(() => {
    ctx.value = canvas.value?.getContext("2d") as CanvasRenderingContext2D;
});

//계속 이미지 받아오기
let width: number = 1;
let height: number = 1;
watch(video, async (currentVideo:Ref<RawVideo | null>, oldVideo:Ref<RawVideo | null>) => {
    if(video.value != null) {
        width = (video.value?.width) ? video.value?.width : 1;
        height = (video.value?.height) ? video.value?.height : 1;

        imgData.value = ctx.value?.createImageData(width, height) ? ctx.value?.createImageData(width, height) :imgData.value;
        await startVideoStreaming();
    }
});

const startVideoStreaming = async () => {
    // while(true) {
        if(video.value && connected.value && server.value.length != 0) {
            axios.get(server.value + `/video/${video.value.title}/streaming`)
                .then((ret:AxiosResponse) => {
                    
                    receivedImg.value = ret.data;
                    return setImage();
                })
                .then((ret) => {
                    console.log(`Frame: ${video.value?.frames.length}`);
                })
                .catch((reason) => {
                    console.log(reason);
                    alert("영상을 받는데 실패했습니다.");
                });
        } else {
            //화면 정리
            console.log(`video: ${video.value}\nconnected: ${connected.value}\nserver: ${server.value}`);
            imgData.value.data.fill(0);
            ctx.value?.putImageData(imgData.value, 0, 0);
            // break;
        }
    // }
};

const setImage = async () => {
    if(video.value && ctx.value && receivedImg.value) {
        const bytes = Uint8Array.from(atob(receivedImg.value.data), c => c.charCodeAt(0));
        imgData.value.data.set(bytes);
        // ctx.value.putImageData(imgData.value, 0, 0);
        draw(imgData.value)
        return true;
    }  else {
        return Promise.reject(`video: ${video.value}\nctx: ${ctx.value}\nreceivedImg: ${receivedImg.value}`);
    }
};

function draw(imgData:ImageData) {
    if(video.value) {
        const arrayBuffer = new ArrayBuffer(video.value.width * video.value.height * 4);
        const pixels = new Uint8ClampedArray(arrayBuffer);
        for (let y = 0; y < video.value.height; y++) {
        for (let x = 0; x < video.value.width; x++) {
            const i = (y*video.value.width + x) * 4;
            pixels[i  ] = x;   // red
            pixels[i+1] = y;   // green
            pixels[i+2] = 0;   // blue
            pixels[i+3] = 255; // alpha
        }
    }
    }
}

// const imageData = new ImageData(pixels, WIDTH, HEIGHT);
// ctx.putImageData(imageData, 0, 0);
// }

// watch(latestLog, (cur:Ref<Log | null>, prv:Ref<Log | null>) => {
//     if(cur.value != null && ctx.value && canvas.value) {
//         ctx.value.fillStyle = 'red';
//         ctx.value.globalAlpha = 0.5;

//         const riskedPos: ("left" | "center" | "right")[] = [];
//         let pos:number;
//         for(let idx of cur.value.risked) {
//             pos = cur.value.objects[idx].center[0];
//             if(pos < 0.33) {
//                 riskedPos.push("left");
//             } else if(pos < 0.66) {
//                 riskedPos.push("center");
//             } else {
//                 riskedPos.push("right");
//             }
//         }

//         for(let pos of riskedPos) {
//             if(pos == "left") {
//                 ctx.value.fillRect(0, 0, canvas.value.width / 3, canvas.value.height);
//             } else if(pos == "center") {
//                 ctx.value.fillRect(canvas.value.width / 3, 0, canvas.value.width / 3, canvas.value.height);
//             } else {
//                 ctx.value.fillRect(2 * canvas.value.width / 3, 0, canvas.value.width / 3, canvas.value.height);
//             }
//         }
//         ctx.value.globalAlpha = 1.0;
//     }
// })


</script>

<style scoped>
canvas, video {
    border: 0.1rem solid #fff; 
    /* height: 20rem; 
    width: 40rem; */
    height: 13rem;
    width: 8rem;
}
</style>