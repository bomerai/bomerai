"use client";
import BuildComponentSidebar from "@/components/build-components/build-component-sidebar";
import { MaterialCostExplorer } from "@/components/materials/material-cost-explorer";
import ExteriorComponentsSection from "@/components/projects/exterior-components-section";
import { FloorPlanSection } from "@/components/projects/floor-plan-section";
import ReviewSection from "@/components/projects/review-section";
import { Button } from "@/components/ui/button";
import { ChevronRight, SparklesIcon } from "lucide-react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";

export default function ProjectPage() {
  const { uuid } = useParams();
  const searchParams = useSearchParams();
  const tab = searchParams.get("tab");
  const buildingComponentUuid = searchParams.get("buildingComponentUuid");
  const selectedMaterialEvaluationUuid = searchParams.get(
    "selectedMaterialEvaluationUuid"
  );

  const renderTabContent = () => {
    switch (tab) {
      case "floor-plan":
        return <FloorPlanSection />;
      case "exterior-components":
        return <ExteriorComponentsSection />;
      case "review":
        return <ReviewSection />;
      default:
        return <FloorPlanSection />;
    }
  };

  return (
    <div className="flex flex-col flex-grow relative overflow-y-auto h-screen">
      {/* page header */}
      <div className="flex items-center justify-between px-8 py-4 border-b h-14">
        <nav className="font-medium text-lg flex items-center gap-2">
          <Link
            href="/projects"
            className="hover:text-primary text-muted-foreground"
          >
            Projetos
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <span>Casa T3, Gondufe, Ponte de Lima</span>
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
            href={`/projects/${uuid}?tab=review`}
          >
            Revisão
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "floor-plan"
                ? "border-anchor font-bold"
                : "border-transparent"
            }`}
            href={`/projects/${uuid}?tab=floor-plan`}
          >
            Planta baixa
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "exterior-components"
                ? "border-anchor font-bold"
                : "border-transparent"
            }`}
            href={`/projects/${uuid}?tab=exterior-components`}
          >
            Components Externos
          </Link>
          <Link
            className={`border-b-2 leading-[54px] ${
              tab === "interior-components"
                ? "border-anchor font-bold"
                : "border-transparent"
            }`}
            href={`/projects/${uuid}?tab=interior-components`}
          >
            Components Internos
          </Link>
        </nav>
        <Button variant="tertiary">
          <SparklesIcon className="w-4 h-4" />
          Análise de custo
        </Button>
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
