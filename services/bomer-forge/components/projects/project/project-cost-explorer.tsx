import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowUpRight, Store } from "lucide-react";
import Image from "next/image";

export default function ProjectCostExplorer() {
  return (
    <div className="flex flex-1 flex-col gap-4 space-y-8 p-8 w-full">
      <div className="flex flex-col space-y-6">
        <h2 className="text-xl font-bold">Planta baixa</h2>
        <div className="w-full bg-white rounded border p-4">
          <Image
            src="/images/floor_plan.png"
            alt="Planta baixa"
            className="mx-auto"
            width={400}
            height={400}
          />
        </div>
      </div>
      <div className="flex flex-col space-y-6">
        <h2 className="text-xl font-bold">Orçamentos</h2>
        <div className="flex flex-col gap-2 hover:cursor-pointer hover:bg-gray-50 border rounded">
          <div className="p-4 flex items-center justify-between">
            <div className="flex flex-col">
              <span className="font-bold text-2xl font-mono">
                23.000,00 eur
              </span>
              <span className="text-xs text-muted-foreground">
                Custo estimado para construção
              </span>
            </div>
            <div className="flex gap-2 items-center">
              <Badge variant="outline" className="bg-green-500 text-white">
                Econômico
              </Badge>
              <Button variant="ghost">
                <Store className="w-4 h-4" />
                Lojas
              </Button>
              <Button variant="ghost">
                Ver detalhes
                <ArrowUpRight className="w-4 h-4" />
              </Button>
            </div>
          </div>
          <hr className="border-dashed" />
          <div className="p-4 flex flex-col space-y-2">
            <div className="flex flex-col">
              <p className="font-bold">Descrição:</p>
              <p className="text-sm text-muted-foreground">
                Uma casa construida com blocos de tijolos, chão de pvc e janelas
                de aluminio.
              </p>
            </div>
          </div>
        </div>
        <div className="flex flex-col gap-2 hover:cursor-pointer hover:bg-gray-50 border rounded">
          <div className="p-4 flex items-center justify-between">
            <div className="flex flex-col">
              <span className="font-bold text-2xl font-mono">
                28.000,00 eur
              </span>
              <span className="text-xs text-muted-foreground">
                Custo estimado para construção
              </span>
            </div>
            <div className="flex gap-2 items-center">
              <Button variant="ghost">
                <Store className="w-4 h-4" />
                Lojas
              </Button>
              <Button variant="ghost">
                Ver detalhes
                <ArrowUpRight className="w-4 h-4" />
              </Button>
            </div>
          </div>
          <hr className="border-dashed" />
          <div className="p-4 flex flex-col space-y-2">
            <div className="flex flex-col">
              <p className="font-bold">Descrição:</p>
              <p className="text-sm text-muted-foreground">
                Uma casa construida com blocos de tijolos, chão de pvc e janelas
                de aluminio.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
