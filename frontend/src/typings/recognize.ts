export interface IIRecognizeResponse { 
    tables: {
        page: number;
        table_info: string[][];
        image_url: string;  
    }[]
};

