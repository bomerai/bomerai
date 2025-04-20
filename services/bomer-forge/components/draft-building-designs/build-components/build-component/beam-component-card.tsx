import { components } from "@/lib/rest-api.types";
import { InfoIcon } from "lucide-react";
import z from "zod";

const beamComponentSchema = z.object({
  width: z.number(),
  length: z.number(),
  height: z.number(),
  longitudinal_reinforcement_diameter: z.number(),
  longitudinal_reinforcement_quantity: z.number(),
  stirrups_diameter: z.number(),
  stirrups_quantity: z.number(),
  stirrups_spacing: z.number(),
});

export function BeamComponentCard({
  beam,
}: {
  beam: components["schemas"]["DraftBuildingDesignBuildingComponent"];
}) {
  const componentData = beamComponentSchema.parse(
    beam.building_component.component_data
  );
  return (
    <div className="p-6 border rounded space-y-2">
      <div className="flex flex-col">
        <span className="text-xs text-muted-foreground">Viga</span>
        <h4 className="font-bold">C.2.1</h4>
      </div>
      <div className="flex items-center gap-4">
        <div className="border-r border-r-border pr-4">
          <div className="flex items-center gap-2">
            <h4 className="font-medium text-sm text-muted-foreground">
              Dimensões (cm)
            </h4>
            <InfoIcon className="w-4 h-4 text-muted-foreground" />
          </div>
          <div className="font-semibold">
            {componentData.width}x{componentData.height}x{componentData.length}
          </div>
        </div>
      </div>
    </div>
  );
}
