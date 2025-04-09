import { observer } from "mobx-react-lite"
import { useContext, useMemo, useState, useEffect } from "react";
import { RecognizeContext, RecognizeStore } from "../../../Stores/Recognize";
import { LoadingStatus } from "../../../Stores/fetchResource";
import { Flex, Spin, Text } from "@gravity-ui/uikit";
import styles from './Results.module.css';
import classNames from "classnames";
import io from 'socket.io-client';

const BASE_URL = '89.169.138.153'

export const Results = observer(() => {
    const { 
        loadingStatus 
    } = useContext(RecognizeContext) as RecognizeStore;

    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const socket = useMemo(() => io(`http://${BASE_URL}:5001`), [])

    const tablesData = useMemo(() => results?.map(({ table_info, image_url }) => {
        const tableData = table_info?.reduce((acc, row, i) => {
            if (i % 2 === 0) {
                const curHeadings = [...acc.headings, ...row];
                return { ...acc, headings: curHeadings };
            }
            const curCells = [...acc.cells, ...row];
            return { ...acc, cells: curCells };
        }, { headings: [] as string[], cells: [] as string[] });

        return { ...tableData, image_url };
    }), [results]);

    console.log(tablesData);

    useEffect(() => {
        socket.on('pdf_status', (data) => {
            console.log(data)
            if (data.error) {
                console.error('Ошибка:', data.error);
            } else {
                setIsLoading(data.is_loading);
            }
        })

        socket.on('page_processed', (data) => {
            if (data.error) {
                console.error(`Ошибка на странице ${data.page}:`, data.error);
            } else {
                console.log(`Страница ${data.page} обработана:`, data);
                setResults((prevResults) => [...prevResults, data]);
            }
        });

        return () => {
            socket.off('page_processed');
        };
    }, []);

    if (isLoading) {
        return <Spin size="m" />
    }

    if (loadingStatus === LoadingStatus.error) {
        return <Text className={styles.errorText}>Извините. Не удалось распознать изображение :(</Text>
    }

    return (
        <Flex direction='column' gap='4'>
            {tablesData?.map((tableRows, pageIndex) => (
                Boolean(tableRows?.cells.length || tableRows?.headings.length) && 
                <div key={pageIndex} className={styles.table}>
                    <Text className={classNames(styles.fz18, styles.tableUpperText)}>
                        Таблица для страницы {pageIndex + 1}
                    </Text>
                    {tableRows.image_url && (
                        <img 
                            src={`http://${BASE_URL}:5001/${tableRows.image_url}`} 
                            alt={`Изображение для страницы ${pageIndex + 1}`} 
                            width={500}
                            className={styles.pageImage} 
                        />
                    )}
                    <table>
                        <thead>
                            <tr>
                                {tableRows?.headings?.map((v, i) => 
                                    <th key={i}>{v}</th>)}
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                {tableRows?.cells?.map((v, i) => 
                                    <td 
                                        key={i} 
                                        contentEditable
                                        suppressContentEditableWarning>
                                            {v}
                                    </td>)}
                            </tr>
                        </tbody>
                    </table>
                </div>
            ))}
        </Flex>
    )
});