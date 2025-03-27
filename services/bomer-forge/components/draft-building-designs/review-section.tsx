"use client";
import { DownloadIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import Asterisc from "../ui/icons/asterisc";

export function ReviewSection() {
  return (
    <div className="p-8 space-y-8 w-full">
      <div className="flex flex-col space-y-2">
        <h2 className="font-bold text-xl">Avaliação</h2>
        <div className="flex items-center gap-2">
          <Asterisc className="text-purple-500" />
          <span className="text-sm">
            Abaixo estão os materiais que foram selecionados para o projeto.
            Foram levados em consideração os materiais que foram selecionados
            para o projeto e os materiais que foram selecionados para o projeto.
          </span>
        </div>
      </div>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h4 className="font-bold text-xl">Medidas</h4>
          <Button variant="tertiary">
            <DownloadIcon className="w-4 h-4" /> Download report
          </Button>
        </div>
      </div>
    </div>
  );
}
