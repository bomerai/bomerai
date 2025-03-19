import { Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { components } from "@/lib/rest-api.types";
import { InfoIcon } from "lucide-react";
import { useRouter } from "next/navigation";
import z from "zod";

// {"code": "P2", "type": "COLUMN", "width": 25.0, "floors": ["Fundacao", "Piso 1"], "height": 400.0, "length": 25.0, "footing_uuid": "58213c30-af46-4d9e-8ebf-ba25147c0e2f", "starter_rebar": "4Ø12", "stirrup_diameter": "Ø6", "longitudinal_rebar": "4Ø12", "starter_rebar_height": 55.0, "starter_rebar_stirrups_distribution": [{"number": 3}], "longitudinal_rebar_stirrups_distribution": [{"number": 20, "spacing": 15.0, "interval": "100-400"}, {"number": 7, "spacing": 15.0, "interval": "0-100"}]}

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

function getFloorName(floor: string) {
  switch (floor) {
    case "o":
      return "Fundação";
    case "1o":
      return "Piso 1";
    case "2o":
      return "Piso 2";
    case "3o":
      return "Piso 3";
    case "4o":
      return "Piso 4";
    case "5o":
      return "Piso 5";
    case "6o":
      return "Piso 6";

    default:
      return floor;
  }
}

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

  return (
    <div
      className="p-6 bg-white border rounded flex items-start justify-between gap-12"
      onClick={() => {
        router.push(
          `/building-designs/${buildingDesignUuid}/design-drawings?drawingComponentColumnUuid=${column.uuid}`
        );
      }}
    >
      <div className="flex flex-col space-y-8 flex-1">
        <div className="flex flex-col gap-4">
          <h4 className="font-semibold">
            Pilar: {componentData.code} | Pisos:{" "}
            {componentData.floors
              .map((floor) => getFloorName(floor))
              .join(", ")}
          </h4>
        </div>

        {componentData.type === "COLUMN" && (
          <div className="flex flex-col space-y-4">
            <div className="grid grid-cols-4 gap-4">
              <div className="flex flex-col text-xs">
                <div className="flex items-center gap-2">
                  <h4 className="font-bold">Dimensões</h4>
                  <InfoIcon className="w-4 h-4" />
                </div>
                <div>
                  {componentData.width}x{componentData.length}x
                  {(componentData?.height ?? 0) +
                    (componentData?.starter_rebar_height ?? 0)}
                  cm
                </div>
              </div>
              <div className="flex flex-col text-xs border-l pl-4">
                <div className="flex items-center gap-2">
                  <h4 className="font-bold">Arm. Long.</h4>
                </div>
                <div>{componentData.longitudinal_rebar}</div>
              </div>
              <div className="flex flex-col text-xs border-l pl-4">
                <div className="flex items-center gap-2">
                  <h4 className="font-bold">Arranque</h4>
                </div>
                <div>{componentData.starter_rebar}</div>
              </div>
              <div className="flex flex-col text-xs border-l pl-4">
                <div className="flex items-center gap-2">
                  <h4 className="font-bold">Estribos</h4>
                  <InfoIcon className="w-4 h-4" />
                </div>
                <div className="flex items-center gap-2">
                  {componentData.longitudinal_rebar_stirrups_distribution.map(
                    (distribution) => (
                      <div key={distribution.number}>
                        {`${distribution.number}${componentData.stirrup_diameter}//`}
                      </div>
                    )
                  )}

                  {componentData.starter_rebar_stirrups_distribution.map(
                    (distribution) => (
                      <div key={distribution.number}>
                        {`${distribution.number}${componentData.stirrup_diameter}//`}
                      </div>
                    )
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
        {componentData.type === "COLUMN_IPE" && (
          <div className="flex flex-col space-y-4">
            <h4 className="text-xs font-bold text-anchor uppercase">
              Dimensões
            </h4>
            <div className="grid grid-cols-4 gap-4 text-xs">
              <div className="flex flex-col">
                <div className="font-medium">Descrição</div>
                <div className="">{componentData.description}</div>
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
