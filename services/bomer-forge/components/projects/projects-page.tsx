"use client";

import { Button } from "@/components/ui/button";
import { PlusIcon } from "lucide-react";
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
import ProjectCreateForm from "./project/project-create-form";
import { Project } from "@/lib/rest-types";
import useSWR from "swr";
import ProjectCard from "./project/project-card";

const fetcher = (url: string) =>
  fetch(url, {
    credentials: "include",
    mode: "cors",
  }).then((res) => res.json() as Promise<Project[]>);

export default function ProjectsPage() {
  const {
    data: projects,
    isLoading,
    error,
  } = useSWR<Project[]>(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/projects/`,
    fetcher
  );

  console.log(projects);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!projects) {
    return <div>No projects found</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between px-8 py-4 border-b">
        <nav className="font-medium text-xl flex items-center gap-2">
          <Link href="/projects" className="hover:text-primary">
            Projetos
          </Link>
        </nav>
      </div>
      {/* header actions */}
      <div className="flex items-center justify-end px-8 py-4">
        <AddProjectDialog />
      </div>

      <div className="px-8 py-4">
        <h1 className="font-bold mb-4 text-xl">Construções recentes</h1>
        <div className="grid grid-cols-3 gap-4">
          {projects?.map((project) => (
            <ProjectCard key={project.uuid} project={project} />
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
          Adicionar projeto
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Adicionar um novo projeto</DialogTitle>
          <DialogDescription>
            Adicione um novo projeto para começar a trabalhar.
          </DialogDescription>
        </DialogHeader>
        <div className="flex items-center space-x-2">
          <ProjectCreateForm />
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
