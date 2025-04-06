import { Box, Button, Flex, Text } from '@gravity-ui/uikit';
import styles from './Main.module.css';
import { URL_PARTS } from '../../constants/url';
import { useNavigate } from 'react-router';

export const Main = () => {
    const navigate = useNavigate();

    const start = () => navigate(URL_PARTS.recongize);

    return (
        <Flex
            direction='column'
            alignItems='center'
            gap='1'
            className={styles.root}
        >
            <Text variant='header-2'>SchoolOCR</Text>
            <Box className={styles.descBox}>
                <Text variant='subheader-3'>
                    Сервис для распознавания структурированных данных в
                    титульных листах всероссийских проверочных работ с
                    применением нейросетевых методов.
                </Text>
            </Box>
            <Button
                size='xl'
                view='action'
                className={styles.startBtn}
                onClick={start}
            >
                Начать
            </Button>
        </Flex>
    );
};
