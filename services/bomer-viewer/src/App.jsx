import React, { useEffect, useRef, useState } from "react";
import { DxfViewer } from "dxf-viewer";
import * as three from "three";
import "./App.css"; // We'll add some basic styles

function App() {
  const viewerRef = useRef(null);
  const dxfContainerRef = useRef(null);
  const [inputFile, setInputFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [selectedEntities, setSelectedEntities] = useState([]);

  const handleEntitySelection = (entities) => {
    setSelectedEntities(entities);
  };

  useEffect(() => {
    console.log('Selected entities:', selectedEntities);
    if (selectedEntities.length > 0) {
      const entity = selectedEntities[0];
      console.log('Selected entity:', entity);
    }
  }, [selectedEntities]);

  // Function to load a DXF file
  const loadDxfFile = (fileOrUrl) => {
    setIsLoading(true);
    setErrorMessage(null);
    
    if (viewerRef.current) {
      // Clear previous drawing if exists
      viewerRef.current.Clear();
      
      viewerRef.current
        .Load({
          url: typeof fileOrUrl === 'string' ? fileOrUrl : URL.createObjectURL(fileOrUrl),
          
          progressCbk: (progress) => console.log(`Loading: ${progress}%`),
          workerFactory: () => new window.Worker(new URL('./Worker.js', import.meta.url), 
          { type: 'module' })
        })
        .then(() => {
          console.log("DXF file loaded successfully");
          setIsLoading(false);
        })
        .catch((error) => {
          console.error("Error loading DXF:", error);
          setErrorMessage(`Failed to load DXF: ${error.message || 'Unknown error'}`);
          setIsLoading(false);
        });
    }
  };

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setInputFile(file);
      loadDxfFile(file);
    }
  };
  
  // Handle URL input
  const handleUrlSubmit = (event) => {
    event.preventDefault();
    const url = event.target.elements.dxfUrl.value.trim();
    if (url) {
      loadDxfFile(url);
    }
  };

  // Initialize viewer
  useEffect(() => {
    // Initialize the DxfViewer when the component mounts
    const viewer = new DxfViewer(dxfContainerRef.current, {
      autoResize: true,
      clearColor: new three.Color('#fff'),
      clearAlpha: 1.0,
      canvasAlpha: true,
      sceneOptions: {
        wireframeMesh: true,
        renderText: true,
        textColor: new three.Color('#000'),
        textScale: 1.0,
      },
      // Add selection options
      selectionOptions: {
        enabled: true,
        enableMultiSelection: true, // Allow selecting multiple entities
        selectionColor: new three.Color('#ff0000'), // Red selection color
        selectionWidth: 2, // Width of selection highlight
      }
    });

    // Set up selection event handlers
    if (viewerRef.current) {
      viewerRef.current.addEventListener('selection', handleEntitySelection);
    }

    viewerRef.current = viewer;

    // Load default sample file if no file is selected
    if (!inputFile) {
      const dxfUrl = "/input.dxf";
      loadDxfFile(dxfUrl);
    }

    // Clean up when the component unmounts
    return () => {
      if (viewerRef.current) {
        viewerRef.current.Destroy();
        viewerRef.current = null;
      }
      // Revoke any object URLs to prevent memory leaks
      if (inputFile) {
        URL.revokeObjectURL(URL.createObjectURL(inputFile));
      }
    };
  }, [inputFile]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>DXF 2D Viewer</h1>
        <div className="controls">
          <div className="file-input">
            <input
              type="file"
              accept=".dxf"
              onChange={handleFileChange}
              id="file-upload"
            />
            <label htmlFor="file-upload" className="custom-file-upload">
              Select DXF File
            </label>
            {inputFile && <span className="filename">{inputFile.name}</span>}
          </div>
          
          <form onSubmit={handleUrlSubmit} className="url-form">
            <input 
              type="text" 
              name="dxfUrl" 
              placeholder="Or enter DXF URL" 
              className="url-input"
            />
            <button type="submit">Load URL</button>
          </form>
        </div>
        
        {isLoading && <div className="loading">Loading DXF file...</div>}
        {errorMessage && <div className="error-message">{errorMessage}</div>}
      </header>
      
      <div
        ref={dxfContainerRef}
        className="dxf-container"
        style={{ width: "100%", height: "80vh", border: "1px solid #ccc" }}
      />
      
      <footer>
        <p>File is processed locally in your browser</p>
      </footer>
    </div>
  );
}

export default App;