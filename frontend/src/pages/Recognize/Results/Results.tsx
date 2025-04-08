import { observer } from "mobx-react-lite"
import { useContext, useMemo } from "react";
import { RecognizeContext, RecognizeStore } from "../../../Stores/Recognize";
import { LoadingStatus } from "../../../Stores/fetchResource";
import { Flex, Spin, Text } from "@gravity-ui/uikit";
import styles from './Results.module.css';
import classNames from "classnames";

export const Results = observer(() => {
    const { 
        result: responseResult, 
        loadingStatus 
    } = useContext(RecognizeContext) as RecognizeStore;

    const tablesData = useMemo(() => responseResult?.tables?.map(({ table_info, image_url }) => {
        const tableData = table_info?.reduce((acc, row, i) => {
            if (i % 2 === 0) {
                const curHeadings = [...acc.headings, ...row];
                return { ...acc, headings: curHeadings };
            }
            const curCells = [...acc.cells, ...row];
            return { ...acc, cells: curCells };
        }, { headings: [] as string[], cells: [] as string[] });

        return { ...tableData, image_url };
    }), [responseResult]);

    console.log(tablesData);

    if (loadingStatus === LoadingStatus.pending) {
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
                            src={`http://localhost:5001/${tableRows.image_url}`} 
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