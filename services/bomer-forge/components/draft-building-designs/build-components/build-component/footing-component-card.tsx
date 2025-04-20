"use client";

import { Button } from "@/components/ui/button";
import { Clock, Pencil, Trash2, XCircle } from "lucide-react";
import { faCheckCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { CeleryTaskResult } from "@/lib/rest-types";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { components } from "@/lib/rest-api.types";
import z from "zod";

const componentDataSchema = z.object({
  type: z.string(),
  references: z.string().optional(),
  width: z.number().optional(),
  length: z.number().optional(),
  height: z.number().optional(),
  bottom_reinforcement_x: z.string().nullable(),
  bottom_reinforcement_y: z.string().nullable(),
  top_reinforcement_x: z.string().nullable(),
  top_reinforcement_y: z.string().nullable(),
});

const getCeleryTaskResult = async (
  taskId: string | undefined
): Promise<CeleryTaskResult> => {
  if (!taskId) {
    return {
      status: "PENDING",
      result: null,
    };
  }
  const resp = await fetch(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/celery-task-result/${taskId}/`,
    {
      method: "GET",
      credentials: "include",
      mode: "cors",
    }
  );
  return resp.json();
};

export function FootingComponentCard({
  footing,
  buildingDesignUuid,
}: {
  footing: components["schemas"]["DraftBuildingDesignBuildingComponent"];
  buildingDesignUuid: string;
}) {
  const router = useRouter();

  const { data: celeryTaskResult } = useQuery({
    queryKey: ["celery-task-result", footing.task_id],
    queryFn: () => getCeleryTaskResult(footing.task_id || ""),
  });
  console.log(celeryTaskResult);

  const componentData = componentDataSchema.parse(
    footing.building_component.component_data
  );

  const renderStatusIcon = (status: CeleryTaskResult["status"]) => {
    switch (status) {
      case "PENDING":
        return <Clock className="w-4 h-4 text-muted-foreground" />;
      case "STARTED":
        return <Clock className="w-4 h-4 text-anchor" />;
      case "SUCCESS":
        return (
          <FontAwesomeIcon
            icon={faCheckCircle}
            className="w-4 h-4 text-green-500"
          />
        );
      case "FAILURE":
        return <XCircle className="w-4 h-4 text-red-500" />;
      case "RETRY":
    }
  };

  const renderStatusText = (status: CeleryTaskResult["status"]) => {
    switch (status) {
      case "PENDING":
        return "Aguardando";
      case "STARTED":
        return "Calculando";
      case "SUCCESS":
        return "Calculado com sucesso!";
      case "FAILURE":
        return "Erro no calculo de quantidade!";
    }
  };

  const handleClick = () => {
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.set("footingComponentUuid", footing.building_component.uuid);
    router.push(`/buildings/${buildingDesignUuid}?${searchParams.toString()}`);
  };

  return (
    <div
      className="p-6 bg-white border rounded flex items-start justify-between gap-12 hover:cursor-pointer hover:ring-2 hover:ring-anchor"
      onClick={handleClick}
    >
      <div className="flex flex-col space-y-8 flex-1">
        <div>
          <h4 className="font-semibold">
            {componentData.type} {componentData.references}
          </h4>
        </div>

        <div className="flex items-center gap-2">
          {renderStatusIcon(celeryTaskResult?.status || "PENDING")}
          <span className="text-xs text-muted-foreground">
            {renderStatusText(celeryTaskResult?.status || "PENDING")}
          </span>
        </div>

        <div className="flex flex-col space-y-4">
          <div className="grid grid-cols-4 gap-4">
            <div className="flex flex-col">
              <div className="font-medium text-sm text-muted-foreground">
                Dimensões (cm)
              </div>
              <div className="font-semibold">
                {componentData.width}x{componentData.length}x
                {componentData.height}
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium text-sm text-muted-foreground">
                Referências
              </div>
              <div className="italic text-sm font-semibold">
                {componentData.references}
              </div>
            </div>
          </div>
          <hr className="w-full border-t border/60" />
          <div className="grid grid-cols-4 gap-4">
            <div className="flex flex-col">
              <div className="font-medium text-sm text-muted-foreground">
                Armadura Inf. X
              </div>
              <div className="font-semibold">
                {componentData.bottom_reinforcement_x}
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium text-sm text-muted-foreground">
                Armadura Inf. Y
              </div>
              <div className="font-semibold">
                {componentData.bottom_reinforcement_y}
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium text-sm text-muted-foreground">
                Armadura Sup. X
              </div>
              <div className="font-semibold">
                {componentData.top_reinforcement_x}
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium text-sm text-muted-foreground">
                Armadura Sup. Y
              </div>
              <div className="font-semibold">
                {componentData.top_reinforcement_y}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon">
          <Trash2 className="w-4 h-4 text-anchor" />
        </Button>
        <Button variant="ghost" size="icon">
          <Pencil className="w-4 h-4 text-anchor" />
        </Button>
      </div>
    </div>
  );
}
