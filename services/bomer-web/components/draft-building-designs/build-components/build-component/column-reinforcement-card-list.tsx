import { ColumnReinforcementMetadata } from "@/lib/rest-types";
import { z } from "zod";

const columnReinforcementSchema = z.object({
  pillar_id: z.string().nullable(),
  starter_rebar: z.string().nullable(),
  pillar_perimeter: z.string().nullable(),
  stirrup_diameter: z.string().nullable(),
  longitudinal_rebar: z.string().nullable(),
  starter_rebar_number: z.number().nullable(),
  stirrups_distribution: z.array(
    z.object({
      number: z.number().nullable(),
      spacing: z.string().nullable(),
      interval: z.string().nullable(),
    })
  ),
  cost_breakdown: z
    .array(
      z.object({
        name: z.string().optional(),
        costs: z.array(
          z.object({
            name: z.string().optional(),
            value: z.string().optional(),
          })
        ),
      })
    )
    .optional(),
  total_cost: z.string().optional(),
});

const componentMetadataSchema = z.array(
  z.object({
    columns: z.array(columnReinforcementSchema),
  })
);

export default function ColumnReinforcementCardList({
  columnReinforcementMetadata,
}: {
  columnReinforcementMetadata: ColumnReinforcementMetadata;
}) {
  const metadata = componentMetadataSchema.parse(
    columnReinforcementMetadata.component_metadata
  );
  return (
    <div className="w-full">
      <p className="text-sm text-gray-500">
        {columnReinforcementMetadata.component_metadata.length} pilares
      </p>
      <div className="grid grid-cols-1 w-full md:grid-cols-2 lg:grid-cols-1 gap-4">
        {metadata.map((m) =>
          m.columns.map((c) => (
            <div
              key={c.pillar_id}
              className="flex flex-col bg-white border rounded p-4"
            >
              <p>
                <span className="font-bold">ID:</span> {c.pillar_id}
              </p>
              <p>
                <span className="font-bold">Arm. Long.:</span>{" "}
                {c.longitudinal_rebar}
              </p>
              <p>
                <span className="font-bold">Arranque:</span> {c.starter_rebar}
              </p>
              <p>
                <span className="font-bold">Perímetro:</span>{" "}
                {c.pillar_perimeter}
              </p>
              <p>
                <span className="font-bold">Armadura transversal:</span>{" "}
                {c.stirrup_diameter}
              </p>
              <p>
                <span className="font-bold">Número de arranque:</span>{" "}
                {c.starter_rebar_number}
              </p>
              <div className="mb-4">
                <p>
                  <span className="font-bold">Distribuição:</span>
                </p>
                {c.stirrups_distribution.map((s) => (
                  <p key={s.number} className="text-sm">
                    {s.number} estribos,{s.spacing}cm de separação e{" "}
                    {s.interval}
                    cm de intervalo.
                  </p>
                ))}
              </div>
              <hr />
              <div className="mt-4">
                <p className="text-lg mb-4">
                  <span className="font-bold">Custo:</span> {c.total_cost}
                </p>
                <div className="flex flex-col space-y-2">
                  {c.cost_breakdown?.map((c) => (
                    <div key={c.name}>
                      {c.name}
                      <div className="flex flex-col">
                        {c.costs.map((cost) => (
                          <div key={cost.name} className="text-sm">
                            <span className="font-bold">{cost.name}</span>:{" "}
                            {cost.value}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
