import { Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { components } from "@/lib/rest-api.types";
import { InfoIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import z from "zod";

const componentDataSchema = z.object({
  code: z.string(),
  type: z.string(),
  width: z.number().nullable(),
  height: z.number().nullable(),
  length: z.number().nullable(),
  stirrups: z.string().nullable(),
  longitudinal_rebar: z.string().nullable(),
});

export function ColumnComponentCard({
  column,
  buildingDesignUuid,
}: {
  column: components["schemas"]["DraftBuildingDesignBuildingComponent"];
  buildingDesignUuid: string;
}) {
  const componentData = componentDataSchema.parse(
    column.building_component.component_data
  );

  const router = useRouter();

  const handleClick = () => {
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.set("columnComponentUuid", column.building_component.uuid);
    router.push(`/buildings/${buildingDesignUuid}?${searchParams.toString()}`);
  };

  return (
    <div
      className="p-6 bg-white border hover:ring-2 ring-offset-1 hover:ring-anchor hover:cursor-pointer rounded flex items-start justify-between gap-12"
      onClick={handleClick}
    >
      <div className="flex flex-col space-y-8 flex-1">
        <div className="flex flex-col gap-4">
          <h4 className="font-semibold">Pilar: {componentData.code}</h4>
        </div>

        {componentData.type === "COLUMN" && (
          <div className="flex flex-col space-y-4">
            <div className="grid grid-cols-4 gap-4">
              <div className="flex flex-col">
                <div className="flex items-center gap-2">
                  <h4 className="font-medium text-sm text-muted-foreground">
                    Dimensões (cm)
                  </h4>
                  <InfoIcon className="w-4 h-4" />
                </div>
                <div className="font-semibold">
                  {componentData.width}x{componentData.length}x
                  {componentData?.height ?? 0}
                </div>
              </div>
              <div className="flex flex-col border-l pl-4">
                <div className="flex items-center gap-2">
                  <h4 className="font-medium text-sm text-muted-foreground">
                    Arm. Long.
                  </h4>
                </div>
                <div className="font-semibold">
                  {componentData.longitudinal_rebar}
                </div>
              </div>

              <div className="flex flex-col border-l pl-4">
                <div className="flex items-center gap-2">
                  <h4 className="font-medium text-sm text-muted-foreground">
                    Estribos
                  </h4>
                  <InfoIcon className="w-4 h-4" />
                </div>
                <div className="font-semibold">{componentData.stirrups}</div>
              </div>
            </div>
          </div>
        )}
      </div>
      <div>
        <Button variant="ghost">
          <Pencil className="w-4 h-4 text-anchor" />
        </Button>
        <Button variant="ghost">
          <Trash2 className="w-4 h-4 text-anchor" />
        </Button>
      </div>
    </div>
  );
}
