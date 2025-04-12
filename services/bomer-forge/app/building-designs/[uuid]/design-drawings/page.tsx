"use client";

import {
  ArrowUpRight,
  ChevronRight,
  InfoIcon,
  PlusIcon,
  SparklesIcon,
} from "lucide-react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import FootingPlanFileUploader from "@/components/draft-building-designs/design-drawings/footing-design-drawing-file-uploader";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { useQuery } from "@tanstack/react-query";
import { DesignDrawing } from "@/lib/rest-types";
import { FootingComponentCard } from "@/components/draft-building-designs/build-components/build-component/footing-component-card";
import ColumnMetadataFileUploader from "@/components/draft-building-designs/design-drawings/column-design-drawing-file-uploader";
import ColumnMetadataCardInfo from "@/components/draft-building-designs/design-drawings/column-metadata-card-info";
import FootingMetadataSidebar from "@/components/draft-building-designs/build-components/build-component/footing-component-sidebar";
import ColumnMetadataSidebar from "@/components/draft-building-designs/build-components/build-component/column-component-sidebar";
import DraftBuildingDesignStructuralDrawingUploader from "@/components/draft-building-designs/draft-building-design-structural-drawing-uploader";

const getDesignDrawings = async (
  buildingDesignUuid: string
): Promise<DesignDrawing[]> => {
  const resp = await fetch(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${buildingDesignUuid}/design-drawings/`,
    {
      method: "GET",
      credentials: "include",
      mode: "cors",
    }
  );
  return resp.json();
};

export default function DesignDrawingsPage() {
  const { uuid: buildingDesignUuid } = useParams();

  const searchParams = useSearchParams();
  const tab = searchParams.get("tab");
  const drawingComponentFootingUuid = searchParams.get(
    "drawingComponentFootingUuid"
  );
  const drawingComponentColumnUuid = searchParams.get(
    "drawingComponentColumnUuid"
  );

  const { data: designDrawings } = useQuery({
    queryKey: ["design-drawings", buildingDesignUuid],
    queryFn: () => getDesignDrawings(buildingDesignUuid as string),
  });

  const structuralDesignDrawings = designDrawings?.filter(
    (designDrawing) => designDrawing.type === "STRUCTURAL_DRAWING"
  );

  const footingDesignDrawingPlans = structuralDesignDrawings?.flatMap(
    (designDrawing) =>
      designDrawing.design_drawing_components_metadata.filter(
        (designDrawingComponentMetadata) =>
          designDrawingComponentMetadata.subtype === "FOOTING"
      )
  );

  const columnDesignDrawingPlans = structuralDesignDrawings?.flatMap(
    (designDrawing) =>
      designDrawing.design_drawing_components_metadata.filter(
        (designDrawingComponentMetadata) =>
          designDrawingComponentMetadata.subtype === "COLUMN"
      )
  );

  return (
    <div className="flex flex-col flex-grow relative overflow-y-auto h-screen">
      {/* page header */}
      <div className="flex items-center justify-between px-8 py-4 border-b h-14">
        <nav className="font-medium text-xl flex items-center gap-2">
          <Link
            href="/projects"
            className="hover:text-primary text-muted-foreground"
          >
            Projetos
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <Link
            href={`/projects/${buildingDesignUuid}`}
            className="hover:text-primary text-muted-foreground"
          >
            Projeto 1
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <Link
            href={`/building-designs/${buildingDesignUuid}`}
            className="hover:text-primary text-muted-foreground"
          >
            Cálculo de estrutura
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <Link
            className="border-b-2 leading-[54px] border-black font-bold"
            href={`/building-designs/${buildingDesignUuid}/design-drawings`}
          >
            Especificações
          </Link>
        </nav>
      </div>
      <div className="flex items-center justify-between px-8 py-4 border-b h-14">
        <nav className="flex items-center gap-10 font-medium -tracking-tight">
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "review"
                ? "border-anchor font-bold"
                : "border-transparent"
            }`}
            href={`/building-designs/${buildingDesignUuid}?tab=review`}
          >
            Revisão
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "pillars"
                ? "border-anchor font-bold"
                : "border-transparent"
            }`}
            href={`/building-designs/${buildingDesignUuid}?tab=pillars`}
          >
            Pilares
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "beams" ? "border-anchor font-bold" : "border-transparent"
            }`}
            href={`/building-designs/${buildingDesignUuid}?tab=beams`}
          >
            Vigas
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "beams" ? "border-anchor font-bold" : "border-transparent"
            }`}
            href={`/building-designs/${buildingDesignUuid}?tab=beams`}
          >
            Lajes
          </Link>
        </nav>
        <div className="flex items-center gap-4">
          <BOMDialog />
          <Link
            className="leading-[54px] font-bold flex items-center gap-2"
            href={`/building-designs/${buildingDesignUuid}/design-drawings`}
          >
            Especificações <ArrowUpRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      <div className="overflow-y-auto flex flex-grow mb-10">
        <div className="p-8 space-y-12 w-full flex flex-col mr-[500px]">
          <div>
            <h2 className="text-xl font-semibold">Sapatas</h2>
            <p className="text-sm text-muted-foreground">
              Pormenores de fundação são desenhos que mostram as medidas exatas
              para a construções de componentes de um projeto de estrutura.
            </p>
          </div>
          <div className="flex flex-col space-y-8 border border-dashed p-8 bg-slate-100">
            {/* section header */}

            {/* Foundation drawings */}
            <div>
              {/* Foundation footing plan */}
              <div className="flex flex-col gap-4 border border-dashed p-8 bg-slate-50">
                <div className="flex gap-4 justify-end">
                  <FootingMetadataFileUploaderDialog />
                </div>
                {/* Existing footing plans */}
                <div className="flex flex-col gap-4">
                  {footingDesignDrawingPlans?.map((footingPlan) => (
                    <FootingComponentCard
                      key={footingPlan.uuid}
                      footing={footingPlan}
                      buildingDesignUuid={buildingDesignUuid as string}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>

          <hr />

          {/* section header */}
          <div>
            <h2 className="text-xl font-semibold">Colunas</h2>
            <p className="text-sm text-muted-foreground">
              Pormenores de fundação são desenhos que mostram as medidas exatas
              para a construções de componentes de um projeto de estrutura.
            </p>
          </div>
          <div className="flex flex-col space-y-8 border border-dashed p-8 bg-slate-100">
            {/* Framing drawings */}
            <div className="flex flex-col space-y-12">
              {/* Framing pillar plan */}
              <div className="flex flex-col gap-4 border border-dashed p-8 bg-slate-50">
                <div className="flex gap-4 justify-end">
                  <ColumnMetadataFileUploaderDialog />
                </div>
                {/* Existing footing plans */}
                <div className="flex flex-col gap-4">
                  {columnDesignDrawingPlans?.map((column) => (
                    <ColumnMetadataCardInfo
                      key={column.uuid}
                      column={column}
                      buildingDesignUuid={buildingDesignUuid as string}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
        {drawingComponentFootingUuid && (
          <FootingMetadataSidebar
            drawingComponentFootingUuid={drawingComponentFootingUuid as string}
          />
        )}
        {drawingComponentColumnUuid && (
          <ColumnMetadataSidebar
            drawingComponentColumnUuid={drawingComponentColumnUuid as string}
          />
        )}
      </div>
    </div>
  );
}

export function FootingMetadataFileUploaderDialog() {
  const { uuid: buildingDesignUuid } = useParams();
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost">
          <PlusIcon className="w-4 h-4 mr-1" />
          Adicionar sapata
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>
            <div className="flex items-center gap-2">
              <InfoIcon className="w-4 h-4" />
              <span>Instruções</span>
            </div>
          </DialogTitle>
          <DialogDescription>
            Carregue um desenho de sapata para começar a trabalhar. Ao escolher
            um desenho, o sistema irá identificar as sapatas.
          </DialogDescription>
        </DialogHeader>
        <div className="flex items-center space-x-2">
          <FootingPlanFileUploader
            buildingDesignUuid={buildingDesignUuid as string}
          />
        </div>
        <DialogFooter className="sm:justify-start">
          <DialogClose asChild>
            <Button type="button" variant="secondary">
              Fechar
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export function ColumnMetadataFileUploaderDialog() {
  const { uuid: buildingDesignUuid } = useParams();
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost">
          <PlusIcon className="w-4 h-4 mr-1" />
          Adicionar colunas
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Especificações de colunas</DialogTitle>
          <DialogDescription>
            Adicione uma ou mais colunas para começar a trabalhar.
          </DialogDescription>
        </DialogHeader>
        <div className="flex items-center space-x-2">
          <ColumnMetadataFileUploader
            buildingDesignUuid={buildingDesignUuid as string}
          />
        </div>
        <DialogFooter className="sm:justify-start">
          <DialogClose asChild>
            <Button type="button" variant="secondary">
              Fechar
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export function BOMDialog() {
  const { uuid: buildingDesignUuid } = useParams();
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="default">
          <SparklesIcon className="w-4 h-4 mr-1" />
          Rodar Cálculo de Quantidade
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Projeto de Estrutura</DialogTitle>
          <DialogDescription>
            Carregue um projeto de estrutura para calcular a quantidade de
            materiais necessários para a construção.
          </DialogDescription>
        </DialogHeader>
        <div className="flex items-center space-x-2">
          <DraftBuildingDesignStructuralDrawingUploader
            buildingDesignUuid={buildingDesignUuid as string}
          />
        </div>
        <DialogFooter className="sm:justify-start">
          <DialogClose asChild>
            <Button type="button" variant="secondary">
              Fechar
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
