"use client";

import z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { UploadIcon } from "lucide-react";

export function ColumnsSection() {
  const formSchema = z.object({
    files: z.array(z.instanceof(File)),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      files: [],
    },
  });

  console.log(form.formState.errors);

  return (
    <div className="p-8 space-y-12 w-full">
      <div className="w-full space-y-12">
        <div className="flex items-center justify-between">
          <h4 className="text-lg font-bold">Pormenor dos pilares</h4>
          <Button variant="outline">
            <UploadIcon className="w-4 h-4 text-anchor" />
            Carregar pormenor de pilares
          </Button>
        </div>
        <div className="flex flex-col space-y-4"></div>
      </div>
    </div>
  );
}
