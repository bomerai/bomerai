"use client";

import z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Loader2, PlusIcon } from "lucide-react";
import {
  DialogClose,
  DialogFooter,
  DialogHeader,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from "@/components/ui/dialog";
import { useParams } from "next/navigation";
import { components } from "@/lib/rest-api.types";
import { fetcher } from "@/lib/api-fetcher";
import { useQuery } from "@tanstack/react-query";
import { FootingComponentCard } from "./build-components/build-component/footing-component-card";
import { FootingDesignDrawingFileUploader } from "./design-drawings/footing-design-drawing-file-uploader";

export function DraftBuildingDesignFootings({
  buildingDesignUuid,
}: {
  buildingDesignUuid: string;
}) {
  const formSchema = z.object({
    files: z.array(z.instanceof(File)),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      files: [],
    },
  });

  const { data: footings, isLoading } = useQuery({
    queryKey: ["footings"],
    queryFn: () =>
      fetcher<components["schemas"]["DraftBuildingDesignBuildingComponent"][]>(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${buildingDesignUuid}/building-components?type=FOOTING`
      ),
  });

  console.log(footings);

  console.log(form.formState.errors);

  return (
    <div className="p-8 space-y-12 w-full">
      <div className="w-full space-y-12">
        <div className="flex items-center justify-between">
          <h4 className="text-lg font-bold">Fundações</h4>
          <FootingDesignDrawingFileUploaderDialog />
        </div>
        <div className="flex flex-col"></div>
        <div className="flex flex-col space-y-4">
          {isLoading ? (
            <div className="flex items-center justify-center">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
          ) : (
            footings?.map((component) => (
              <FootingComponentCard
                key={component.uuid}
                footing={component}
                buildingDesignUuid={buildingDesignUuid as string}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export function FootingDesignDrawingFileUploaderDialog() {
  const { uuid: buildingDesignUuid } = useParams();
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">
          <PlusIcon className="w-4 h-4 mr-1" />
          Adicionar fundações
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Especificações de fundações</DialogTitle>
          <DialogDescription>
            Adicione uma ou mais fundações para começar a trabalhar.
          </DialogDescription>
        </DialogHeader>
        <div className="flex items-center space-x-2">
          <FootingDesignDrawingFileUploader
            buildingDesignUuid={buildingDesignUuid as string}
          />
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
