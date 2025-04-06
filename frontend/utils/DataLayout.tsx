import { Context as ReactContext, memo, PropsWithChildren, useEffect } from 'react';

export type BaseDataProvider = {
    destroy(): void;
    init(): void;
}

export const createDataLayout = <T extends BaseDataProvider | null>(Context: ReactContext<T>) => {
    return memo<PropsWithChildren<{ value?: T }>>(({ children, value }) => {
        useEffect(() => {
            value?.init();
            return () => void value?.destroy();
        }, [value]);

        if (!value) {
            return <>{children}</>;
        }

        return <Context.Provider value={value}>{children}</Context.Provider>;
    });
};
