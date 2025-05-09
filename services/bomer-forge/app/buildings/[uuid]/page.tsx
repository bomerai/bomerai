"use client";

import { DraftBuildingDesignBomSection } from "@/components/draft-building-designs/draft-building-design-bom-section";
import { Button } from "@/components/ui/button";
import {
  ChevronRight,
  ArrowRight,
  CheckCircleIcon,
  ToyBrick,
} from "lucide-react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { DraftBuildingDesignColumns } from "@/components/draft-building-designs/draft-building-design-columns";
import { DraftBuildingDesignBeams } from "@/components/draft-building-designs/draft-building-design-beams";
import Asterisc from "@/components/ui/icons/asterisc";
import { useQuery } from "@tanstack/react-query";
import { components } from "@/lib/rest-api.types";
import { fetcher } from "@/lib/api-fetcher";
import { DraftBuildingDesignFootings } from "@/components/draft-building-designs/draft-building-design-footings";
import { FootingComponentSidebar } from "@/components/draft-building-designs/build-components/build-component/footing-component-sidebar";
import { cn } from "@/lib/utils";
import { ColumnComponentSidebar } from "@/components/draft-building-designs/build-components/build-component/column-component-sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowTurnUpRightIcon, BellIcon } from "@heroicons/react/24/outline";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";

const TABS = {
  bom: "bom",
  foundations: "foundations",
  columns: "columns",
  beams: "beams",
  slabs: "slabs",
};

export default function BuildingDesignPage() {
  const { uuid } = useParams();
  const searchParams = useSearchParams();
  const tab = searchParams.get("tab");
  const columnComponentUuid = searchParams.get("columnComponentUuid");
  const footingComponentUuid = searchParams.get("footingComponentUuid");

  const { data: draftBuildingDesign } = useQuery({
    queryKey: ["draftBuildingDesign", uuid],
    queryFn: () =>
      fetcher<components["schemas"]["DraftBuildingDesign"]>(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${uuid}/`
      ),
  });

  const HomeSection = () => {
    return (
      <div className="flex flex-col flex-grow relative overflow-y-auto h-screen">
        <div className="p-8 space-y-8 w-full">
          <div className="flex flex-col space-y-12">
            <div>
              <h2 className="font-bold text-2xl mb-4">Módulos de cálculo</h2>
              <p className="w-1/2">
                Cada módulo de cálculo possui um conjunto de cálculos para uma
                parte específica da construção.
              </p>
            </div>
            <div className="grid grid-cols-4">
              <Card className="">
                <CardHeader className="flex flex-row items-center space-y-0">
                  <Asterisc className="w-4 h-4 mr-4 text-anchor" />
                  <CardTitle className="text-xl">
                    Cálculo de estrutura
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm mb-8">
                    Cálculo de estrutura é um módulo de cálculo que calcula a
                    estrutura da construção como pilares, vigas, lajes e betão.
                  </p>
                  <div className="flex justify-end">
                    <Link
                      href={`/buildings/${uuid}/modules/structure-project/bom?step=1`}
                      className="flex items-center bg-anchor text-white px-4 py-1 text-sm rounded shadow-md transition-all duration-300"
                    >
                      Começar
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderTabContent = () => {
    switch (tab) {
      case TABS.bom:
        return (
          <DraftBuildingDesignBomSection
            draftBuildingDesignId={uuid as string}
          />
        );
      case TABS.foundations:
        return (
          <DraftBuildingDesignFootings buildingDesignUuid={uuid as string} />
        );
      case TABS.columns:
        return (
          <DraftBuildingDesignColumns buildingDesignUuid={uuid as string} />
        );
      case TABS.beams:
        return <DraftBuildingDesignBeams buildingDesignUuid={uuid as string} />;
      default:
        return <HomeSection />;
    }
  };

  return (
    <div className="bg-white flex flex-col flex-grow relative overflow-y-auto h-screen">
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
            href={`/projects/${uuid}`}
            className="hover:text-primary text-muted-foreground"
          >
            Projeto 1
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <Link
            className="leading-[54px] font-bold"
            href={`/buildings/${uuid}/structure-calculation`}
          >
            {draftBuildingDesign?.name}
          </Link>
        </nav>
        <div className="flex self-end">
          {/* notifications */}
          <div className="flex items-center gap-2">
            <div className="relative">
              {/* notifications dropdown */}
              <NotificationDropdown />
            </div>
          </div>
        </div>
      </div>
      <div className="flex items-center justify-between px-8 py-4 border-b h-14 z-10">
        <div className="flex items-center gap-4">
          <Link
            className={`leading-[54px] flex items-center font-semibold gap-1 ${
              tab === TABS.bom ? "font-bold" : ""
            }`}
            href={`/buildings/${uuid}?tab=${TABS.bom}`}
          >
            Caderno de encargos
            <ArrowTurnUpRightIcon className="w-4 h-4" />
          </Link>
          |
          <span className="text-sm text-black/70 font-semibold">
            Componentes:
          </span>
          <nav className="flex items-center space-x-6">
            <Link
              className={`leading-[54px] flex items-center gap-1 ${
                tab === TABS.foundations ? "font-bold" : ""
              }`}
              href={`/buildings/${uuid}?tab=${TABS.foundations}`}
            >
              <ToyBrick className="w-4 h-4" />
              Fundação
            </Link>
            <Link
              className={`leading-[54px] flex items-center gap-1 ${
                tab === TABS.columns ? "font-bold" : ""
              }`}
              href={`/buildings/${uuid}?tab=${TABS.columns}`}
            >
              <ToyBrick className="w-4 h-4" />
              Pilares
            </Link>
            <Link
              className={`leading-[54px] flex items-center gap-1 ${
                tab === TABS.beams ? "font-bold" : ""
              }`}
              href={`/buildings/${uuid}?tab=${TABS.beams}`}
            >
              <ToyBrick className="w-4 h-4" />
              Vigas
            </Link>
            <Link
              className={`leading-[54px] flex items-center gap-1 ${
                tab === "slabs" ? "font-bold" : ""
              }`}
              href={`/buildings/${uuid}?tab=slabs`}
            >
              <ToyBrick className="w-4 h-4" />
              Lajes
            </Link>
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <Button variant="outline">
            <Asterisc className="w-4 h-4 text-anchor" />
            Gerar caderno de encargos
          </Button>
        </div>
      </div>

      <div className="overflow-y-auto flex flex-grow mb-10">
        <div id="tab-container" className="flex w-full">
          <div
            className={cn(
              "tab-content flex flex-1 mr-[500px] z-10",
              (tab === TABS.bom || tab === null) && "mr-[0px]"
            )}
          >
            {renderTabContent()}
          </div>
          {columnComponentUuid && (
            <ColumnComponentSidebar
              buildingComponentUuid={columnComponentUuid}
            />
          )}
          {footingComponentUuid && (
            <FootingComponentSidebar
              buildingComponentUuid={footingComponentUuid}
            />
          )}
        </div>
      </div>
    </div>
  );
}

const NotificationItem = () => {
  return (
    <div className="flex items-center gap-2 px-4 py-2 hover:bg-gray-100">
      <CheckCircleIcon className="w-4 h-4 text-green-500" />
      <p className="font-medium hover:underline">
        Cálculo finalizado com sucesso.{" "}
      </p>
      <span className="text-sm text-muted-foreground">2 horas atrás</span>
    </div>
  );
};

const NotificationDropdown = () => {
  return (
    <Popover>
      <PopoverTrigger className="relative flex items-center">
        <BellIcon className="w-5 h-5 text-anchor" />
        <div className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></div>
      </PopoverTrigger>
      <PopoverContent className="w-[500px] p-0">
        <div className="flex flex-col">
          <h2 className="text-xl font-bold p-4">Notificações</h2>
          <Separator />
          <div className="flex flex-col px-2 py-4">
            <NotificationItem />
            <NotificationItem />
            <NotificationItem />
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
};
