import { Button } from "@/components/ui/button";
import { Pencil, Trash2 } from "lucide-react";
import { DesignDrawingPlan } from "@/lib/rest-types";
export default function FootingPlanCard({
  footingPlan,
}: {
  footingPlan: DesignDrawingPlan;
}) {
  return (
    <div className="p-6 bg-white border rounded flex items-start justify-between gap-12">
      <div className="flex flex-col space-y-8 flex-1">
        <div>
          <h4 className="font-semibold">{footingPlan.name}</h4>
          <p className="text-sm text-muted-foreground">
            {footingPlan.justification}
          </p>
        </div>

        <div className="flex flex-col space-y-4">
          <div className="grid grid-cols-4 gap-4 text-xs">
            <div className="flex flex-col">
              <div className="font-medium">Largura (cm)</div>
              <div className="">
                {(footingPlan?.plan_metadata || { width: 0 }).width}
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Comprimento (cm)</div>
              <div className="">
                {(footingPlan?.plan_metadata || { length: 0 }).length}
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Altura (cm)</div>
              <div className="">
                {(footingPlan?.plan_metadata || { height: 0 }).height}
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Referências</div>
              <div className="italic">Aguardando pilares</div>
            </div>
          </div>
          <hr className="w-full border-t border/60" />
          <div className="grid grid-cols-4 gap-4 text-xs">
            <div className="flex flex-col">
              <div className="font-medium">Armadura Inf. X</div>
              <div className="">
                {
                  (
                    footingPlan?.plan_metadata || {
                      bottom_reinforcement_x: 0,
                    }
                  ).bottom_reinforcement_x
                }
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Armadura Inf. Y</div>
              <div className="">
                {
                  (
                    footingPlan?.plan_metadata || {
                      bottom_reinforcement_y: 0,
                    }
                  ).bottom_reinforcement_y
                }
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Armadura Sup. X</div>
              <div className="">
                {
                  (
                    footingPlan?.plan_metadata || {
                      top_reinforcement_x: 0,
                    }
                  ).top_reinforcement_x
                }
              </div>
            </div>
            <div className="flex flex-col border-l pl-4">
              <div className="font-medium">Armadura Sup. Y</div>
              <div className="">
                {
                  (
                    footingPlan?.plan_metadata || {
                      top_reinforcement_y: 0,
                    }
                  ).top_reinforcement_y
                }
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
  );
}
