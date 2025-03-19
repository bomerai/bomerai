package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/go-chi/chi/v5"
)

func main() {
    // Verify dwg2dxf is available at startup
    if _, err := exec.LookPath("/usr/local/bin/dwg2dxf"); err != nil {
        fmt.Printf("Error: dwg2dxf not found: %v\n", err)
        os.Exit(1)
    }

    // Set up the Chi router
    r := chi.NewRouter()

    // Define a health check endpoint
    r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("OK"))
    })

    // Define the /convert endpoint
    r.Post("/convert", convertHandler)

    // Start the server
    fmt.Println("Server starting on :8080...")
    if err := http.ListenAndServe(":8080", r); err != nil {
        fmt.Printf("Server failed: %v\n", err)
    }
}

func convertHandler(w http.ResponseWriter, r *http.Request) {
    // Parse the multipart form data
    err := r.ParseMultipartForm(32 << 20) // 32 MB max memory
    if err != nil {
        http.Error(w, "Unable to parse form: "+err.Error(), http.StatusBadRequest)
        return
    }

    // Get the file from the form
    file, handler, err := r.FormFile("file")
    if err != nil {
        http.Error(w, "Unable to get file from form: "+err.Error(), http.StatusBadRequest)
        return
    }
    defer file.Close()

    // Validate file extension
    if !strings.EqualFold(filepath.Ext(handler.Filename), ".dwg") {
        http.Error(w, "File must be a .dwg file", http.StatusBadRequest)
        return
    }

    // Create a temporary directory for our files
    tempDir, err := os.MkdirTemp("", "dwg2dxf-*")
    if err != nil {
        http.Error(w, "Unable to create temporary directory: "+err.Error(), http.StatusInternalServerError)
        return
    }
    defer os.RemoveAll(tempDir) // Clean up when done

    // Sanitize filename to avoid spaces or special characters
    safeFilename := strings.ReplaceAll(handler.Filename, " ", "_")
    safeFilename = strings.ReplaceAll(safeFilename, string(os.PathSeparator), "_")

    // Create paths for our files
    tmpDWG := filepath.Join(tempDir, safeFilename)
    tmpDXF := filepath.Join(tempDir, safeFilename[:len(safeFilename)-4]+".dxf")

    // Create the temporary DWG file
    tmpFile, err := os.Create(tmpDWG)
    if err != nil {
        http.Error(w, "Unable to create temporary file: "+err.Error(), http.StatusInternalServerError)
        return
    }

    // Copy the uploaded file to the temporary location
    _, err = io.Copy(tmpFile, file)
    if err != nil {
        tmpFile.Close()
        http.Error(w, "Unable to save uploaded file: "+err.Error(), http.StatusInternalServerError)
        return
    }

    // Close the file to ensure all data is written to disk
    if err := tmpFile.Close(); err != nil {
        http.Error(w, "Unable to close temporary file: "+err.Error(), http.StatusInternalServerError)
        return
    }

    // Log file info for debugging
    fileInfo, err := os.Stat(tmpDWG)
    if err != nil {
        fmt.Printf("Error getting file info: %v\n", err)
    } else {
        fmt.Printf("File size: %d bytes\n", fileInfo.Size())
    }

    // Execute dwg2dxf command
    cmd := exec.Command("/usr/local/bin/dwg2dxf", tmpDWG, "-v2000", "-y", tmpDXF)
    output, err := cmd.CombinedOutput()
    if err != nil {
        fmt.Printf("dwg2dxf error: %v\nOutput: %s\n", err, string(output))
        http.Error(w, "Conversion failed: "+err.Error()+", Output: "+string(output), http.StatusInternalServerError)
        return
    }

    // Check if the output file was created
    if _, err := os.Stat(tmpDXF); os.IsNotExist(err) {
        fmt.Printf("Output file was not created: %v\n", err)
        http.Error(w, "Conversion failed - output file not created", http.StatusInternalServerError)
        return
    }

    // Read the converted DXF file
    dxfFile, err := os.Open(tmpDXF)
    if err != nil {
        http.Error(w, "Unable to open converted file: "+err.Error(), http.StatusInternalServerError)
        return
    }
    defer dxfFile.Close()

    // Set response headers for file download
    w.Header().Set("Content-Disposition", "attachment; filename="+safeFilename[:len(safeFilename)-4]+".dxf")
    w.Header().Set("Content-Type", "application/dxf")

    // Stream the DXF file to the response
    _, err = io.Copy(w, dxfFile)
    if err != nil {
        http.Error(w, "Unable to send file: "+err.Error(), http.StatusInternalServerError)
        return
    }
}