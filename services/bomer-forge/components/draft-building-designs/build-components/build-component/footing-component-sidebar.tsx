import { XIcon } from "lucide-react";
import { Button } from "../../../ui/button";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { DesignDrawingComponentMetadata } from "@/lib/rest-types";
import { truncate } from "lodash";
import { Skeleton } from "@/components/ui/skeleton";

const getDesignDrawingComponentMetadata = async (
  designDrawingComponentMetadataUuid: string
): Promise<DesignDrawingComponentMetadata> => {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/design-drawing-component-metadata/${designDrawingComponentMetadataUuid}/`,
    {
      credentials: "include",
      mode: "cors",
    }
  );
  return response.json();
};

export default function FootingMetadataSidebar({
  drawingComponentFootingUuid,
}: {
  drawingComponentFootingUuid: string;
}) {
  const router = useRouter();

  const { data: designDrawingComponentMetadata, isLoading } = useQuery({
    queryKey: [
      "design-drawing-component-metadata",
      drawingComponentFootingUuid,
    ],
    queryFn: () =>
      getDesignDrawingComponentMetadata(drawingComponentFootingUuid),
  });

  return (
    <div className="bg-white border-l w-[500px] fixed right-0 bottom-0 top-[112px]">
      {isLoading && (
        <div className="flex justify-center items-center h-full">
          <div className="space-y-4">
            <Skeleton className="h-4 w-[250px]" />
            <Skeleton className="h-4 w-[200px]" />
          </div>
        </div>
      )}
      {!isLoading && designDrawingComponentMetadata && (
        <div className="min-w-[400px] px-4 py-8 space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="text-xl font-bold tracking-wide">
              {truncate(designDrawingComponentMetadata.uuid, { length: 20 })}
            </h4>
            <Button
              variant="ghost"
              onClick={() => {
                const searchParams = new URLSearchParams(
                  window.location.search
                );
                searchParams.delete("designDrawingComponentMetadataUuid");
                router.push(
                  `${window.location.pathname}?${searchParams.toString()}`
                );
              }}
            >
              <XIcon className="" />
            </Button>
          </div>
          <div className="overflow-y-scroll h-[calc(100vh-112px)] p-2 custom-scrollbar">
            <div className="space-y-8">
              {/* basic info */}
              <div className="flex flex-col gap-2 border-b pb-8">
                <div className="text-sm">
                  <div className="font-bold">Justificativa:</div>
                  <p className="">
                    {designDrawingComponentMetadata?.justification}
                  </p>
                </div>
              </div>

              {/* bom */}
              <div className="flex flex-col gap-2 border-b pb-8">
                <div className="">
                  <div className="font-bold mb-4">Cálculo de Quantidade</div>
                  <div className="flex flex-col gap-2">
                    <div className="text-sm">
                      <div className="font-bold">Raciocínio:</div>
                      <p className="">
                        {designDrawingComponentMetadata?.bom?.rationale}
                      </p>
                    </div>

                    <div className="text-sm">
                      <div className="font-bold">Volume de concreto:</div>
                      <p className="">
                        {
                          designDrawingComponentMetadata?.bom
                            ?.concrete_volume_in_cubic_meters
                        }{" "}
                        m³
                      </p>
                    </div>
                    <div className="text-sm">
                      <div className="font-bold">Peso do aço:</div>
                      <p className="">
                        {Number(
                          designDrawingComponentMetadata?.bom
                            ?.steel_weight_in_kilograms
                        ).toFixed(2)}{" "}
                        kg
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
