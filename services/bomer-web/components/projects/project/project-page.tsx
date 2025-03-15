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

import { DraftBuildingDesign, Project } from "@/lib/rest-types";
import useSWR from "swr";
import DraftBuildingDesignCard from "@/components/draft-building-designs/draft-building-design-card";
import { useParams } from "next/navigation";
import DraftBuildingDesignForm from "@/components/draft-building-designs/draft-building-design-form";

const fetcher = <T,>(url: string) =>
  fetch(url, {
    credentials: "include",
    mode: "cors",
  }).then((res) => res.json() as Promise<T>);

export default function ProjectPage() {
  const { uuid: projectUuid } = useParams();

  const {
    data: project,
    isLoading: isProjectLoading,
    error: projectError,
  } = useSWR<Project>(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/projects/${projectUuid}/`,
    fetcher
  );

  const {
    data: draftBuildingDesigns,
    isLoading: isDraftBuildingDesignsLoading,
    error: draftBuildingDesignsError,
  } = useSWR<DraftBuildingDesign[]>(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/?project_uuid=${projectUuid}`,
    fetcher
  );

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
        <AddProjectDialog />
      </div>

      <div className="px-8 py-4">
        <h1 className="font-bold mb-4 text-xl">Cálculos</h1>
        <p className="text-sm text-muted-foreground mb-4">
          Cada módulo tem um cálculo próprio.
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

export function AddProjectDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="tertiary">
          <PlusIcon className="w-4 h-4 mr-1" />
          Adicionar novo cálculo
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Adicionar uma construção</DialogTitle>
          <DialogDescription>
            Adicione uma nova construção para começar a trabalhar.
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
