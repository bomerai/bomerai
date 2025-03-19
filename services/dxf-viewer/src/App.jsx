import { useState } from "react";
import DXFLoader from "./DXFLoader";
import DXFCanvas from "./DXFCanvas";

const App = () => {
    const [dxfData, setDxfData] = useState(null);

    return (
        <div>
            <h2>DXF Table Selector</h2>
            <DXFLoader onLoad={setDxfData} />
            {dxfData && <DXFCanvas dxfData={dxfData} />}
        </div>
    );
};

export default App;