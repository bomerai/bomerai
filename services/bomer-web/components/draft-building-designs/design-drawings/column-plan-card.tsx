import { Button } from "@/components/ui/button";
import { AlertCircle, Pencil, Trash2 } from "lucide-react";
import { DesignDrawingPlan } from "@/lib/rest-types";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

type Column = DesignDrawingPlan["plan_metadata"]["columns"][0];

export default function ColumnPlanCard({
  column,
}: {
  column: DesignDrawingPlan;
}) {
  return (
    <>
      {column?.plan_metadata?.columns.map((column: Column) => (
        <div
          key={column.uuid}
          className="p-6 bg-white border rounded flex items-start justify-between gap-12"
        >
          <div className="flex flex-col space-y-8 flex-1">
            <div>
              <h4 className="font-semibold">{column.code}</h4>
              <p className="text-sm text-muted-foreground">
                {column.justification}
              </p>
              <br />
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Atenção</AlertTitle>
                <AlertDescription>
                  Edite os pilares para definir onde se encontram as armaduras e
                  estribos.
                </AlertDescription>
              </Alert>
            </div>

            <div className="flex flex-col space-y-4">
              <h4 className="text-xs font-bold text-anchor uppercase">
                Dimensões
              </h4>
              <div className="grid grid-cols-4 gap-4 text-xs">
                <div className="flex flex-col">
                  <div className="font-medium">Largura (cm)</div>
                  <div className="">{column.width}</div>
                </div>
                <div className="flex flex-col border-l pl-4">
                  <div className="font-medium">Comprimento (cm)</div>
                  <div className="">{column.length}</div>
                </div>
                <div className="flex flex-col border-l pl-4">
                  <div className="font-medium">Altura (cm)</div>
                  <div className="">{column.height}</div>
                </div>
                <div className="flex flex-col border-l pl-4">
                  <div className="font-medium">Sapata</div>
                  <div className="italic">--</div>
                </div>
              </div>
              <hr className="w-full border-t border/60" />
              <div className="flex flex-col space-y-2">
                <h4 className="text-xs font-bold text-anchor uppercase">
                  Armadura
                </h4>
                <div className="grid grid-cols-4 gap-4 text-xs">
                  <div className="flex flex-col">
                    <div className="font-medium">Diametro</div>
                    <div className="">{column.longitudinal_rebar_diameter}</div>
                  </div>
                  <div className="flex flex-col border-l pl-4">
                    <div className="font-medium">Numero de estribos</div>
                    <div className="">
                      {column.longitudinal_rebar_stirrups_number}
                    </div>
                  </div>
                  <div className="flex flex-col border-l pl-4">
                    <div className="font-medium">Espaçamento (cm)</div>
                    <div className="">
                      {column.longitudinal_rebar_stirrups_spacing}
                    </div>
                  </div>
                  <div className="flex flex-col border-l pl-4">
                    <div className="font-medium">Nível</div>
                    <div className="">{column.level}</div>
                  </div>
                </div>
              </div>
              <hr className="w-full border-t border/60" />
              <div className="flex flex-col space-y-2">
                <h4 className="text-xs font-bold text-anchor uppercase">
                  Arranque
                </h4>
                <div className="grid grid-cols-4 gap-4 text-xs">
                  <div className="flex flex-col">
                    <div className="font-medium">Diametro</div>
                    <div className="">{column.starter_rebar_diameter}</div>
                  </div>
                  <div className="flex flex-col border-l pl-4">
                    <div className="font-medium">Numero de estribos</div>
                    <div className="">
                      {column.starter_rebar_stirrups_number}
                    </div>
                  </div>
                  <div className="flex flex-col border-l pl-4">
                    <div className="font-medium italic">Espaçamento</div>
                    <div className="italic">A definir...</div>
                  </div>
                </div>
              </div>
              <hr className="w-full border-t border/60" />
              <div className="flex flex-col space-y-2">
                <h4 className="text-xs font-bold text-anchor uppercase">
                  Estribos
                </h4>
                <div className="grid grid-cols-4 gap-4 text-xs">
                  <div className="flex flex-col">
                    <div className="font-medium">Diametro</div>
                    <div className="">{column.stirrup_diameter}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div>
            <Button variant="ghost">
              <Trash2 className="w-4 h-4 text-anchor" />
            </Button>
            <Button variant="ghost">
              <Pencil className="w-4 h-4 text-anchor" />
            </Button>
          </div>
        </div>
      ))}
    </>
  );
}
