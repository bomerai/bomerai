"use client";

import { useEffect, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FileUpload } from "@/components/ui/file-upload";
import { Cuboid, Calculator } from "lucide-react";
import { Button } from "@/components/ui/button";
import Cookies from "js-cookie";
import { useNotificationContext } from "@/hooks/notification-context";
import Check from "@/components/ui/icons/check";

interface FormData {
  files: File[];
  type: string;
}

export default function BuildingMeasure() {
  const { uuid: buildingDesignUuid } = useParams();
  const searchParams = useSearchParams();
  const [step, setStep] = useState<number>(1);
  const { addNotification } = useNotificationContext();

  const handleNextStep = () => {
    const newStep = step + 1;
    setStep(newStep);

    // Store step in both cookie and URL
    Cookies.set("measureStep", newStep.toString(), { expires: 7 }); // Cookie expires in 7 days

    // Update URL parameters
    const params = new URLSearchParams(window.location.search);
    params.set("step", newStep.toString());
    window.history.replaceState({}, "", `?${params.toString()}`);
  };

  useEffect(() => {
    // Check for step in cookie first
    const cookieStep = Cookies.get("measureStep");
    if (cookieStep) {
      const stepValue = parseInt(cookieStep);
      setStep(stepValue);

      // Ensure URL reflects the cookie value
      const params = new URLSearchParams(window.location.search);
      params.set("step", stepValue.toString());
      window.history.replaceState({}, "", `?${params.toString()}`);
    } else {
      // If no cookie, check URL params
      if (searchParams.get("step")) {
        const urlStep = parseInt(searchParams.get("step") as string);
        setStep(urlStep);
        // Store in cookie for future use
        Cookies.set("measureStep", urlStep.toString(), { expires: 7 });
      } else {
        // Default to step 1 and store in both cookie and URL
        setStep(1);
        Cookies.set("measureStep", "1", { expires: 7 });

        const params = new URLSearchParams(window.location.search);
        params.set("step", "1");
        window.history.replaceState({}, "", `?${params.toString()}`);
      }
    }
  }, [searchParams]);

  const handleSubmit = async ({ files, type }: FormData) => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });
    formData.append("draft_building_design_uuid", buildingDesignUuid as string);
    formData.append("type", type);

    try {
      const resp = await fetch(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${buildingDesignUuid}/upload-files/`,
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
        handleNextStep();
      } else {
        console.error("Erro ao carregar pormenor dos pilares");
      }
    } catch (error) {
      console.error(error);
      addNotification({
        message: "Erro ao iniciar leitura",
        type: "error",
      });
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return <Step1 onSubmit={handleSubmit} />;
      case 2:
        return <Step2 onSubmit={handleSubmit} />;
      case 3:
        return <Step3 onSubmit={handleSubmit} />;
      case 4:
        return <Step4 />;
    }
  };

  return (
    <div className="p-8 space-y-12 bg-white h-screen">
      <div>
        <h1 className="text-2xl font-bold">Leitura de pormenores</h1>
        <p className="text-sm text-muted-foreground">
          Medir uma construção é um processo que consiste em medir as
          características da construção e calcular a quantidade de cada
          componente.
        </p>
      </div>
      {renderStep()}
    </div>
  );
}

// Footings
const Step1 = ({
  onSubmit,
}: {
  onSubmit: (formData: FormData) => Promise<void>;
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleContinue = async () => {
    setIsLoading(true);
    await onSubmit({ files, type: "FOOTING" });
    setIsLoading(false);
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Sapatas
          </CardTitle>
          <CardDescription>
            Faça o upload das imagens dos pormenores das sapatas
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <FileUpload
              onFilesSelected={(files) => setFiles(files)}
              maxFiles={100}
            />
            <Button onClick={handleContinue} disabled={isLoading}>
              {isLoading ? "Aguarde..." : "Continuar"}
            </Button>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Pilares
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Vigas
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Lajes
          </CardTitle>
        </CardHeader>
      </Card>
    </div>
  );
};

// Columns
const Step2 = ({
  onSubmit,
}: {
  onSubmit: (formData: FormData) => Promise<void>;
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleContinue = async () => {
    setIsLoading(true);
    await onSubmit({ files, type: "COLUMN" });
    setIsLoading(false);
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Sapatas
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Pilares
          </CardTitle>
          <CardDescription>
            Faça o upload das imagens dos pormenores dos pilares
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <FileUpload
              onFilesSelected={(files) => setFiles(files)}
              maxFiles={100}
            />
            <Button onClick={handleContinue} disabled={isLoading}>
              {isLoading ? "Aguarde..." : "Continuar"}
            </Button>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Vigas
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Lajes
          </CardTitle>
        </CardHeader>
      </Card>
    </div>
  );
};

// Beams
const Step3 = ({
  onSubmit,
}: {
  onSubmit: (formData: FormData) => Promise<void>;
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleContinue = async () => {
    setIsLoading(true);
    await onSubmit({ files, type: "BEAM" });
    setIsLoading(false);
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Cuboid className="w-4 h-4" /> Sapatas
              </div>
              <div>
                <div className="rounded-full p-1 bg-green-500">
                  <Check className="w-4 h-4 text-white" />
                </div>
              </div>
            </div>
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Cuboid className="w-4 h-4" /> Pilares
              </div>
              <div>
                <div className="rounded-full p-1 bg-green-500">
                  <Check className="w-4 h-4 text-white" />
                </div>
              </div>
            </div>
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Vigas
          </CardTitle>
          <CardDescription>
            Faça o upload das imagens dos pormenores das vigas
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <FileUpload
              onFilesSelected={(files) => setFiles(files)}
              maxFiles={100}
            />
            <Button onClick={handleContinue} disabled={isLoading}>
              {isLoading ? "Aguarde..." : "Continuar"}
            </Button>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Lajes
          </CardTitle>
        </CardHeader>
      </Card>
    </div>
  );
};

const Step4 = () => {
  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Cuboid className="w-4 h-4" /> Sapatas
              </div>
              <div>
                <div className="rounded-full p-1 bg-green-500">
                  <Check className="w-4 h-4 text-white" />
                </div>
              </div>
            </div>
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Cuboid className="w-4 h-4" /> Pilares
              </div>
              <div>
                <div className="rounded-full p-1 bg-green-500">
                  <Check className="w-4 h-4 text-white" />
                </div>
              </div>
            </div>
          </CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Cuboid className="w-4 h-4" /> Vigas
              </div>
              <div>
                <div className="rounded-full p-1 bg-green-500">
                  <Check className="w-4 h-4 text-white" />
                </div>
              </div>
            </div>
          </CardTitle>
        </CardHeader>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold flex items-center gap-2">
            <Calculator className="w-4 h-4" /> Resumo
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <Button>Iniciar leitura</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
