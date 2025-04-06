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

    const tableRows = useMemo(() => responseResult?.table_info?.reduce((acc, row, i) => {
        if (i % 2 === 0) {
            const curHeadings = [...acc.headings, ...row];
            return {...acc, headings: curHeadings}
        }
        const curCells = [...acc.cells, ...row];
        return {...acc, cells: curCells}
    }, {headings: [] as string[], cells: [] as string[]}), [responseResult])

    console.log(tableRows)


    if (loadingStatus === LoadingStatus.pending) {
        return <Spin size="m" />
    }

    if (loadingStatus === LoadingStatus.error) {
        return <Text className={styles.errorText}>Извините. Не удалось распознать изображение :(</Text>
    }

    return (
        <Flex direction='column' gap='4'>
           {Boolean(tableRows?.cells.length || tableRows?.headings.length) && 
            <>
                <div className={styles.table}>
                    <Text className={classNames(styles.fz18, styles.tableUpperText)}>
                        Таблица для внесения баллов участника
                    </Text>
                    <table>
                        <tr>
                            {tableRows?.headings?.map((v, i) => 
                                <td key={i}>{v}</td>)}
                        </tr>
                        <tr>
                            {tableRows?.cells?.map((v, i) => 
                                <td 
                                    key={i} 
                                    contentEditable
                                    suppressContentEditableWarning>
                                        {v}
                                </td>)}
                        </tr>
                    </table> 
                </div>
               
                {/* <Text className={styles.total}>Сумма баллов: 
                {' '}
                <span className={styles.brendColor}>{scoreValue}</span></Text> */}
            </>
           }
        </Flex>
    )
});