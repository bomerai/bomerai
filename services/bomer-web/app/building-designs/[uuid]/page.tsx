"use client";
import BuildComponentSidebar from "@/components/draft-building-designs/build-components/build-component-sidebar";
import { MaterialCostExplorer } from "@/components/materials/material-cost-explorer";
import { FloorPlanSection } from "@/components/draft-building-designs/build-components/build-component/floor-plan-section";
import ReviewSection from "@/components/projects/review-section";
import { Button } from "@/components/ui/button";
import { ArrowUpRight, ChevronRight, SparklesIcon } from "lucide-react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import PillarsSection from "@/components/draft-building-designs/build-components/build-component/pillars-section";
import DesignDrawingsSection from "@/components/draft-building-designs/design-drawings/design-drawings-section";

export default function BuildingDesignPage() {
  const { uuid } = useParams();
  const searchParams = useSearchParams();
  const tab = searchParams.get("tab");
  const buildingComponentUuid = searchParams.get("buildingComponentUuid");
  const selectedMaterialEvaluationUuid = searchParams.get(
    "selectedMaterialEvaluationUuid"
  );

  const renderTabContent = () => {
    switch (tab) {
      case "review":
        // Review section
        return <ReviewSection />;
      case "design-drawings":
        // Draft building design drawings
        return <DesignDrawingsSection />;
      case "pillars":
        // Draft building design components
        return <PillarsSection />;
      default:
        return <FloorPlanSection />;
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
            className="border-b-2 leading-[54px] border-black font-bold"
            href={`/building-designs/${uuid}/structure-calculation`}
          >
            Cálculo de estrutura
          </Link>
        </nav>
      </div>
      <div className="flex items-center justify-between px-8 py-4 border-b h-14">
        <nav className="flex items-center gap-10">
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "review"
                ? "border-anchor font-bold"
                : "border-transparent"
            }`}
            href={`/building-designs/${uuid}?tab=review`}
          >
            Revisão
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "pillars"
                ? "border-anchor font-bold"
                : "border-transparent"
            }`}
            href={`/building-designs/${uuid}?tab=pillars`}
          >
            Pilares
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "beams" ? "border-anchor font-bold" : "border-transparent"
            }`}
            href={`/building-designs/${uuid}?tab=beams`}
          >
            Vigas
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "beams" ? "border-anchor font-bold" : "border-transparent"
            }`}
            href={`/building-designs/${uuid}?tab=beams`}
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
            href={`/building-designs/${uuid}/design-drawings`}
          >
            Especificações <ArrowUpRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      <div className="overflow-y-auto flex flex-grow mb-10">
        <div id="tab-container" className="flex w-full">
          <div className="tab-content flex flex-1 mr-[500px] z-10">
            {renderTabContent()}
          </div>
          {buildingComponentUuid && <BuildComponentSidebar />}
          {selectedMaterialEvaluationUuid && <MaterialCostExplorer />}
        </div>
      </div>
    </div>
  );
}
