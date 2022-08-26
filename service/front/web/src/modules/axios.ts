import {Result} from '/@types'
import { ref, Ref } from 'vue';
import axios, { AxiosResponse } from 'axios';
import { AxiosRequestConfig } from 'axios';

export type METHOD = 'GET' | 'POST';

export class Socket {
    private server: string;
    private connected: boolean = false;
    public readonly currentServer: Ref<string>;

    public constructor(server:string) {
        this.server = server;
        this.currentServer = ref(server);
    }
    
    public connectServer(server:string):null {
        this.server = server;
        this.run("GET", '/', (res:Result) => {
            console.log(res.data);
        })
        .then((ret:boolean) => {
            if(ret == false) {
                alert("서버가 연결되지 않았습니다. 주소를 확인해주세요.");
                this.connected = false;
            } else {
                alert("서버가 연결되었습니다. 서비스를 시작합니다.");
                this.connected = true;
            }
        });
        return null
    };

    public isConnected():boolean {
        return this.connected;
    }

    public async run(method: METHOD, url:string, onSuccess:(arg0:Result)=>void, onFailed?:()=>void, params?:any, data?: any,):Promise<boolean> {
        let result:Result = {};
        if(method == 'GET') {
            result = await this.get(this.server + url, params);
        } else if(method == 'POST') {
            result = await this.post(this.server + url, data);
        }
        if(result.code == 200) {
            onSuccess(result);
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

    private async get(url:string, params?: any, ):Promise<Result> {
        const config:AxiosRequestConfig = {params: params};
        try {
            const res: AxiosResponse = await axios.get(url, {params: params});
            if(res.status == 200) {
                return {code: res.status, msg:res.statusText, data:res.data};
            } else {
                return {code: res.status, msg:res.statusText};
            }
        }
        catch(err:any) {
            return {code: 600, msg: "Unknown Error", data: err};
        }
    }

    private async post(url:string, data?: any, ): Promise<Result> {
        try {
            console.log(url)
            const res: AxiosResponse = await axios.post(url=url, data=data, {
                headers: {
                  "Content-Type": `application/json`,
            }
        }
            if(res.status == 200) {
                return {code: res.status, msg:res.statusText, data:res.data};
            } else {
                return {code: res.status, msg:res.statusText};
            }
        }
        catch(err:any) {
            return {code: 600, msg: "Unknown Error", data: err};
        }
    }
};