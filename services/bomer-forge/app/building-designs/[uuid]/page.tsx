"use client";

import { ReviewSection } from "@/components/draft-building-designs/review-section";
import { Button } from "@/components/ui/button";
import { ChevronRight, CuboidIcon, RulerIcon } from "lucide-react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { ColumnsSection } from "@/components/draft-building-designs/columns-section";
import Asterisc from "@/components/ui/icons/asterisc";
import { useQuery } from "@tanstack/react-query";
import { components } from "@/lib/rest-api.types";
import { fetcher } from "@/lib/api-fetcher";
import { FoundationsSection } from "@/components/draft-building-designs/foundations-section";
import { FootingComponentSidebar } from "@/components/draft-building-designs/build-components/build-component/footing-component-sidebar";
import { cn } from "@/lib/utils";
import { ColumnComponentSidebar } from "@/components/draft-building-designs/build-components/build-component/column-component-sidebar";

const TABS = {
  review: "review",
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

  const renderTabContent = () => {
    switch (tab) {
      case TABS.review:
        return <ReviewSection />;
      case TABS.foundations:
        return <FoundationsSection buildingDesignUuid={uuid as string} />;
      case TABS.columns:
        return <ColumnsSection buildingDesignUuid={uuid as string} />;
      default:
        return null;
    }
  };

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
            href={`/projects/${uuid}`}
            className="hover:text-primary text-muted-foreground"
          >
            Projeto 1
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <Link
            className="leading-[54px] font-bold"
            href={`/building-designs/${uuid}/structure-calculation`}
          >
            {draftBuildingDesign?.name}
          </Link>
        </nav>
      </div>
      <div className="flex items-center justify-between px-8 py-4 border-b h-14 z-10">
        <nav className="flex items-center space-x-6">
          <Link
            className="leading-[54px] flex items-center gap-1"
            href={`/building-designs/${uuid}/measurements`}
          >
            <RulerIcon className="w-4 h-4 text-anchor" />
            Medidas
          </Link>
          <Link
            aria-disabled={true}
            className="leading-[54px] flex items-center gap-1 opacity-30"
            href={`/building-designs/${uuid}/measurements`}
          >
            <CuboidIcon className="w-4 h-4 text-anchor" />
            Materiais
          </Link>
        </nav>
        <nav className="flex items-center space-x-6">
          <Link
            className={`leading-[54px] flex items-center gap-1 ${
              tab === TABS.review ? "font-bold" : ""
            }`}
            href={`/building-designs/${uuid}?tab=${TABS.review}`}
          >
            Revisão
          </Link>
          <Link
            className={`leading-[54px] flex items-center gap-1 ${
              tab === TABS.foundations ? "font-bold" : ""
            }`}
            href={`/building-designs/${uuid}?tab=${TABS.foundations}`}
          >
            Fundação
          </Link>
          <Link
            className={`leading-[54px] flex items-center gap-1 ${
              tab === TABS.columns ? "font-bold" : ""
            }`}
            href={`/building-designs/${uuid}?tab=${TABS.columns}`}
          >
            Pilares
          </Link>
          <Link
            className={`leading-[54px] flex items-center gap-1 ${
              tab === TABS.beams ? "font-bold" : ""
            }`}
            href={`/building-designs/${uuid}?tab=${TABS.beams}`}
          >
            Vigas
          </Link>
          <Link
            className={`leading-[54px] flex items-center gap-1 ${
              tab === "slabs" ? "font-bold" : ""
            }`}
            href={`/building-designs/${uuid}?tab=slabs`}
          >
            Lajes
          </Link>
        </nav>
        <div className="flex items-center gap-4">
          <Button variant="outline">
            <RulerIcon className="w-4 h-4 text-anchor" />
            Medir projeto de estrutura
          </Button>
          <Button variant="outline">
            <Asterisc className="w-4 h-4 text-anchor" />
            Rodar cálculo de quantidade
          </Button>

          {/* <Link
            className="leading-[54px] font-bold flex items-center gap-2"
            href={`/building-designs/${uuid}/design-drawings`}
          >
            Especificações <ArrowUpRight className="w-4 h-4" />
          </Link> */}
        </div>
      </div>

      <div className="overflow-y-auto flex flex-grow mb-10">
        <div id="tab-container" className="flex w-full">
          <div
            className={cn(
              "tab-content flex flex-1 mr-[500px] z-10",
              tab === TABS.review && "mr-[0px]"
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
