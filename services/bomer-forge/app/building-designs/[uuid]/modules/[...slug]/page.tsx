"use client";
import { BuildComponentMeasurer } from "@/components/draft-building-designs/build-components/build-component-measurer";
import { ColumnDesignDrawingFileUploader } from "@/components/draft-building-designs/design-drawings/column-design-drawing-file-uploader";
import { FootingDesignDrawingFileUploader } from "@/components/draft-building-designs/design-drawings/footing-design-drawing-file-uploader";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { CheckCircleIcon } from "@heroicons/react/24/outline";
import {
  ArrowLeft,
  ArrowRight,
  MessageCircleQuestionIcon,
  X,
} from "lucide-react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { useState, useRef, useEffect } from "react";

const STEPS = {
  "1": {
    label: "Leitura do pormenor de sapatas",
    slug: "footing-design",
  },
  "2": {
    label: "Leitura do pormenor de pilares",
    slug: "column-design",
  },
  "3": {
    label: "Leitura do pormenor de vigas",
    slug: "beam-design",
  },
  "4": {
    label: "Leitura do pormenor de lajes",
    slug: "slab-design",
  },
  "5": {
    label: "Leitura do pormenor de Pavimentos",
    slug: "pavement-design",
  },
  "6": {
    label: "Medição",
    slug: "measurement",
  },
};

export default function BuildingDesignModulesPage() {
  const { uuid } = useParams();
  const searchParams = useSearchParams();

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const sidebarRef = useRef<HTMLDivElement>(null);

  const currentStep =
    STEPS[String(searchParams.get("step")) as keyof typeof STEPS];

  const renderStep = () => {
    switch (currentStep?.slug) {
      case "footing-design":
        return (
          <div className="space-y-8">
            <div>
              <h4 className="font-bold mb-4">Instruções</h4>
              <ul className="space-y-2">
                <li className="flex items-center gap-2">
                  <CheckCircleIcon className="w-4 h-4 " />
                  <p className="text-sm">
                    Carregue o pormenor de sapatas{" "}
                    <span className="font-bold">ISOLADAS</span> que encontra no
                    desenho de betão armado.
                  </p>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircleIcon className="w-4 h-4 " />
                  <p className="text-sm">
                    Caso haja pormenores de sapatas continuas ou muro de
                    fundações, estes devem ser carregados no passo de vigas.
                  </p>
                </li>
              </ul>
            </div>
            <FootingDesignDrawingFileUploader
              buildingDesignUuid={uuid as string}
            />
            <div className="flex items-center justify-end">
              <Button>
                Passo 2
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
          </div>
        );
      case "column-design":
        return (
          <ColumnDesignDrawingFileUploader
            buildingDesignUuid={uuid as string}
          />
        );
      case "measurement":
        return <BuildComponentMeasurer />;
    }
  };
  useEffect(() => {
    if (isSidebarOpen) {
      sidebarRef.current?.style.setProperty("width", "500px");
    } else {
      sidebarRef.current?.style.setProperty("width", "40px");
    }
  }, [isSidebarOpen]);

  function getNextStep() {
    const nextStep = Number(searchParams.get("step")) + 1;
    return nextStep;
  }

  function hasNextStep() {
    return Object.keys(STEPS).includes(String(getNextStep()));
  }

  function getPreviousStep() {
    const previousStep = Number(searchParams.get("step")) - 1;
    return previousStep;
  }

  function hasPreviousStep() {
    return Number(searchParams.get("step")) > 1;
  }

  return (
    <div className="p-8 bg-white h-screen relative">
      <div
        className={cn(
          "pr-[500px] space-y-8 transition-all duration-300",
          isSidebarOpen ? "pr-[500px]" : "pr-[40px]"
        )}
      >
        <Link
          href={`/building-designs/${uuid}/modules`}
          className="flex items-center text-sm text-muted-foreground hover:text-anchor"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Voltar
        </Link>
        <div className="">
          <h1 className="font-bold text-2xl">Cálculo de estrutura</h1>
        </div>
        <div className="flex items-center justify-between">
          <div>
            {hasPreviousStep() && (
              <Link
                href={`/building-designs/${uuid}/modules/structure-project/bom?step=${getPreviousStep()}`}
                className="flex items-center text-sm hover:text-anchor text-anchor"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                <span className="font-bold mr-2">
                  Passo {getPreviousStep()}:{" "}
                  {
                    STEPS[String(getPreviousStep()) as keyof typeof STEPS]
                      ?.label
                  }
                </span>
              </Link>
            )}
            <h1 className="text-lg font-bold">
              Step {searchParams.get("step")}: {currentStep?.label}
            </h1>
          </div>
          {hasNextStep() && (
            <Link
              href={`/building-designs/${uuid}/modules/structure-project/bom?step=${getNextStep()}`}
              className="flex items-center hover:text-anchor text-anchor"
            >
              <span className="font-bold mr-2">
                Passo {getNextStep()}:{" "}
                {STEPS[String(getNextStep()) as keyof typeof STEPS]?.label}
              </span>
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
          )}
        </div>
        <div className="">{renderStep()}</div>
      </div>
      <div
        ref={sidebarRef}
        className="fixed transition-all duration-300 top-0 right-0 h-screen w-[40px]"
      >
        <div className="border-l h-full">
          <Button
            variant="ghost"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          >
            {isSidebarOpen ? (
              <X className="w-4 h-4" />
            ) : (
              <MessageCircleQuestionIcon className="w-4 h-4" />
            )}
          </Button>
          <div
            className={cn(
              "p-6 flex flex-col gap-4 transition-all duration-300",
              isSidebarOpen ? "flex" : "hidden"
            )}
          >
            <h4 className="text-lg font-bold">Ajuda</h4>
            <p className="text-sm text-muted-foreground">
              Cálculo de estrutura é um módulo de cálculo que calcula a
              estrutura da construção como pilares, vigas, lajes e betão.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
