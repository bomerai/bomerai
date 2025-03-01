"use client";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { ArrowUpRight, InfoIcon, Store } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { useMemo } from "react";

export default function ExteriorComponentsSection() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const buildingComponentUuid = searchParams.get("buildingComponentUuid");
  const isSelected = useMemo(() => {
    return buildingComponentUuid === "1";
  }, [buildingComponentUuid]);

  return (
    <div className="flex flex-1 flex-col gap-4 space-y-8 p-8 w-full">
      <div className="flex flex-col space-y-6">
        <h2 className="text-xl font-bold">Components Externos</h2>
      </div>
      <div className="flex flex-col space-y-6">
        <h2 className="text-lg font-bold">Fundação</h2>
        <div
          onClick={() => {
            const searchParams = new URLSearchParams(window.location.search);
            searchParams.set("buildingComponentUuid", "1");
            router.push(
              `${window.location.pathname}?${searchParams.toString()}`
            );
          }}
          className={cn(
            "flex flex-col gap-2 hover:cursor-pointer hover:border-primary border rounded p-6 space-y-2 bg-white",
            { "border-primary border-2": isSelected }
          )}
        >
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-lg">Parede externa</h4>
            <div className="flex gap-2 items-center">
              <Button variant="ghost">
                Ver detalhes
                <ArrowUpRight className="w-4 h-4" />
              </Button>
            </div>
          </div>
          <div className="flex flex-row items-center gap-4 border-b border-muted-foreground/10 pb-4">
            <div className="flex flex-col space-y-1 border-r border-muted-foreground/10 pr-4 flex-1">
              <span className="text-sm">Projeção</span>
              <p className="font-bold">Aproximadamente 100m²</p>
            </div>
            <div className="flex flex-col space-y-1 flex-1">
              <div className="text-sm flex items-center gap-2">
                Estimativa de tempo <InfoIcon className="w-4 h-4" />
              </div>
              <p className="font-bold">12 dias</p>
            </div>
          </div>
          <div className="flex flex-row items-center gap-4 pb-4 border-b border-muted-foreground/10">
            <div className="flex flex-col space-y-1 border-muted-foreground/10 pr-4 flex-1">
              <span className="text-sm">Materiais</span>
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2 font-bold">
                  <span className="">Bloco cerâmico</span>
                  <span className="w-1 h-1 rounded-full bg-muted-foreground"></span>
                  <span className="">Argamassa</span>
                  <span className="w-1 h-1 rounded-full bg-muted-foreground"></span>
                  <span className="">Ferragens</span>
                </div>
              </div>
            </div>
            {/* <div className="flex flex-col space-y-1 flex-1">
              <span className="text-sm">Quantidade</span>
              <p className="font-bold">1232 unidades</p>
            </div> */}
          </div>
          <p className="text-sm">
            A parede externa é uma parede de tijolo com 10cm de espessura,
            revestida com argamassa de cimento.
          </p>
        </div>
      </div>
      <div className="flex flex-col space-y-6">
        <h2 className="text-lg font-bold">Cobertura</h2>
        <div
          className={cn(
            "flex flex-col gap-2 hover:cursor-pointer hover:border-primary border rounded p-6 space-y-2 bg-white",
            { "border-primary border-2": false }
          )}
        >
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-lg">Laje</h4>
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
          <div className="flex flex-row items-center gap-4 border-b border-muted-foreground/10 pb-4">
            <div className="flex flex-col space-y-1 border-r border-muted-foreground/10 pr-4 flex-1">
              <span className="text-sm">Projeção</span>
              <p className="font-bold">Aproximadamente 57m²</p>
            </div>
            <div className="flex flex-col space-y-1 flex-1">
              <div className="text-sm flex items-center gap-2">
                Estimativa de tempo <InfoIcon className="w-4 h-4" />
              </div>
              <p className="font-bold">3 dias</p>
            </div>
          </div>
          <div className="flex flex-row items-center gap-4 pb-4 border-b border-muted-foreground/10">
            <div className="flex flex-col space-y-1 border-muted-foreground/10 pr-4 flex-1">
              <span className="text-sm">Materiais</span>
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2 font-bold">
                  <span className="">Cimento</span>
                  <span className="w-1 h-1 rounded-full bg-muted-foreground"></span>
                  <span className="">Pedra</span>
                  <span className="w-1 h-1 rounded-full bg-muted-foreground"></span>
                  <span className="">Agua</span>
                  <span className="w-1 h-1 rounded-full bg-muted-foreground"></span>
                  <span className="">Areia</span>
                  <span className="w-1 h-1 rounded-full bg-muted-foreground"></span>
                  <span className="">Ferragens</span>
                </div>
              </div>
            </div>
            {/* <div className="flex flex-col space-y-1 flex-1">
              <span className="text-sm">Quantidade</span>
              <p className="font-bold">1232 unidades</p>
            </div> */}
          </div>
          <p className="text-sm">
            A parede externa é uma parede de tijolo com 10cm de espessura,
            revestida com argamassa de cimento.
          </p>
        </div>
      </div>
      <div className="flex flex-col space-y-6">
        <h2 className="text-lg font-bold">Tubulação</h2>
        <div
          className={cn(
            "flex flex-col gap-2 hover:cursor-pointer hover:border-primary border rounded p-6 space-y-2 bg-white",
            { "border-primary border-2": false }
          )}
        >
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-lg">Parede externa</h4>
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
          <div className="flex flex-row items-center gap-4 border-b pb-4">
            <div className="flex flex-col space-y-1 border-r pr-4 flex-1">
              <span className="text-sm">Projeção</span>
              <p className="font-bold">Aproximadamente 375m²</p>
            </div>
            <div className="flex flex-col space-y-1 flex-1">
              <span className="text-sm">Estimativa de tempo</span>
              <p className="font-bold">12 dias</p>
            </div>
          </div>
          <div className="flex flex-row items-center gap-4 pb-4 border-b border-muted-foreground/10">
            <div className="flex flex-col space-y-1 border-muted-foreground/10 pr-4 flex-1">
              <span className="text-sm">Materiais</span>
            </div>
          </div>
          <p className="text-sm">
            A parede externa é uma parede de tijolo com 10cm de espessura,
            revestida com argamassa de cimento.
          </p>
        </div>
      </div>
      <div className="flex flex-col space-y-6">
        <h2 className="text-lg font-bold">Fiação</h2>
        <div
          className={cn(
            "flex flex-col gap-2 hover:cursor-pointer hover:border-primary border rounded p-6 space-y-2 bg-white",
            { "border-primary border-2": false }
          )}
        >
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-lg">Parede externa</h4>
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
          <div className="flex flex-row items-center gap-4 border-b pb-4">
            <div className="flex flex-col space-y-1 border-r pr-4 flex-1">
              <span className="text-sm">Projeção</span>
              <p className="font-bold">Aproximadamente 100m²</p>
            </div>
            <div className="flex flex-col space-y-1 flex-1">
              <span className="text-sm">Estimativa de tempo</span>
              <p className="font-bold">12 dias</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
