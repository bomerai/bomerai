"use client";

import z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Boxes, Loader2, UploadIcon } from "lucide-react";
import { DialogClose, DialogFooter } from "@/components/ui/dialog";
import {
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useParams } from "next/navigation";
import { Dialog } from "@/components/ui/dialog";
import { ColumnDesignDrawingFileUploader } from "./design-drawings/column-design-drawing-file-uploader";
import { useQuery } from "@tanstack/react-query";
import { fetcher } from "@/lib/api-fetcher";
import { components } from "@/lib/rest-api.types";
import { BeamComponentCard } from "./build-components/build-component/beam-component-card";

export function DraftBuildingDesignBeams({
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

  const { data: beams, isLoading } = useQuery({
    queryKey: ["beams"],
    queryFn: () =>
      fetcher<components["schemas"]["DraftBuildingDesignBuildingComponent"][]>(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${buildingDesignUuid}/building-components?type=BEAM`
      ),
  });

  console.log(beams);

  console.log(form.formState.errors);

  return (
    <div className="p-8 space-y-12 w-full">
      <div className="w-full space-y-12">
        <div className="flex items-center justify-between">
          <h4 className="text-lg font-bold">Vigas</h4>
          <BeamDesignDrawingFileUploaderDialog />
        </div>
        <div className="flex flex-col space-y-4">
          {isLoading ? (
            <div className="flex items-center justify-center">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
          ) : (
            beams?.map((beam) => (
              <BeamComponentCard
                key={beam.uuid}
                beam={beam}
                buildingDesignUuid={buildingDesignUuid}
              />
            ))
          )}
          {beams?.length === 0 && (
            <div className="flex items-center justify-center border p-4 text-muted-foreground">
              <Boxes className="w-4 h-4 mr-1" /> Nenhuma viga adicionada ainda.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function BeamDesignDrawingFileUploaderDialog() {
  const { uuid: buildingDesignUuid } = useParams();
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">
          <UploadIcon className="w-4 h-4 mr-1" />
          Adicionar vigas
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Especificações de vigas</DialogTitle>
          <DialogDescription>
            Adicione uma ou mais vigas para começar a trabalhar.
          </DialogDescription>
        </DialogHeader>
        <div className="flex items-center space-x-2">
          <ColumnDesignDrawingFileUploader
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
