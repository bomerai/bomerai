import { XIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Skeleton } from "@/components/ui/skeleton";
import { components } from "@/lib/rest-api.types";
import { fetcher } from "@/lib/api-fetcher";
import z from "zod";
import { Separator } from "@/components/ui/separator";

const componentDataSchema = z.object({
  code: z.string(),
  type: z.string(),
  width: z.number().optional(),
  height: z.number().optional(),
  length: z.number().optional(),
  longitudinal_rebar: z.string().optional(),
  stirrups: z.string().optional(),
  bom: z.object({
    steel_weight: z.number().optional(),
    concrete_volume: z.number().optional(),
    rationale: z.string().optional(),
  }),
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
              {/* bom */}
              <div className="flex flex-col space-y-4">
                <div className="">
                  <div className="font-bold mb-4 text-lg">Especificações</div>
                  <div className="flex flex-col text-sm">
                    <div className="flex gap-2 items-center">
                      <div className="">Dimensões:</div>
                      <p className="font-semibold">
                        {componentData?.width}x{componentData?.length}x
                        {componentData?.height}cm
                      </p>
                    </div>
                    <div className="flex gap-2 items-center">
                      <div className="">Diâmetro da armadura longitudinal:</div>
                      <p className="font-semibold">
                        {componentData?.longitudinal_rebar}
                      </p>
                    </div>
                  </div>
                </div>
                <Separator />
                <div className="">
                  <div className="font-bold mb-4 text-lg">Materiais</div>
                  <div className="flex flex-col gap-2">
                    <div className="">
                      <div className="text-muted-foreground text-sm">
                        Peso do aço:
                      </div>
                      <p className="font-bold">
                        {componentData?.bom?.steel_weight}kg
                      </p>
                    </div>
                    <div className="">
                      <div className="text-muted-foreground text-sm">
                        Volume de concreto:
                      </div>
                      <p className="font-bold">
                        {componentData?.bom?.concrete_volume}m³
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
