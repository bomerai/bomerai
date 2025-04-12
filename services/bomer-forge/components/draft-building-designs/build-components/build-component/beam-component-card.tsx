import { PlusIcon } from "lucide-react";

import { Button } from "@/components/ui/button";

export function BeamComponentCard() {
  return (
    <div className="p-4 border rounded space-y-2">
      <div className="flex flex-col">
        <span className="text-xs text-muted-foreground">Viga</span>
        <h4 className="font-bold">C.2.1</h4>
      </div>
      <div className="flex items-center gap-4">
        <div className="border-r border-r-border pr-4">
          Largura: <span className="font-bold">23cm</span>
        </div>
        <div className="border-r border-r-border pr-4">
          Altura: <span className="font-bold">23cm</span>
        </div>
        <div className="flex items-center gap-2">
          Comprimento:{" "}
          <Button variant="link">
            <PlusIcon className="w-4 h-4" />
            Adicionar
          </Button>
        </div>
      </div>
    </div>
  );
}
