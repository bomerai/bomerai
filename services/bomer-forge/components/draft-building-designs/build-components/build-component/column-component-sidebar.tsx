import { XIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Skeleton } from "@/components/ui/skeleton";
import { components } from "@/lib/rest-api.types";
import { fetcher } from "@/lib/api-fetcher";
import z from "zod";

const componentDataSchema = z.object({
  code: z.string(),
  type: z.string(),
  width: z.number().nullable(),
  floors: z.array(z.string()),
  height: z.number().nullable(),
  length: z.number().nullable(),
  footing_uuid: z.string().nullable(),
  starter_rebar: z.string().nullable(),
  stirrup_diameter: z.string().nullable(),
  longitudinal_rebar: z.string().nullable(),
  starter_rebar_height: z.number().nullable(),
  starter_rebar_stirrups_distribution: z.array(
    z.object({
      number: z.number(),
    })
  ),
  longitudinal_rebar_stirrups_distribution: z.array(
    z.object({
      number: z.number(),
      spacing: z.number(),
      interval: z.string(),
    })
  ),
  description: z.string().optional(),
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

export function ColumnComponentSidebar({
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

  const bom = bomSchema.safeParse(buildingComponent?.component_bom);
  console.log(bom);

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
              {componentData.code}
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
          <div className="overflow-y-scroll h-[calc(100vh-112px)] p-2 custom-scrollbar">
            <div className="space-y-8">
              {/* basic info */}
              <div className="flex flex-col gap-2 border-b pb-8">
                <div className="text-sm">
                  <div className="font-bold">Justificativa:</div>
                </div>
              </div>

              {/* bom */}
              <div className="flex flex-col gap-2 border-b pb-8">
                <div className="">
                  <div className="font-bold mb-4">Especificações</div>
                  <div className="flex flex-col gap-2">
                    <div className="text-sm">
                      <div className="font-bold">Dimensões:</div>
                      <p className="">
                        {componentData?.width}x{componentData?.length}x
                        {componentData?.height}cm
                      </p>
                    </div>
                    <div className="text-sm">
                      <div className="font-bold">Tipo:</div>
                      <p className="">{componentData?.type}</p>
                    </div>
                    <div className="text-sm">
                      <div className="font-bold">
                        Diâmetro da armadura longitudinal:
                      </div>
                      <p className="">{componentData?.longitudinal_rebar}</p>
                    </div>
                    <div className="text-sm">
                      <div className="font-bold">
                        Número de estribos e espaçamento:
                      </div>
                      <div className="">
                        {componentData.longitudinal_rebar_stirrups_distribution.map(
                          (item) => (
                            <p key={item.interval}>
                              [{item.interval}] - {item.number}u//{item.spacing}
                              cm
                            </p>
                          )
                        )}
                      </div>
                    </div>
                    <div className="text-sm">
                      <div className="font-bold">Arranque:</div>
                      <p className="">
                        Altura: {componentData?.starter_rebar_height || 0}cm
                      </p>
                      <p className="">
                        Diâmetro: {componentData?.starter_rebar || 0}
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
