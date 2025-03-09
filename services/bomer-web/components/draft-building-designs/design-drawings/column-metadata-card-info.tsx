import { Button } from "@/components/ui/button";
import { Pencil, Trash2 } from "lucide-react";
import { DesignDrawingComponentMetadata } from "@/lib/rest-types";
import { useRouter } from "next/navigation";

type ColumnStirrupsDistribution = {
  interval: string;
  number: number;
  spacing: number;
};

type ColumnStarterRebarStirrupsDistribution = {
  number: number;
};

type ColumnMetadata = {
  code: string;
  width: number;
  description: string;
  length: number;
  height: number;
  longitudinal_rebar: string;
  longitudinal_rebar_stirrups_distribution: ColumnStirrupsDistribution[];
  starter_rebar: string;
  starter_rebar_stirrups_distribution: ColumnStarterRebarStirrupsDistribution[];
  stirrup_diameter: string;
  floors: string[];
  type: string;
};

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

export default function ColumnMetadataCardInfo({
  column,
  buildingDesignUuid,
}: {
  column: DesignDrawingComponentMetadata;
  buildingDesignUuid: string;
}) {
  const data = column.data as ColumnMetadata;

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
            {data.code} -{" "}
            {data.floors.map((floor) => getFloorName(floor)).join(", ")}
          </h4>
        </div>

        {data.type === "0" && (
          <div className="flex flex-col space-y-4">
            <h4 className="text-xs font-bold text-anchor uppercase">
              Dimensões
            </h4>
            <div className="grid grid-cols-4 gap-4 text-xs">
              <div className="flex flex-col">
                <div className="font-medium">Largura (cm)</div>
                <div className="">{data.width}</div>
              </div>
              <div className="flex flex-col border-l pl-4">
                <div className="font-medium">Comprimento (cm)</div>
                <div className="">{data.length}</div>
              </div>
              <div className="flex flex-col border-l pl-4">
                <div className="font-medium">Altura (cm)</div>
                <div className="">{data.height}</div>
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
                  <div className="">{data.longitudinal_rebar}</div>
                </div>
                <div className="flex flex-col border-l pl-4">
                  <div className="font-medium">Estribos</div>
                  <div className="">
                    {data.longitudinal_rebar_stirrups_distribution.map(
                      (distribution) => (
                        <div key={distribution.interval}>
                          {`${distribution.number}${data.stirrup_diameter}//${distribution.spacing}cm`}
                        </div>
                      )
                    )}
                  </div>
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
                  <div className="">{data.starter_rebar}</div>
                </div>
                <div className="flex flex-col border-l pl-4">
                  <div className="font-medium">Estribos</div>
                  <div className="">
                    {data.starter_rebar_stirrups_distribution.map(
                      (distribution) =>
                        `${distribution.number}${data.stirrup_diameter}//`
                    )}
                  </div>
                </div>
                <div className="flex flex-col border-l pl-4">
                  <div className="font-medium">Altura do arranque (cm)</div>
                  <div className="italic">
                    A altura do arranque será definida quando for feita a
                    leitura da planta
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        {data.type === "1" && (
          <div className="flex flex-col space-y-4">
            <h4 className="text-xs font-bold text-anchor uppercase">
              Dimensões
            </h4>
            <div className="grid grid-cols-4 gap-4 text-xs">
              <div className="flex flex-col">
                <div className="font-medium">Descrição</div>
                <div className="">{data.description}</div>
              </div>
            </div>
          </div>
        )}
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
  );
}
