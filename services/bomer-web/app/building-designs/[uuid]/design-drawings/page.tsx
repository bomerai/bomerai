"use client";

import {
  ArrowUpRight,
  ChevronRight,
  Pencil,
  PlusIcon,
  SparklesIcon,
  Trash2,
} from "lucide-react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import FootingPlanFileUploader from "@/components/draft-building-designs/design-drawings/footing-plan-file-uploader";
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
import BuildComponentSidebar from "@/components/draft-building-designs/build-components/build-component-sidebar";
import { useQuery } from "@tanstack/react-query";
import { DesignDrawing } from "@/lib/rest-types";
import FootingPlanCard from "@/components/draft-building-designs/design-drawings/footing-plan-card";

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

  const { data: designDrawings } = useQuery({
    queryKey: ["design-drawings", buildingDesignUuid],
    queryFn: () => getDesignDrawings(buildingDesignUuid as string),
  });

  const footingDesignDrawings = designDrawings?.filter(
    (designDrawing) => designDrawing.type === "STRUCTURAL_DRAWING"
  );

  const footingDesignDrawingPlans = footingDesignDrawings?.flatMap(
    (designDrawing) => designDrawing.design_drawing_plans
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
          <Button variant="tertiary">
            <SparklesIcon className="w-4 h-4" />
            Calcular
          </Button>
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
          <div className="flex flex-col space-y-8 border border-dashed p-8 bg-slate-100">
            {/* section header */}
            <div>
              <h2 className="text-xl font-semibold">
                Sapatas, Vigas de apoio e Laje de fundação
              </h2>
              <p className="text-sm text-muted-foreground">
                Pormenores de fundação são desenhos que mostram as medidas
                exatas para a construções de componentes de um projeto de
                estrutura.
              </p>
            </div>

            {/* Foundation drawings */}
            <div>
              {/* Foundation footing plan */}
              <div className="flex flex-col gap-4 border border-dashed p-8 bg-slate-50">
                <div className="flex gap-4 justify-between">
                  <h3 className="text-lg font-medium">
                    Especificações de sapatas
                  </h3>
                  <PilarPlanFileUploaderDialog />
                </div>
                {/* Existing footing plans */}
                <div className="flex flex-col gap-4">
                  {footingDesignDrawingPlans?.map((footingPlan) => (
                    <FootingPlanCard
                      key={footingPlan.uuid}
                      footingPlan={footingPlan}
                    />
                  ))}
                </div>
              </div>

              {/* Foundation beam plan */}
            </div>
          </div>

          <hr />

          <div className="flex flex-col space-y-8 border border-dashed p-8 bg-slate-100">
            {/* section header */}
            <div>
              <h2 className="text-xl font-semibold">Colunas, Vigas e Lajes</h2>
              <p className="text-sm text-muted-foreground">
                Pormenores de fundação são desenhos que mostram as medidas
                exatas para a construções de componentes de um projeto de
                estrutura.
              </p>
            </div>
            {/* Framing drawings */}
            <div className="flex flex-col space-y-12">
              {/* Framing pillar plan */}
              <div className="flex flex-col gap-4 border border-dashed p-8 bg-slate-50">
                <div className="flex gap-4 justify-between">
                  <h3 className="font-medium text-lg">
                    Especificações de colunas
                  </h3>
                  <PilarPlanFileUploaderDialog />
                </div>
                {/* Existing footing plans */}
                <div className="flex flex-col gap-4">
                  <div className="p-6 bg-white border rounded flex items-start justify-between gap-12">
                    <div className="flex flex-col space-y-4 flex-1">
                      <div>
                        <h4 className="font-semibold">Sapata 1</h4>
                        <p className="text-sm text-muted-foreground">
                          Sapata 1 é uma sapata de fundação que suporta a carga
                          do pilar 1.
                        </p>
                      </div>

                      <div className="flex items-center justify-between text-sm">
                        <div className="flex flex-col">
                          <div className="font-medium">Largura (cm)</div>
                          <div className="">75</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Comprimento (cm)</div>
                          <div className="">75</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Altura (cm)</div>
                          <div className="">40</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Referências</div>
                          <div className="italic">Aguardando pilares</div>
                        </div>
                      </div>
                      <hr className="w-full border-t border/60" />
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex flex-col">
                          <div className="font-medium">Armadura Inf. X</div>
                          <div className="">ø8//30</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Armadura Inf. Y</div>
                          <div className="">ø8//30</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Armadura Sup. X</div>
                          <div className="">ø12//30</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Armadura Sup. Y</div>
                          <div className="">ø12//30</div>
                        </div>
                      </div>
                    </div>
                    <div>
                      <Button variant="ghost">
                        <Trash2 className="w-4 h-4 text-anchor" />
                      </Button>
                      <Button variant="ghost">
                        <Pencil className="w-4 h-4 text-anchor" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Framing beam plan */}
              <div className="flex flex-col gap-4 border border-dashed p-8 bg-slate-50">
                <div className="flex gap-4 justify-between">
                  <h3 className="text-lg font-medium">
                    Especificações de vigas
                  </h3>
                  <PilarPlanFileUploaderDialog />
                </div>
                {/* Existing footing plans */}
                <div className="flex flex-col gap-4">
                  <div className="p-6 bg-white border rounded flex items-start justify-between gap-12">
                    <div className="flex flex-col space-y-4 flex-1">
                      <div>
                        <h4 className="font-semibold">Viga 1</h4>
                        <p className="text-sm text-muted-foreground">
                          Sapata 1 é uma sapata de fundação que suporta a carga
                          do pilar 1.
                        </p>
                      </div>

                      <div className="flex items-center justify-between text-sm">
                        <div className="flex flex-col">
                          <div className="font-medium">Largura (cm)</div>
                          <div className="">75</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Comprimento (cm)</div>
                          <div className="">75</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Altura (cm)</div>
                          <div className="">40</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Referências</div>
                          <div className="italic">Aguardando pilares</div>
                        </div>
                      </div>
                      <hr className="w-full border-t border/60" />
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex flex-col">
                          <div className="font-medium">Armadura Inf. X</div>
                          <div className="">ø8//30</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Armadura Inf. Y</div>
                          <div className="">ø8//30</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Armadura Sup. X</div>
                          <div className="">ø12//30</div>
                        </div>
                        <div className="flex flex-col border-l pl-4">
                          <div className="font-medium">Armadura Sup. Y</div>
                          <div className="">ø12//30</div>
                        </div>
                      </div>
                    </div>
                    <div>
                      <Button variant="ghost">
                        <Trash2 className="w-4 h-4 text-anchor" />
                      </Button>
                      <Button variant="ghost">
                        <Pencil className="w-4 h-4 text-anchor" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {buildingDesignUuid && <BuildComponentSidebar />}
      </div>
    </div>
  );
}

export function PilarPlanFileUploaderDialog() {
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
          <DialogTitle>Adicionar um novo projeto</DialogTitle>
          <DialogDescription>
            Adicione um novo projeto para começar a trabalhar.
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
