import { Route, Routes } from 'react-router';
import { Main } from './pages/Main/Main';
import { Recognize } from './pages/Recognize/Recognize';
import { URL_PARTS } from './constants/url';

export const App = () => {
    return (
        <Routes>
            <Route path={URL_PARTS.main} element={<Main />} />
            <Route path={URL_PARTS.recongize} element={<Recognize />} />
        </Routes>
    );
};
