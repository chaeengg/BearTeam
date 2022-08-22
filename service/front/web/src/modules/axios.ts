import {Result} from '/@types'
import { ref, Ref } from 'vue';
import axios from 'axios';
import { AxiosRequestConfig } from 'axios';

export type METHOD = 'GET' | 'POST';

export class Socket {
    private server: string;
    public readonly currentServer: Ref<string>;

    public constructor(server:string) {
        this.server = server;
        this.currentServer = ref(server);
    }
    
    public changeServer(server:string) {
        this.server = server;
    }

    public async run(method: METHOD, url:string, onSucess:(arg0:Result)=>void, onFailed?:()=>void, params?:{string:string}, data?: {string:any},):Promise<boolean> {
        let result:Result = {};
        if(method == 'GET') {
            result = await this.get(this.server + url, params);
        } else if(method == 'POST') {
            result = await this.post(this.server + url, data);
        }
        if(result.code == 200) {
            onSucess(result);
            return true;
        } else {
            console.log(`Communicating Failed...\n`);
            console.log(`code: ${result.code}\n`);
            console.log(`message: ${result.msg}\n`);
            if(onFailed) {
                onFailed();
            }
            return false;
        }
    }

    private async get(url:string, params?: {string: string}, ):Promise<Result> {
        const config:AxiosRequestConfig = {params: params};
        try {
            const res: Response = await axios.get(url, config);
            if(res.status == 200) {
                return {code: res.status, msg:res.statusText, data:res.body};
            } else {
                return {code: res.status, msg:res.statusText};
            }
        }
        catch(err:any) {
            return {code: 600, msg: "Unknown Error", data: err};
        }
    }

    private async post(url:string, data?: {string:any}, ): Promise<Result> {
        try {
            const res: Response = await axios.post(url, data);
            if(res.status == 200) {
                return {code: res.status, msg:res.statusText, data:res.body};
            } else {
                return {code: res.status, msg:res.statusText};
            }
        }
        catch(err:any) {
            return {code: 600, msg: "Unknown Error", data: err};
        }
    }
};