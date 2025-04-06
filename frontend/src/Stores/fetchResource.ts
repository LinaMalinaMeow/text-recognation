import { action, makeObservable, observable, runInAction } from "mobx";
import type {Method} from 'axios';
import axios from "axios";

interface ICreate {
    method?: Method, 
    body?: Record<string, unknown>
}

export enum LoadingStatus {
    done = 'done',
    pending = 'pending',
    error = 'error'
}

export class fetchResource<T> {
    @observable
    public data: T | null = null
    @observable
    public loadingStatus: LoadingStatus = LoadingStatus.done;

    protected readonly axiosIns = axios.create();

    constructor() {
        makeObservable(this);
    }

    @action.bound
    public async loadData(url: string, {method = 'GET', body}: ICreate) {
        try {
            runInAction(() => this.loadingStatus = LoadingStatus.pending)

            const { data: result } = await axios<T>({
                method, 
                url, 
                data: 
                body, 
                headers: {
                    Authorization: '42d354f4b6e38ff95553137e49f724c9bc429399',
                }})

            runInAction(() => {
                this.data = result
                this.loadingStatus = LoadingStatus.done;
            })
        } catch(err) {
            console.error(err);

            runInAction(() => {
                this.loadingStatus = LoadingStatus.error;
            })
        }   
    }

    @action.bound
    public destroy() {
        runInAction(() => {
            this.data = null;
            this.loadingStatus = LoadingStatus.done;
        })
    }
}