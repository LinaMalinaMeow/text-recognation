import { Route, Routes } from 'react-router';
import { Main } from './pages/Main/Main';
import { URL_PARTS } from './constants/url';
import { Recognize } from './pages/Recognize/Recognize';

export const App = () => {
    return (
        <Routes>
            <Route path={URL_PARTS.main} element={<Main />} />
            <Route path={URL_PARTS.recongize} element={<Recognize />} />
        </Routes>
    );
};
