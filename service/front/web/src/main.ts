import {createApp} from 'vue/dist/vue.esm-bundler';

import App from '/@/App.vue';
import Home from '/@components/Home.vue'
import Demo from '/@components/Demo.vue';
import Info from '/@components/Info.vue'
import Screen from '/@components/Screen.vue';
import NavBar from '/@components/NavBar.vue';
import Profile from '/@components/Profile.vue';




// import store from '/@store';
import { router } from '/@router';

import '../index.css'
import 'bootstrap/dist/js/bootstrap.esm.min';
import 'bootstrap/dist/css/bootstrap.min.css';

const app = createApp(App);

app.use(router);


app.component(Home.name, Home);
app.component(Demo.name, Demo);
app.component(Info.name, Info);
app.component(Screen.name, Screen);
app.component(NavBar.name, NavBar);
app.component(Profile.name, Profile);

app.mount('#app');