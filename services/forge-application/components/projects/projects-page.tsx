"use client";

import CostEstimatorForm from "@/components/project-cost-estimator/cost-estimator-form";
import { Button } from "@/components/ui/button";
import { EyeIcon, PlusIcon } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
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
import { Card, CardFooter, CardHeader, CardTitle } from "../ui/card";

export default function ProjectsPage() {
  const router = useRouter();
  return (
    <div>
      <div className="flex items-center justify-between px-8 py-4 border-b">
        <nav className="font-medium text-lg flex items-center gap-2">
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
        <h1 className="font-bold mb-4">Recentes</h1>
        <div className="grid grid-cols-3 gap-4">
          <Card className="h-[300px] justify-between flex flex-col hover:cursor-pointer">
            <CardHeader>
              <CardTitle className="space-y-2">
                <p className="text-sm font-medium tracking-wide text-anchor">
                  100m², 3 dormitórios, 2 banheiros, 1 sala de estar, 1 cozinha
                </p>
                <h4 className="font-bold text-lg">
                  Casa T3, Gondufe, Ponte de Lima
                </h4>
              </CardTitle>
            </CardHeader>
            <CardFooter>
              <div className="flex justify-between border-t-2 w-full py-4">
                <div className="flex justify-between text-xs text-muted-foreground">
                  <div>
                    <p>
                      <span className="font-bold">Cliente:</span> João da Silva
                    </p>
                    <p>
                      <span className="font-bold">Data de criação:</span>{" "}
                      10/01/2024
                    </p>
                  </div>
                </div>
                <Button
                  variant="outline"
                  onClick={() => router.push(`/projects/1`)}
                >
                  <EyeIcon className="w-4 h-4 mr-1" />
                  Ver projeto
                </Button>
              </div>
            </CardFooter>
          </Card>
          <Card className="h-[300px] justify-between flex flex-col hover:cursor-pointer">
            <CardHeader>
              <CardTitle className="space-y-2">
                <p className="text-sm font-medium tracking-wide text-anchor">
                  100m², 3 dormitórios, 2 banheiros, 1 sala de estar, 1 cozinha
                </p>
                <h4 className="font-bold text-lg">
                  Casa T3, Gondufe, Ponte de Lima
                </h4>
              </CardTitle>
            </CardHeader>
            <CardFooter>
              <div className="flex justify-between border-t-2 w-full py-4">
                <div className="flex justify-between text-xs text-muted-foreground">
                  <div>
                    <p>
                      <span className="font-bold">Cliente:</span> João da Silva
                    </p>
                    <p>
                      <span className="font-bold">Data de criação:</span>{" "}
                      10/01/2024
                    </p>
                  </div>
                </div>
                <Button
                  variant="outline"
                  onClick={() => router.push(`/projects/2`)}
                >
                  <EyeIcon className="w-4 h-4 mr-1" />
                  Ver projeto
                </Button>
              </div>
            </CardFooter>
          </Card>
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
          <CostEstimatorForm />
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
