"use client";
import { Button } from "@/components/ui/button";
import { CircularProgress } from "@/components/ui/circular-progress";
import Check from "@/components/ui/icons/check";
import { fetcher } from "@/lib/api-fetcher";
import { components } from "@/lib/rest-api.types";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export enum StepStatus {
  SUCCESS = "SUCCESS",
  FAILURE = "FAILURE",
  RUNNING = "RUNNING",
  ENQUEUED = "ENQUEUED",
  NOT_STARTED = "NOT_STARTED",
}

export enum BuildingStep {
  NOT_STARTED = "NOT_STARTED",
  CREATING_FOOTING_COMPONENTS = "CREATING_FOOTING_COMPONENTS",
  CREATING_COLUMN_COMPONENTS = "CREATING_COLUMN_COMPONENTS",
  CREATING_BEAM_COMPONENTS = "CREATING_BEAM_COMPONENTS",
  CREATING_SLAB_COMPONENTS = "CREATING_SLAB_COMPONENTS",
  FINISHED = "FINISHED",
  FAILED = "FAILED",
}

const stepOrder: Record<BuildingStep, number> = {
  [BuildingStep.NOT_STARTED]: 0,
  [BuildingStep.CREATING_FOOTING_COMPONENTS]: 1,
  [BuildingStep.CREATING_COLUMN_COMPONENTS]: 2,
  [BuildingStep.CREATING_BEAM_COMPONENTS]: 3,
  [BuildingStep.CREATING_SLAB_COMPONENTS]: 4,
  [BuildingStep.FINISHED]: 5,
  [BuildingStep.FAILED]: 6,
};

export const loadingSteps: {
  id: string;
  step_enum: BuildingStep;
  description: string;
}[] = [
  {
    id: "step-creating-footing-components",
    step_enum: BuildingStep.CREATING_FOOTING_COMPONENTS,
    description: "Medindo e criando componentes de sapatas",
  },
  {
    id: "step-creating-column-components",
    step_enum: BuildingStep.CREATING_COLUMN_COMPONENTS,
    description: "Medindo e criando componentes de pilares",
  },
  {
    id: "step-creating-beam-components",
    step_enum: BuildingStep.CREATING_BEAM_COMPONENTS,
    description: "Medindo e criando componentes de vigas",
  },
];

export default function Building() {
  const { uuid } = useParams();
  const [buildingDesignStatus, setBuildingDesignStatus] =
    useState<BuildingStep>(BuildingStep.NOT_STARTED);

  const { data: draftBuildingDesign } = useQuery({
    queryKey: ["draftBuildingDesign", uuid],
    queryFn: () =>
      fetcher<components["schemas"]["DraftBuildingDesign"]>(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${uuid}/`
      ),
    refetchInterval: 5000,
  });

  useEffect(() => {
    if (draftBuildingDesign) {
      setBuildingDesignStatus(draftBuildingDesign.status as BuildingStep);
    }
  }, [draftBuildingDesign]);

  // Util function to render a project step status with the appropriate icon
  const showStepStatus = (step: BuildingStep) => {
    let stepStatus = StepStatus.NOT_STARTED;
    console.log(step, stepOrder[step], stepOrder[buildingDesignStatus]);
    if (
      stepOrder[step] < stepOrder[buildingDesignStatus] ||
      buildingDesignStatus === BuildingStep.FINISHED
    ) {
      stepStatus = StepStatus.SUCCESS;
    }

    if (stepOrder[step] === stepOrder[buildingDesignStatus]) {
      stepStatus = StepStatus.RUNNING;
    }

    switch (stepStatus) {
      case StepStatus.RUNNING:
        return (
          <div className="h-6 w-6">
            <CircularProgress width={24} height={24} progress={50} />
          </div>
        );
      case StepStatus.SUCCESS:
        return (
          <div className="rounded-full h-6 w-6 flex items-center justify-center bg-green-600">
            <Check className="w-4 h-4 text-white" />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="bg-white h-screen">
      <div className="flex items-center justify-center h-full">
        <div className="flex items-start">
          <div className="w-[300px]">
            <h1 className="text-4xl font-bold">Medindo...</h1>
            <p className="text-sm text-muted-foreground">
              Aproximadamente 2minutos
            </p>
            <div className="mt-4">
              <Button disabled={buildingDesignStatus !== BuildingStep.FINISHED}>
                Ir para detalhes da construção
              </Button>
            </div>
          </div>
          <div className="flex flex-col">
            <ul className="flex flex-col gap-4">
              {loadingSteps.map((step) => (
                <li
                  key={step.id}
                  className="flex items-center justify-between gap-4"
                >
                  {step.description}
                  {showStepStatus(step.step_enum)}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
