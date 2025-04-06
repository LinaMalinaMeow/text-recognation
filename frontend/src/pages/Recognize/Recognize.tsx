import { Box, Flex} from '@gravity-ui/uikit';
import styles from './Recognize.module.css';
import { useMemo } from 'react';
import { LoadFile } from './LoadFile/LoadFile';
import { observer } from 'mobx-react-lite';
import { RecognizeContextProvider, RecognizeStore } from '../../Stores/Recognize';
import { Results } from './Results/Results';

export const Recognize = observer(() => {
    const Recognize = useMemo(() => new RecognizeStore(), [])

    return (
        <RecognizeContextProvider value={Recognize}>
            <Flex className={styles.root} gap='10'>
                <Box width='50%'>
                    <LoadFile />
                </Box>
                <Box width='50%'>
                    <Results key='results'/>
                </Box>
            </Flex>
        </RecognizeContextProvider>
        
    );
})