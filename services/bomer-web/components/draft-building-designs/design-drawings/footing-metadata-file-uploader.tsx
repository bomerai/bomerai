import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import Cookies from "js-cookie";
import { Trash2 } from "lucide-react";

interface FootingPlanFileUploaderProps {
  buildingDesignUuid: string;
}

export default function FootingPlanFileUploader({
  buildingDesignUuid,
}: FootingPlanFileUploaderProps) {
  const formSchema = z.object({
    files: z.array(z.instanceof(File)),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      files: [],
    },
  });

  console.log(form.formState.errors);

  const [dragActive, setDragActive] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchCSRFToken = async () => {
      console.log("fetching CSRF token...");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/auth/csrf/`,
        {
          method: "GET",
          credentials: "include",
          mode: "cors",
        }
      );
      const data = await response.json();
      console.log(data);
      Cookies.set("csrftoken", data.csrfToken);
    };

    fetchCSRFToken();
  }, []);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const newFiles = Array.from(e.dataTransfer.files);
      setUploadedFiles((prev) => [...prev, ...newFiles]);
      form.setValue("files", [...uploadedFiles, ...newFiles]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const newFiles = Array.from(e.target.files);
      setUploadedFiles((prev) => [...prev, ...newFiles]);
      form.setValue("files", [...uploadedFiles, ...newFiles]);
    }
  };

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    setIsLoading(true);
    const formData = new FormData();
    data.files.forEach((file) => {
      formData.append("files", file);
    });
    formData.append("building_design_uuid", buildingDesignUuid as string);
    formData.append("design_drawing_type", "STRUCTURAL_DRAWING");
    formData.append(
      "design_drawing_component_metadata_type",
      "FOUNDATION_PLAN"
    );
    formData.append("design_drawing_component_metadata_subtype", "FOOTING");
    const resp = await fetch(
      `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${buildingDesignUuid}/upload-drawing-design/`,
      {
        method: "POST",
        body: formData,
        credentials: "include",
        mode: "cors",
        headers: {
          "X-CSRFToken": Cookies.get("csrftoken") || "",
        },
      }
    );

    if (resp.ok) {
      console.log("Pormenor dos pilares carregado com sucesso");
      window.location.reload();
    } else {
      console.error("Erro ao carregar pormenor dos pilares");
    }
    setIsLoading(false);
  };

  const handleDeleteFile = (file: File) => {
    setUploadedFiles(uploadedFiles.filter((f) => f !== file));
    form.setValue(
      "files",
      uploadedFiles.filter((f) => f !== file)
    );
  };

  return (
    <div className="w-full max-w-md">
      <h4 className="text-lg font-bold">Fundação</h4>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <Label htmlFor="projectDescription">Sapatas</Label>
          <div
            className={`border-2 border-dashed rounded-lg p-6 text-center ${
              dragActive ? "border-blue-500 bg-blue-50" : "border-gray-300"
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="file-upload"
              multiple
              className="hidden"
              onChange={handleFileInput}
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer text-blue-600 hover:text-blue-800"
            >
              <div className="flex flex-col items-center">
                <svg
                  className="w-10 h-10 mb-3 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  ></path>
                </svg>
                <p className="mb-2 text-sm text-gray-500">
                  <span className="font-semibold">Clique para carregar</span> ou
                  arraste e largue
                </p>
                <p className="text-xs text-gray-500">
                  Apenas imagens em formato PNG, JPG ou JPEG são aceitos.
                </p>
              </div>
            </label>
            {uploadedFiles.length > 0 && (
              <div className="mt-4 space-y-2">
                <p className="text-sm text-gray-500">Uploaded files:</p>
                <ul className="text-sm text-gray-600">
                  {uploadedFiles.map((file, index) => (
                    <li key={index} className="flex items-center gap-2">
                      {file.name}
                      <button onClick={() => handleDeleteFile(file)}>
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        <div className="flex justify-end">
          <Button isLoading={isLoading} type="submit" disabled={isLoading}>
            {isLoading ? "Carregando..." : "Carregar"}
          </Button>
        </div>
      </form>
    </div>
  );
}
