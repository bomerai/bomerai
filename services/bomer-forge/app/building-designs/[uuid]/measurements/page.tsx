"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { fetcher } from "@/lib/api-fetcher";
import { components } from "@/lib/rest-api.types";
import { useQuery } from "@tanstack/react-query";
import { ChevronLeftIcon, ChevronRight, InfoIcon } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function MeasurementsPage() {
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
          <span className="leading-[54px] font-bold">Medidas</span>
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
            <h2 className="font-bold text-2xl mb-4">Medidas</h2>
            <p className="w-1/2">
              Comece medindo o projeto de estrutura para calcular a quantidade
              de materiais necessários. Leia as instruções abaixo para saber
              como medir o projeto de estrutura automaticamente 🤖.
            </p>
          </div>
          <div className="grid grid-cols-3">
            <Card className="">
              <CardHeader className="flex flex-row items-center space-y-0">
                <InfoIcon className="w-4 h-4 mr-4" />
                <CardTitle className="text-lg">Como medir o projeto?</CardTitle>
              </CardHeader>
              <CardContent>
                <p>
                  Para medir o projeto, você precisa ter um arquivo PDF do
                  projeto de estrutura.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
