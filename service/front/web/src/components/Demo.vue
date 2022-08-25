<template>

<div class="container">
    <div class="row">
        <div class="col">
            <button type="button" class="btn btn-success mx-auto my-3" data-bs-toggle="modal" data-bs-target="#exampleModal" style="width:20rem">
                서비스 이용하기
            </button>
        </div>
        <div class="col">
            <div class="input-group mx-auto my-3" style="width:20rem">
                <input type="text" class="form-control" placeholder="영상 이름" aria-label="영상 이름" aria-describedby="basic-addon2" v-model="title"/>
                <div class="input-group-append">
                    <button class="btn btn-secondary" type="button" @click.prevent="startVideo">재생</button>
                </div>
            </div>
        </div>
  </div>
<!-- Button trigger modal -->

</div>
<!-- Modal -->
<div class="modal" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="false">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">서버 주소를 입력해주세요</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="mb-3">
            <input type="url" class="form-control" id="serverAddr" v-model="server" aria-describedby="urlHelp" required aria-required="true" placeholder="http://localhost:9000">
            <div id="urlHelp" class="form-text">서버 주소는 라즈베리 파이 주소입니다</div>
        </div>
        <button type="submit" class="btn btn-primary" data-bs-dismiss="modal" @click="socket.connectServer(server); server=''">Submit</button>
      </div>
    </div>
  </div>
</div>
<main class="px-3 text-center mx-auto" style="width:40rem">
    <div class="container my-1" >
        <div class="row">
            <div class="col">
            </div>
            <div class="col">
                <h5 class = "h5">{{video?.title ? video.title : "우리는 곰돌이팀!"}}</h5>
            </div>
            <div class="col float-bs-right">
                <button type="button" class="btn btn-light" @click.prevent="endVideo">종료</button>
            </div>
        </div>
    </div>
    <screen></screen>
    <description></description>
    
</main>
</template>


<script lang="ts">
export default {
    name: 'Demo',
}

</script>

<script lang="ts" setup>
import {reactive, ref, Ref, onMounted, provide, watch} from 'vue';
import {Socket} from '../modules/axios';
import {Result, RawVideo,} from '../types';
import Screen from './Screen.vue';
import Description from './Description.vue';

const socket:Socket = new Socket("");

const server:Ref<string> = ref("");


// const video:Ref<Video> = ref({title:"", url:"", type:""});
// const log:string[] = reactive(["PM 05:38 - 왼쪽에서 자전거가 감지됩니다. 위험도: 2"]);
const video: Ref<RawVideo | null> = ref(null);


const title:Ref<string> = ref("");
const startVideo = () => {
    if(socket.isConnected()){
        if(title.value.length > 0) {
            socket.run("POST", `/video/${title.value}/start`, (ret:Result) => {
                // console.log(ret);
                video.value = ret.data;
            })
                .then((ret:boolean) => {
                    if(ret) {
                        alert("영상을 재생합니다.");
                        // console.log(video.value);
                    } else {
                        alert("영상을 불러오는데 실패했습니다.");
                    }
                });
        } else {
            alert("영상 제목을 입력해주세요.");
        }
    } else {
        alert("서버가 연결되어 있지 않습니다.");
    }
    title.value = "";
};

const endVideo = () => {
    if(socket.isConnected()) {
        socket.run("POST", `/video/${video.value?.title}/end`, (ret:Result) => {
            video.value = ret.data;
        })
            .then((ret:boolean) => {
                if(ret){
                    alert(`영상이 종료되었습니다.`);
                    video.value = null;
                } else {
                    alert("영상을 종료하는데 실패했습니다.");
                }
            });
    } else {
        alert("서버가 연결되어 있지 않습니다.");
    }
};

provide("socket", socket);
provide("video", video);
</script>

<style scoped>
.h5{
  font-family:"LeferiPoint-WhiteObliqueA";
  font-size:1.5rem;
}
</style>