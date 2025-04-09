import { action, computed, makeObservable, observable, runInAction } from "mobx";
import { fetchResource } from "./fetchResource";
import { BaseDataProvider, createDataLayout } from "../../utils/DataLayout";
import { createContext } from "react";
import { toBase64 } from "../utils/toBase64";
import { IIRecognizeResponse } from "../typings/recognize";

export class RecognizeStore implements BaseDataProvider {
    private _recognize: fetchResource<IIRecognizeResponse>;
    @observable
    private _currentFile: File | null = null;

    constructor() {
        this._recognize = new fetchResource<IIRecognizeResponse>();

        makeObservable(this);
    }

    @computed
    private get _baseUrl() {
        return 'http://127.0.0.1:5001/recognize';
    }

    @computed
    private get _baseUrlPdf() {
        return 'http://127.0.0.1:5001/recognize-pdf';
    }

    @computed
    public get _baseUrlPdfStream() {
        return 'http://127.0.0.1:5001/recognize-pdf-socket';
    }

    @computed
    public get currentFile() {
        return this._currentFile;
    }

    @action.bound
    public setFile(file: File) {
        this._currentFile = file;
    }

    @action.bound
    public async recognize() {
        if (!this._currentFile) {
            throw Error('no files');
        }

        const image_base64 = await toBase64(this.currentFile as File);

        this._recognize.loadData(this._baseUrl, {
            method: "POST",
            body: {
                image_base64
            }
        })
    }

    @action.bound
    public async recognizePdf() {
        if (!this._currentFile) {
            throw Error('no files');
        }

        const formData = new FormData();
        formData.append('pdf_file', this._currentFile);

        this._recognize.loadData(this._baseUrlPdfStream, {
            method: "POST",
            body: formData
        })
    }

    @computed
    public get result() {
        return this._recognize.data;
    }

    @computed
    public get loadingStatus() {
        return this._recognize.loadingStatus;
    }

    init() {}

    @action.bound
    public destroy(){
        this._recognize.destroy()
        runInAction(() => this._currentFile = null)
    }
}

export const RecognizeContext = createContext<RecognizeStore | null>(null)
export const RecognizeContextProvider = createDataLayout(RecognizeContext);