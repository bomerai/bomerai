import { useState } from "react";
import DxfParser from "dxf-parser";

const DXFLoader = ({ onLoad }) => {
    const [fileName, setFileName] = useState("");

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setFileName(file.name);

        const reader = new FileReader();
        reader.onload = (e) => {
            const parser = new DxfParser();
            try {
                const dxfData = parser.parseSync(e.target.result);
                onLoad(dxfData); // Send DXF data to the renderer
            } catch (error) {
                console.error("Error parsing DXF:", error);
                alert("Failed to parse DXF file.");
            }
        };

        reader.readAsText(file);
    };

    return (
        <div>
            <input type="file" accept=".dxf" onChange={handleFileUpload} />
            {fileName && <p>Loaded: {fileName}</p>}
        </div>
    );
};

export default DXFLoader;