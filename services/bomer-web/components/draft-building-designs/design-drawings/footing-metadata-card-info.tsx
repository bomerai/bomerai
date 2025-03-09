"use client";

import { Button } from "@/components/ui/button";
import { Clock, Pencil, Trash2, XCircle, LockOpen, Lock } from "lucide-react";
import { faCheckCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  DesignDrawingComponentMetadata,
  CeleryTaskResult,
} from "@/lib/rest-types";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

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

export default function FootingMetadataCardInfo({
  footing,
  buildingDesignUuid,
}: {
  footing: DesignDrawingComponentMetadata;
  buildingDesignUuid: string;
}) {
  const router = useRouter();

  const { data: celeryTaskResult } = useQuery({
    queryKey: ["celery-task-result", footing.task_id],
    queryFn: () => getCeleryTaskResult(footing.task_id || ""),
  });
  console.log(celeryTaskResult);

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

  return (
    <div
      className="p-6 bg-white border rounded flex items-start justify-between gap-12 hover:cursor-pointer hover:border-anchor"
      onClick={() => {
        router.push(
          `/building-designs/${buildingDesignUuid}/design-drawings?drawingComponentFootingUuid=${footing.uuid}`
        );
      }}
    >
      <div className="flex flex-col space-y-8 flex-1">
        <div>
          <h4 className="font-semibold">
            {footing?.data?.type} {footing?.data?.references}
          </h4>
          <p className="text-sm text-muted-foreground">
            {footing.justification}
          </p>
        </div>

        <div className="flex items-center gap-2">
          {renderStatusIcon(celeryTaskResult?.status || "PENDING")}
          <span className="text-xs text-muted-foreground">
            {renderStatusText(celeryTaskResult?.status || "PENDING")}
          </span>
        </div>

        <div className="flex flex-col space-y-4">
          <div className="grid grid-cols-4 gap-4 text-xs">
            <div className="flex flex-col">
              <div className="font-medium">Largura (cm)</div>
              <div className="">{(footing?.data || { width: 0 }).width}</div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Comprimento (cm)</div>
              <div className="">{(footing?.data || { length: 0 }).length}</div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Altura (cm)</div>
              <div className="">{(footing?.data || { height: 0 }).height}</div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Referências</div>
              <div className="italic">
                {footing?.data?.references || "Aguardando pilares"}
              </div>
            </div>
          </div>
          <hr className="w-full border-t border/60" />
          <div className="grid grid-cols-4 gap-4 text-xs">
            <div className="flex flex-col">
              <div className="font-medium">Armadura Inf. X</div>
              <div className="">
                {
                  (
                    footing?.data || {
                      bottom_reinforcement_x: 0,
                    }
                  ).bottom_reinforcement_x
                }
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Armadura Inf. Y</div>
              <div className="">
                {
                  (
                    footing?.data || {
                      bottom_reinforcement_y: 0,
                    }
                  ).bottom_reinforcement_y
                }
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Armadura Sup. X</div>
              <div className="">
                {
                  (
                    footing?.data || {
                      top_reinforcement_x: 0,
                    }
                  ).top_reinforcement_x
                }
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Armadura Sup. Y</div>
              <div className="">
                {
                  (
                    footing?.data || {
                      top_reinforcement_y: 0,
                    }
                  ).top_reinforcement_y
                }
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
        <Button variant="ghost" size="icon">
          {footing.is_locked ? (
            <Lock className="w-4 h-4 text-anchor" />
          ) : (
            <LockOpen className="w-4 h-4 text-anchor" />
          )}
        </Button>
      </div>
    </div>
  );
}
