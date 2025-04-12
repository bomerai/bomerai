"use client";

import Link from "next/link";
import {
  ChevronRight,
  ChevronLeftIcon,
  PyramidIcon,
  ArrowBigRight,
  ArrowRight,
} from "lucide-react";
import { useParams } from "next/navigation";
import { fetcher } from "@/lib/api-fetcher";
import { components } from "@/lib/rest-api.types";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Asterisc from "@/components/ui/icons/asterisc";

export default function BuildingDesignModulesPage() {
  const { uuid } = useParams();

  const { data: draftBuildingDesign } = useQuery({
    queryKey: ["draftBuildingDesign", uuid],
    queryFn: () =>
      fetcher<components["schemas"]["DraftBuildingDesign"]>(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${uuid}/`
      ),
  });

  return (
    <div className="flex flex-col flex-grow relative overflow-y-auto h-screen">
      <div className="flex items-center justify-between px-8 py-4 border-b h-14">
        <nav className="font-medium text-xl flex items-center gap-2">
          <Link
            href="/projects"
            className="hover:text-primary text-muted-foreground"
          >
            Projetos
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <Link
            href={`/projects/${uuid}`}
            className="hover:text-primary text-muted-foreground"
          >
            Projeto 1
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <Link
            className="leading-[54px] text-muted-foreground"
            href={`/building-designs/${uuid}/structure-calculation`}
          >
            {draftBuildingDesign?.name}
          </Link>
          <ChevronRight className="w-4 h-4 text-muted-foreground" />
          <span className="leading-[54px] font-bold">Módulos de cálculo</span>
        </nav>
      </div>
      <div className="p-8 space-y-8 w-full">
        <Link
          href={`/building-designs/${uuid}`}
          className="flex items-center gap-2"
        >
          <ChevronLeftIcon className="w-4 h-4" />
          Voltar
        </Link>
        <div className="flex flex-col space-y-12">
          <div>
            <h2 className="font-bold text-2xl mb-4">Módulos de cálculo</h2>
            <p className="w-1/2">
              Cada módulo de cálculo possui um conjunto de cálculos para uma
              parte específica da construção.
            </p>
          </div>
          <div className="grid grid-cols-4">
            <Card className="">
              <CardHeader className="flex flex-row items-center space-y-0">
                <Asterisc className="w-4 h-4 mr-4 text-anchor" />
                <CardTitle className="text-xl">Cálculo de estrutura</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm mb-8">
                  Cálculo de estrutura é um módulo de cálculo que calcula a
                  estrutura da construção como pilares, vigas, lajes e betão.
                </p>
                <div className="flex justify-end">
                  <Button variant="ai">
                    Começar
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
