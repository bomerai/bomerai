"use client";

import { Button } from "@/components/ui/button";
import { PlusIcon, ChevronRight } from "lucide-react";
import Link from "next/link";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import DraftBuildingDesignCard from "@/components/draft-building-designs/draft-building-design-card";
import { useParams } from "next/navigation";
import DraftBuildingDesignForm from "@/components/draft-building-designs/draft-building-design-form";
import { useQuery } from "@tanstack/react-query";
import { components } from "@/lib/rest-api.types";

const getProject = async (
  projectUuid: string
): Promise<components["schemas"]["Project"]> => {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/projects/${projectUuid}/`,
    {
      credentials: "include",
      mode: "cors",
    }
  );
  return res.json();
};

const getDraftBuildingDesigns = async (
  projectUuid: string
): Promise<components["schemas"]["DraftBuildingDesign"][]> => {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/?project_uuid=${projectUuid}`,
    {
      credentials: "include",
      mode: "cors",
    }
  );
  return res.json();
};

export default function ProjectPage() {
  const { uuid: projectUuid } = useParams();

  const {
    data: project,
    isLoading: isProjectLoading,
    error: projectError,
  } = useQuery({
    queryKey: ["project", projectUuid],
    queryFn: () => getProject(projectUuid as string),
  });

  const {
    data: draftBuildingDesigns,
    isLoading: isDraftBuildingDesignsLoading,
    error: draftBuildingDesignsError,
  } = useQuery({
    queryKey: ["draftBuildingDesigns", projectUuid],
    queryFn: () => getDraftBuildingDesigns(projectUuid as string),
  });

  if (isProjectLoading || isDraftBuildingDesignsLoading) {
    return <div>Loading...</div>;
  }

  if (projectError || draftBuildingDesignsError) {
    return (
      <div>
        Error: {projectError?.message || draftBuildingDesignsError?.message}
      </div>
    );
  }

  if (!draftBuildingDesigns && !project) {
    return <div>No draft building designs found</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between px-8 py-4 border-b">
        <nav className="font-medium text-xl flex items-center gap-2">
          <Link href="/projects" className="hover:text-primary">
            Projetos
          </Link>
          <ChevronRight className="w-4 h-4" />
          <Link
            href={`/projects/${projectUuid}`}
            className="hover:text-primary"
          >
            {project?.name}
          </Link>
        </nav>
      </div>
      {/* header actions */}
      <div className="flex items-center justify-end px-8 py-4">
        <AddNewDraftBuildingDesignDialog />
      </div>

      <div className="px-8 py-4">
        <h1 className="font-bold mb-4 text-xl">Construções</h1>
        <p className="text-sm text-muted-foreground mb-4">
          Cada construção possui um conjunto de módulos de cálculo. Como cálculo
          de estrutura, piso, telhado, etc.
        </p>
        <div className="grid grid-cols-3 gap-4">
          {draftBuildingDesigns?.map((draftBuildingDesign) => (
            <DraftBuildingDesignCard
              key={draftBuildingDesign.uuid}
              draftBuildingDesign={draftBuildingDesign}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export function AddNewDraftBuildingDesignDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="tertiary">
          <PlusIcon className="w-4 h-4 mr-1" />
          Adicionar construção
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Adicionar uma construção</DialogTitle>
          <DialogDescription>
            A construção é o que você quer construir. Ela pode ser um edifício,
            uma casa, um galpão, etc.
          </DialogDescription>
        </DialogHeader>
        <div className="flex items-center space-x-2">
          <DraftBuildingDesignForm />
        </div>
        <DialogFooter className="sm:justify-start">
          <DialogClose asChild>
            <Button type="button" variant="secondary">
              Fechar
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
