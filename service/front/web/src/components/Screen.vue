<template>
<canvas id="screen" :width="width" :height="height" ref="canvas"></canvas>
</template>

<script lang="ts">
export default {
    name: "Screen",
}
</script>

<script lang="ts" setup>
import {ref, reactive, Ref, computed, onMounted} from 'vue';

const canvas:Ref<HTMLCanvasElement | null> = ref(null);
const ctx:Ref<CanvasRenderingContext2D | null> = ref(null);

onMounted(() => {
    ctx.value = canvas.value?.getContext("2d") as CanvasRenderingContext2D;
});

const img = ref(new Image());
img.value.src = 'src/assets/profiles/chaena.png';
const center:Ref<number[]> = ref([10, 150]);
const width:Ref<number> = ref(640)
const height:Ref<number> = ref(640);

const objName:Ref<string> = ref("bicycle");
const risk: Ref<string> = ref("high");

const path:Ref<"왼쪽"|"중앙"|"오른쪽"> = computed(() => {
    if (center.value[0] + width.value / 2 <= 213) {
        return "왼쪽";
    } else if (center.value[0] + width.value / 2 <= 427) {
        return "중앙";
    } else {
        return "오른쪽"
    }
});

img.value.onload = () => {
    if(ctx.value) {
        console.log(ctx.value)
        ctx.value.drawImage(img.value, 0, 0);
        ctx.value.fillStyle = 'red';
        ctx.value.globalAlpha = 0.5;
        ctx.value.fillRect(center.value[0], center.value[1], width.value, height.value);
        ctx.value.textAlign = "center";
        ctx.value.font = "bold 30px Arial, sans-serif";
        ctx.value.fillText(`${objName} 감지! 위험도: ${risk}`, 250, 100);
    }
}

</script>

<style scoped>
canvas {
    border: 0.1rem solid #fff; 
    height: 20.0rem; 
    width: 20.0rem;
}
</style>