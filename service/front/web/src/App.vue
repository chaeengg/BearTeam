<template>
    <nav-bar />
    <router-view />
    <info />
</template>

<script lang="ts">
export default {
  name: 'App',
};
</script>

<script lang="ts" setup>
import { ref, provide, reactive } from 'vue';
import { Page } from '/@types';

const pages: {[page: string]:Page} = reactive({
    'home': {
        key: 0,
        url: '/home',
        name: 'Intro',
    },
    'demo': {
        key: 1,
        url: '/demo',
        name: 'Try',
    },
    'profile': {
        key: 2,
        url: '/profile',
        name: 'Team Info',
    },
});
const currentPage:Page = ref(pages.home);

const onFocus = (evt:Event, page:Page) => {
    // console.log(evt.currentTarget);
    currentPage.value = page;
}

provide('pages', pages);
provide('currentPage', currentPage);
provide('onFocus', onFocus);

</script>
