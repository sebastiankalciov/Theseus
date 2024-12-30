import './styles/App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Home from "./pages/Home";
import AnimationPage from "./pages/AnimationPage";

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/animationPage" element={<AnimationPage/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
