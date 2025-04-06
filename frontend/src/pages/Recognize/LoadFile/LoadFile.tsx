import { Button, Flex, Icon } from "@gravity-ui/uikit"
import { useCallback, useContext, useState } from "react"
import { RecognizeContext, RecognizeStore } from "../../../Stores/Recognize"
import styles from './LoadFile.module.css';
import { LoadingStatus } from "../../../Stores/fetchResource";
import {Xmark} from '@gravity-ui/icons';
import { observer } from "mobx-react-lite";

export const LoadFile = observer(() => {
    const { 
        setFile, 
        currentFile, 
        recognize,
        loadingStatus,
        result,
        destroy
    } = useContext(RecognizeContext) as RecognizeStore;
    const [image, setImage] = useState<string | null>(null);

    const onChangeInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setImage(URL.createObjectURL(file))
        setFile(file)
    }, [])

    return (
        <Flex gap='4' direction='column'>
            {!currentFile ? 
                <input type='file' onChange={onChangeInput} accept='.jpg' /> : 
                <img src={image as string} className={styles.image} />
            }
            <Flex gap='4'>
                {!Boolean(result) && 
                    <Button
                        view='action'
                        size='l'
                        disabled={loadingStatus === LoadingStatus.pending || !currentFile}
                        onClick={recognize}>
                        Начать обработку
                    </Button>
                }
                {Boolean(currentFile) && 
                    <Button
                        view='action'
                        size='l'
                        onClick={destroy}>
                            <Icon data={Xmark} />
                            Очистить
                    </Button>
                }
            </Flex>
        </Flex>
    )
});