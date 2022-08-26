<template>
    <div class="embed-responsive embed-responsive-1by1">
        <canvas id="screen" ref="canvas">
        최신 버전의 크롬을 이용해주세요!
        </canvas>
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
import { Socket } from '../modules/axios'

import {RawVideo, Path, RawImage, Result, Log} from '../types';

const socket: Socket = inject("socket", new Socket(""));
const video: Ref<RawVideo | null> = inject("video", ref(null));
const latestLog: Ref<Log| null> = inject("latestLog", ref(null));
const sleep = inject("sleep");

const canvas:Ref<HTMLCanvasElement | null> = ref(null);
const ctx:Ref<CanvasRenderingContext2D | null> = ref(null);

const rawImg:Ref<RawImage | null > = ref(null);
const img = ref(new Image());
const imgData: Ref<ImageData> = ref(new ImageData(1, 1));

onMounted(() => {
    ctx.value = canvas.value?.getContext("2d") as CanvasRenderingContext2D;
});

//계속 이미지 받아오기
let width: number = 1;
let height: number = 1;
watch(video, (currentVideo:Ref<RawVideo | null>, oldVideo:Ref<RawVideo | null>) => {
    if(currentVideo) {
        width = (video.value?.width) ? video.value?.width : 1;
        height = (video.value?.height) ? video.value?.height : 1;

        imgData.value = ctx.value?.createImageData(width, height) ? ctx.value?.createImageData(width, height) :imgData.value;
        startVideoStreaming();
    }
});

const startVideoStreaming = async () => {
    while(true) {
        if(video.value) {
            if(socket.isConnected()) {
                const ret = await socket.run("GET", `/video/${video.value?.title}/streaming`, (ret:Result) => {
                    rawImg.value = ret.data;
                })
                .then((ret:boolean) => {
                    if(ret) {
                        return setImage();
                    } else {
                        return Promise.reject();
                    }
                })
                .then((ret: boolean) => {
                    if(ret) {
                        console.log(`Frame: ${rawImg.value?.id}\n`);
                        return true;
                    } else {
                        console.log("Canvas Context에 접근할 수 없습니다.");
                        return false;
                    }
                })
                .catch(() => {
                    console.log("영상을 받아오는데 실패했습니다. 연결을 확인해주세요.");
                    return false;
                });
                
                if(ret == false) {
                    break;
                }
            } else {
                console.log("이미지를 받아오던 중, 서버와의 연결이 끊겼습니다.");
                break;
            }
        } else {
            console.log("이미지를 받아오던 중, 서버와의 연결이 끊겼습니다.");
            break;
        }
        // await _sleep(5000);
    }

    // 영상이 끝나면 화면도 처음으로!
    imgData.value.data.fill(0);
    ctx.value?.putImageData(imgData.value, 0, 0);
}

let bytes: Uint8Array;
const setImage = async () => {
    if(video.value && ctx.value) {
        bytes = Uint8Array.from(atob(rawImg.value?.data ? rawImg.value?.data : ""), c => c.charCodeAt(0));
        imgData.value.data.set(bytes);
        ctx.value?.putImageData(imgData.value, 0, 0);
        return true;
    }
    // 가장 최신 로그로 이미지에 표시한다.
    return false;
}

watch(latestLog, (cur:Ref<Log | null>, pr:Ref<Log | null>) => {
    if(cur.value != null && ctx.value) {
        ctx.value.fillStyle = 'red';
        ctx.value.globalAlpha = 0.5;

        const riskedPos: ("left" | "center" | "right")[] = [];
        let pos:number;
        for(let idx of cur.value.risked) {
            pos = cur.value.objects[idx].center[0];
            if(pos < 0.5) {

            }
            
        }


        ctx.value.fillRect(center.value[0], center.value[1], bbox_width.value, bbox_height.value);
        ctx.value.globalAlpha = 1.0;
        ctx.value.textAlign = "center";
        ctx.value.font = "bold 30px KOTRA_BOLD-Bold";
        ctx.value.fillText(`${objName} 감지! 위험도: ${risk}`, 300, 300);
    }
})

// img.value.src = 'src/assets/profiles/KakaoTalk_20220823_113458238.jpg';

// const path:Ref<Path> = computed(() => {
//     if()
//     if (center.value[0] + bbox_width.value / 2 <= 213) {
//         return "왼쪽";
//     } else if (center.value[0] + bbox_width.value / 2 <= 427) {
//         return "중앙";
//     } else {
//         return "오른쪽"
//     }
// });

// img.value.onload = () => {
//     if(ctx.value) {
//         ctx.value.drawImage(img.value, 0, 0);
//         ctx.value.fillStyle = 'red';
//         ctx.value.globalAlpha = 0.5;
//         ctx.value.fillRect(center.value[0], center.value[1], bbox_width.value, bbox_height.value);
//         ctx.value.globalAlpha = 1.0;
//         ctx.value.textAlign = "center";
//         ctx.value.font = "bold 30px KOTRA_BOLD-Bold";
//         ctx.value.fillText(`${objName} 감지! 위험도: ${risk}`, 300, 300);
//     }
// }

</script>

<style scoped>
canvas {
    border: 0.1rem solid #fff; 
    height: 20rem; 
    width: 40rem;
}
</style>