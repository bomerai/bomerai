import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { DxfViewer } from "dxf-viewer";

const DXFCanvas = ({ dxfData }) => {
    const viewerRef = useRef(null);
    const dxfContainerRef = useRef(null);
    const [objectUrl, setObjectUrl] = useState(null);

    useEffect(() => {
        if (!dxfData || !dxfContainerRef.current) return;

        // Initialize the DxfViewer
        const viewer = new DxfViewer(dxfContainerRef.current, {
            autoResize: true,
            clearColor: new THREE.Color('#fff'),
            clearAlpha: 1.0,
            canvasAlpha: true,
            sceneOptions: {
                wireframeMesh: true,
                renderText: true,
                textColor: new THREE.Color('#000'),
                textScale: 1.0,
            }
        });

        viewerRef.current = viewer;

        // Create object URL if needed
        let url = dxfData;
        if (dxfData instanceof File || dxfData instanceof Blob) {
            url = URL.createObjectURL(dxfData);
            setObjectUrl(url);
        }

        // Load DXF data - use a simpler approach without custom worker
        viewer.Load({
            url: url,
            progressCbk: (progress) => console.log(`Loading: ${progress}%`)
            // Let dxf-viewer handle the worker creation
        }).catch(error => {
            console.error("Error loading DXF:", error);
        });

        // Cleanup
        return () => {
            if (viewerRef.current) {
                viewerRef.current.Destroy();
                viewerRef.current = null;
            }
            
            // Revoke object URL if we created one
            if (objectUrl) {
                URL.revokeObjectURL(objectUrl);
                setObjectUrl(null);
            }
        };
    }, [dxfData, objectUrl]);

    const handleExport = () => {
        if (!dxfContainerRef.current) return;
        
        // Get the canvas from the container
        const canvas = dxfContainerRef.current.querySelector('canvas');
        if (!canvas) return;
        
        // Create a download link
        const dataUrl = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = 'dxf-export.png';
        link.href = dataUrl;
        link.click();
    };

    return (
        <div>
            <div 
                ref={dxfContainerRef} 
                style={{ width: "100%", height: "100vh", border: "1px solid #ccc" }} 
            />
            <button 
                onClick={handleExport}
                style={{ position: "absolute", bottom: "20px", right: "20px" }}
            >
                Export as Image
            </button>
        </div>
    );
};

export default DXFCanvas;