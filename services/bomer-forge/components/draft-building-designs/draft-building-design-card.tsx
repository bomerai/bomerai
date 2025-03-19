import { Card, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowUpRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { DraftBuildingDesign } from "@/lib/rest-types";
import { formatDate } from "@/lib/utils";

export interface DraftBuildingDesignCardProps {
  draftBuildingDesign: DraftBuildingDesign;
}

export default function DraftBuildingDesignCard({
  draftBuildingDesign,
}: DraftBuildingDesignCardProps) {
  const router = useRouter();

  const getStatus = (status: DraftBuildingDesign["status"]) => {
    switch (status) {
      case "DRAFT":
        return "";
      case "IN_PROGRESS":
        return "Em andamento";
      case "PUBLISHED":
        return "Publicado";
    }
  };

  const getPhase = (phase: DraftBuildingDesign["phase"]) => {
    switch (phase) {
      case "PHASE_1":
        return "Cálculo de estrutura";
      case "PHASE_2":
        return "Cálculo de alvenaria";
      case "PHASE_3":
        return "Cálculo de telhado";
    }
  };

  const getPhaseDescription = (phase: DraftBuildingDesign["phase"]) => {
    switch (phase) {
      case "PHASE_1":
        return "Vigas, pilares, lajes, betões, etc.";
      case "PHASE_2":
        return "Muros, pilares, lajes, betões, etc.";
      case "PHASE_3":
        return "Telhas, estrutura de madeira, etc.";
    }
  };

  return (
    <Card
      className="h-[300px] justify-between flex flex-col hover:cursor-pointer"
      onClick={() =>
        router.push(`/building-designs/${draftBuildingDesign.uuid}`)
      }
    >
      <CardHeader>
        <CardTitle className="space-y-2">
          <div className="flex justify-between">
            <div>
              <p className="text-sm font-medium tracking-wide text-anchor">
                {getStatus(draftBuildingDesign.status)}
              </p>
              <h4 className="font-bold text-lg">
                {getPhase(draftBuildingDesign.phase)}
              </h4>
              <p className="text-sm text-muted-foreground">
                {getPhaseDescription(draftBuildingDesign.phase)}
              </p>
            </div>
            <ArrowUpRight className="w-4 h-4 mr-1" />
          </div>
        </CardTitle>
      </CardHeader>
      <CardFooter>
        <div className="flex justify-between border-t-2 w-full py-4">
          <div className="flex justify-between text-xs text-muted-foreground">
            <div>
              <p>
                <span className="font-bold">Data de criação:</span>{" "}
                {formatDate(draftBuildingDesign.created_at)}
              </p>
            </div>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
