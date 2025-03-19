import { XIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { DesignDrawingComponentMetadata } from "@/lib/rest-types";
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

export default function ColumnMetadataSidebar({
  drawingComponentColumnUuid,
}: {
  drawingComponentColumnUuid: string;
}) {
  const router = useRouter();

  const { data: designDrawingComponentMetadata, isLoading } = useQuery({
    queryKey: ["design-drawing-component-metadata", drawingComponentColumnUuid],
    queryFn: () =>
      getDesignDrawingComponentMetadata(drawingComponentColumnUuid),
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
              {designDrawingComponentMetadata.data.code}
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
                  <div className="font-bold mb-4">Especificações</div>
                  <div className="flex flex-col gap-2">
                    <h4 className="text-xs uppercase">Dimensões</h4>
                    <div className="text-xs">
                      <div className="font-bold">Largura:</div>
                      <p className="">
                        {designDrawingComponentMetadata?.data.width}
                      </p>
                    </div>
                    <div className="text-xs">
                      <div className="font-bold">Comprimento:</div>
                      <p className="">
                        {designDrawingComponentMetadata?.data.length}
                      </p>
                    </div>
                    <div className="text-xs">
                      <div className="font-bold">Altura:</div>
                      <p className="">
                        {designDrawingComponentMetadata?.data.height}
                      </p>
                    </div>
                    <div className="text-xs">
                      <div className="font-bold">Tipo:</div>
                      <p className="">
                        {designDrawingComponentMetadata?.data.type}
                      </p>
                    </div>
                    <div className="text-xs">
                      <div className="font-bold">
                        Diâmetro da armadura longitudinal:
                      </div>
                      <p className="">
                        {
                          designDrawingComponentMetadata?.data
                            .longitudinal_rebar_diameter
                        }
                      </p>
                    </div>
                    <div className="text-xs">
                      <div className="font-bold">Número de estribos:</div>
                      <p className="">
                        {
                          designDrawingComponentMetadata?.data
                            .longitudinal_rebar_stirrups_number
                        }
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
