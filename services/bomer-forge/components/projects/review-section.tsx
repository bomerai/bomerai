import Script from "next/script";
import {
  DownloadIcon,
  GitCompareArrows,
  InfoIcon,
  StarsIcon,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import Asterisc from "../ui/icons/asterisc";
import { cn } from "@/lib/utils";
import { useSearchParams, useRouter, useParams } from "next/navigation";
import { useMemo } from "react";

export function ReviewSection() {
  const params = useParams();
  const buildingDesignUuid = params.buildingDesignUuid as string;

  console.log(buildingDesignUuid);
  const router = useRouter();
  const searchParams = useSearchParams();
  const selectedMaterialEvaluationUuid = searchParams.get(
    "selectedMaterialEvaluationUuid"
  );
  const isSelected = useMemo(() => {
    return selectedMaterialEvaluationUuid === "1";
  }, [selectedMaterialEvaluationUuid]);

  return (
    <div className="p-6 space-y-8 w-full">
      <link
        rel="stylesheet"
        href="https://developer.api.autodesk.com/modelderivative/v2/viewers/7.*/style.min.css"
        type="text/css"
      />
      <Script
        src="https://developer.api.autodesk.com/modelderivative/v2/viewers/7.*/viewer3D.min.js"
        strategy="lazyOnload"
      />
      <Script
        src="/js/autodesk-viewer.js"
        strategy="lazyOnload"
        type="module"
      />
      <div id="forgeViewer" />
      <div className="flex flex-col space-y-2">
        <h2 className="font-bold text-xl">Avaliação</h2>
        <div className="flex items-center gap-2">
          <Asterisc className="text-purple-500" />
          <span className="text-sm">
            Abaixo estão os materiais que foram selecionados para o projeto.
            Foram levados em consideração os materiais que foram selecionados
            para o projeto e os materiais que foram selecionados para o projeto.
          </span>
        </div>
      </div>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h4 className="font-bold text-xl">Materiais</h4>
          <Button variant="tertiary">
            <DownloadIcon className="w-4 h-4" /> Download report
          </Button>
        </div>
        <h4 className="font-bold">Fundação</h4>
        <div className="flex flex-col space-y-2">
          <div
            className={cn(
              "flex flex-col gap-2 hover:cursor-pointer hover:bg-gray-50 border rounded p-6 space-y-2 bg-white",
              { "border-primary border-2": isSelected }
            )}
            onClick={() => {
              const searchParams = new URLSearchParams(window.location.search);
              searchParams.set("selectedMaterialEvaluationUuid", "1");
              router.push(
                `${window.location.pathname}?${searchParams.toString()}`
              );
            }}
          >
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-lg">Tijolo</h4>
              <div className="flex gap-2 items-center">
                <Button variant="link" size="sm">
                  <StarsIcon className="w-4 h-4" />
                  Recalcular
                </Button>
                <Button variant="link" size="sm">
                  <GitCompareArrows className="w-4" />
                  Comparar preços
                </Button>
              </div>
            </div>
            <div className="flex flex-row items-center gap-4 border-muted-foreground/10">
              <div className="flex flex-col space-y-1 border-r border-muted-foreground/10 pr-4 flex-1">
                <span className="text-sm">Quantidade total</span>
                <p className="font-bold">1232 unidades</p>
              </div>
              <div className="flex flex-col space-y-1 flex-1">
                <div className="text-sm flex items-center gap-2">
                  Medida <InfoIcon className="w-4 h-4" />
                </div>
                <p className="font-bold">30x15x15cm</p>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-2 hover:cursor-pointer hover:bg-gray-50 border rounded p-6 space-y-2 bg-white">
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-lg">Cimento</h4>
              <div className="flex gap-2 items-center">
                <Button variant="link" size="sm">
                  <StarsIcon className="w-4 h-4" />
                  Recalcular
                </Button>
                <Button variant="link" size="sm">
                  <GitCompareArrows className="w-4" />
                  Comparar preços
                </Button>
              </div>
            </div>
            <div className="flex flex-row items-center gap-4 border-muted-foreground/10">
              <div className="flex flex-col space-y-1 flex-1">
                <span className="text-sm">Quantidade total</span>
                <p className="font-bold">120kg</p>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-2 hover:cursor-pointer hover:bg-gray-50 border rounded p-6 space-y-2 bg-white">
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-lg">Janela</h4>
              <div className="flex gap-2 items-center">
                <Button variant="link" size="sm">
                  <StarsIcon className="w-4 h-4" />
                  Recalcular
                </Button>
                <Button variant="link" size="sm">
                  <GitCompareArrows className="w-4" />
                  Comparar preços
                </Button>
              </div>
            </div>
            <div className="flex flex-row items-center gap-4 border-muted-foreground/10">
              <div className="flex flex-col space-y-1 flex-1">
                <span className="text-sm">Quantidade total</span>
                <p className="font-bold">4 unidades</p>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-2 hover:cursor-pointer hover:bg-gray-50 border rounded p-6 space-y-2 bg-white">
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-lg">Piso PVC</h4>
              <div className="flex gap-2 items-center">
                <Button variant="link" size="sm">
                  <StarsIcon className="w-4 h-4" />
                  Recalcular
                </Button>
                <Button variant="link" size="sm">
                  <GitCompareArrows className="w-4" />
                  Comparar preços
                </Button>
              </div>
            </div>
            <div className="flex flex-row items-center gap-4 border-muted-foreground/10">
              <div className="flex flex-col space-y-1 flex-1">
                <span className="text-sm">Quantidade total</span>
                <p className="font-bold">120m²</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
