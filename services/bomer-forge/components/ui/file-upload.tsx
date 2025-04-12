"use client";

import * as React from "react";
import { useDropzone } from "react-dropzone";
import { cn } from "@/lib/utils";
import { Upload } from "lucide-react";

interface FileUploadProps extends React.HTMLAttributes<HTMLDivElement> {
  onFilesSelected: (files: File[]) => void;
  multiple?: boolean;
  accept?: string;
  maxFiles?: number;
  maxSize?: number;
}

export function FileUpload({
  onFilesSelected,
  multiple = true,
  accept,
  maxFiles,
  maxSize,
  className,
  ...props
}: FileUploadProps) {
  const [files, setFiles] = React.useState<File[]>([]);

  const onDrop = React.useCallback(
    (acceptedFiles: File[]) => {
      setFiles((prev) => {
        const newFiles = [...prev, ...acceptedFiles];
        if (maxFiles) {
          return newFiles.slice(0, maxFiles);
        }
        return newFiles;
      });
      onFilesSelected(acceptedFiles);
    },
    [maxFiles, onFilesSelected]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple,
    accept: accept ? { [accept]: [] } : undefined,
    maxFiles,
    maxSize,
  });

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={cn(
          "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
          isDragActive
            ? "border-primary bg-primary/5"
            : "border-border hover:border-primary/50",
          className
        )}
        {...props}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
        <p className="mt-2 text-sm text-muted-foreground">
          {isDragActive
            ? "Drop the files here"
            : "Drag and drop files here, or click to select files"}
        </p>
        {maxFiles && (
          <p className="mt-1 text-xs text-muted-foreground">
            Maximum {maxFiles} file{maxFiles === 1 ? "" : "s"}
          </p>
        )}
      </div>

      {files.length > 0 && (
        <div className="space-y-2">
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-2 bg-muted rounded"
            >
              <span className="text-sm truncate">{file.name}</span>
              <button
                type="button"
                onClick={() => removeFile(index)}
                className="text-muted-foreground hover:text-foreground"
              >
                Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
