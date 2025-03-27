import { XIcon } from "lucide-react";
import { Button } from "../../../ui/button";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { components } from "@/lib/rest-api.types";
import { truncate } from "lodash";
import { Skeleton } from "@/components/ui/skeleton";
import { fetcher } from "@/lib/api-fetcher";
import { z } from "zod";

const componentDataSchema = z.object({
  type: z.string(),
  references: z.string().optional(),
  justification: z.string().optional(),
  width: z.number().optional(),
  length: z.number().optional(),
  height: z.number().optional(),
  bottom_reinforcement_x: z.string().optional(),
  bottom_reinforcement_y: z.string().optional(),
  top_reinforcement_x: z.string().optional(),
  top_reinforcement_y: z.string().optional(),
});

const bomSchema = z.object({
  concrete_volume_in_cubic_meters: z.number().optional(),
  steel_weight_in_kilograms: z.number().optional(),
  rationale: z.string().optional(),
});

const getBuildingComponent = async (
  buildingComponentUuid: string
): Promise<components["schemas"]["BuildingComponent"]> => {
  const response = await fetcher<components["schemas"]["BuildingComponent"]>(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/building-components/${buildingComponentUuid}/`,
    {
      credentials: "include",
      mode: "cors",
    }
  );
  return response;
};

export function FootingComponentSidebar({
  buildingComponentUuid,
}: {
  buildingComponentUuid: string;
}) {
  const router = useRouter();

  const { data: buildingComponent, isLoading } = useQuery({
    queryKey: ["building-component", buildingComponentUuid],
    queryFn: () => getBuildingComponent(buildingComponentUuid),
  });

  if (!buildingComponent) {
    return null;
  }

  const componentData = componentDataSchema.parse(
    buildingComponent?.component_data
  );

  const bom = bomSchema.parse(buildingComponent?.component_bom);

  return (
    <div className="bg-white border-l w-[500px] fixed right-0 bottom-0 top-[112px]">
      {isLoading && (
        <div className="flex justify-center items-center h-full">
          <div className="space-y-4">
            <Skeleton className="h-4 w-[250px]" />
            <Skeleton className="h-4 w-[200px]" />
          </div>
        </div>
      )}
      {!isLoading && buildingComponent && (
        <div className="min-w-[400px] px-4 py-8 space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="text-xl font-bold tracking-wide">
              {truncate(buildingComponent.uuid, { length: 20 })}
            </h4>
            <Button
              variant="ghost"
              onClick={() => {
                const searchParams = new URLSearchParams(
                  window.location.search
                );
                searchParams.delete("designDrawingComponentMetadataUuid");
                router.push(
                  `${window.location.pathname}?${searchParams.toString()}`
                );
              }}
            >
              <XIcon className="" />
            </Button>
          </div>
          <div className="overflow-y-scroll h-[calc(100vh-112px)] pb-[112px] p-2 custom-scrollbar">
            <div className="space-y-8">
              {/* basic info */}
              <div className="flex flex-col gap-2 border-b pb-8">
                <div className="text-sm">
                  <div className="font-bold">Justificativa:</div>
                  <p className="">{componentData.justification}</p>
                </div>
              </div>

              {/* bom */}
              <div className="flex flex-col gap-2 border-b pb-8">
                <div className="">
                  <div className="font-bold mb-4">Cálculo de Quantidade</div>
                  <div className="flex flex-col gap-2">
                    <div className="text-sm">
                      <div className="font-bold">Raciocínio:</div>
                      <p className="">{bom.rationale ?? "--"}</p>
                    </div>

                    <div className="text-sm">
                      <div className="font-bold">Volume de concreto:</div>
                      <p className="">
                        {bom.concrete_volume_in_cubic_meters?.toFixed(2) ??
                          "N/A"}
                        m³
                      </p>
                    </div>
                    <div className="text-sm">
                      <div className="font-bold">Peso do aço:</div>
                      <p className="">
                        {bom.steel_weight_in_kilograms?.toFixed(2) ?? "N/A"} kg
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
