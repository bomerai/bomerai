"use client";

import z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function PillarsSection() {
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
      <div className="w-full">
        <h4 className="text-lg font-bold mb-4">Pormenor dos pilares</h4>
        <div className="flex flex-col space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>P1=P2=P3</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center border-b pb-4">
                <div className="flex flex-col border-r flex-1">
                  <h4 className="text-sm font-bold">Arm. Long.</h4>
                  <p>4Ø16</p>
                </div>
                <div className="flex flex-col px-4 border-r flex-1">
                  <h4 className="text-sm font-bold">Arranque</h4>
                  <p>4Ø16</p>
                </div>
                <div className="flex flex-col px-4 flex-1">
                  <h4 className="text-sm font-bold">Arm. Transv.</h4>
                  <p>Ø6</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
        {/* {columnReinforcementsMetadata &&
          columnReinforcementsMetadata.map((metadata) => (
            <ColumnReinforcementCardList
              key={metadata.uuid}
              columnReinforcementMetadata={metadata}
            />
          ))} */}
      </div>
    </div>
  );
}
