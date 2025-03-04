import { BoxIcon, ChevronDown, ToyBrick, XIcon } from "lucide-react";
import { Button } from "../../ui/button";
import { useRouter } from "next/navigation";

export default function BuildComponentSidebar() {
  const router = useRouter();

  return (
    <div className="bg-white border-l w-[500px] fixed right-0 bottom-0 top-[112px]">
      <div className="min-w-[400px] px-4 py-8 space-y-4">
        <div className="flex justify-between items-center">
          <h4 className="text-xl font-bold tracking-wide">Parede externa</h4>
          <Button
            variant="ghost"
            onClick={() => {
              const searchParams = new URLSearchParams(window.location.search);
              searchParams.delete("buildingComponentUuid");
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
              <div>
                <div className="">
                  <span className="font-bold">Área:</span> 100m²
                </div>
              </div>
              <div>
                <div className="font-bold">Justificativa:</div>
                <p className="text-sm">
                  Uma casa com isolamento de gesso e paredes de tijolos. Um chão
                  com pvc para melhor isolamento térmico.
                </p>
              </div>
            </div>

            {/* materials used */}
            <div className="flex-flex-col gap-4">
              <div className="font-bold flex justify-between pb-6">
                <div>Calculo de quantidade</div>
                <div>
                  <Button variant="ghost">
                    <ChevronDown className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              <div className="max-h-[300px] overflow-y-scroll custom-scrollbar">
                <ul className="space-y-4">
                  <li className="flex items-start gap-2 border-b pb-2 pr-8">
                    <div className="p-1">
                      <ToyBrick className="w-4 h-4" />
                    </div>
                    <div className="flex flex-col flex-1">
                      <div className="flex items-center justify-between">
                        <div>Bloco cerâmico</div>
                        <div className="">
                          x 5791{" "}
                          <span className="uppercase text-xs text-muted-foreground">
                            un
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="text-xs text-muted-foreground">
                          30x20x10cm
                        </div>
                        <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
                        <div className="text-xs text-muted-foreground">
                          Barro
                        </div>
                      </div>
                    </div>
                  </li>
                  <li className="flex items-start gap-2 border-b pb-2 pr-8">
                    <div className="p-1">
                      <BoxIcon className="w-4 h-4" />
                    </div>
                    <div className="flex flex-col flex-1">
                      <div className="flex items-center justify-between">
                        <div>Areia</div>
                        <div className="">
                          x 10{" "}
                          <span className="uppercase text-xs text-muted-foreground">
                            m3
                          </span>
                        </div>
                      </div>
                    </div>
                  </li>
                  <li className="flex items-start gap-2 border-b pb-2 pr-8">
                    <div className="p-1">
                      <BoxIcon className="w-4 h-4" />
                    </div>
                    <div className="flex flex-col flex-1">
                      <div className="flex items-center justify-between">
                        <div>Cimento</div>
                        <div className="">
                          x 80{" "}
                          <span className="uppercase text-xs text-muted-foreground">
                            kg
                          </span>
                        </div>
                      </div>
                    </div>
                  </li>
                  <li className="flex items-start gap-2 border-b pb-2 pr-8">
                    <div className="p-1">
                      <BoxIcon className="w-4 h-4" />
                    </div>
                    <div className="flex flex-col flex-1">
                      <div className="flex items-center justify-between">
                        <div>Agua</div>
                        <div className="">
                          x 240{" "}
                          <span className="uppercase text-xs text-muted-foreground">
                            L
                          </span>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
