<template>
<header class="mb-auto">
    <div>
      <img class="float-md-start" src="https://item.kakaocdn.net/do/9f6391218e3a68eb052a0e6bdd46e649616b58f7bf017e58d417ccb3283deeb3" width="38" height="38" hspace="10" align=left />
      <h3 class="float-md-start mb-0 fw-bold">BearTeam</h3>
      <nav class="nav nav-masthead justify-content-center float-md-end">
        <router-link v-for="page in pages" :to="page.url" class="nav-link fw-bold py-1 px-0" :class="{active : currentPage.key == page.key}" @click="onFocus($event, page)">{{page.name}}</router-link>
      </nav>
    </div>
</header>
</template>


<script lang="ts">
export default {
    name: 'NavBar',
}
</script>

<script lang="ts" setup>
import { inject } from 'vue';
import { Page } from '/@types';

const pages:{[page:string]:Page} = inject('pages', {});
const currentPage:Page = inject('currentPage', {});
const onFocus:(evt:Event, page:Page)=>void = inject('onFocus', (evt:Event, page:Page) => {});
</script>

<style scoped>
.nav-masthead .nav-link {
  color: rgba(0, 0, 0, .5);
  border-bottom: .25rem solid transparent;
}

.nav-masthead .nav-link:hover,
.nav-masthead .nav-link:focus {
  border-bottom-color: rgba(255, 255, 255, .25);
}

.nav-masthead .nav-link + .nav-link {
  margin-left: 1rem;
}

.nav-masthead .active {
  color: rgba(100, 100, 100, .5);
  border-bottom-color: #fff;
}
</style>