import { XIcon } from "lucide-react";
import { Button } from "../ui/button";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils";

const mockData = [
  {
    uuid: "1",
    image: "/images/tijolo.jpg",
    name: "Bloco cerâmico - 30x20x10 cm",
    price: 0.65,
    quantity: 5822,
    total: 3784.3,
    store: "Leroy Merlin - Braga",
  },
  {
    uuid: "2",
    image: "/images/tijolo.jpg",
    name: "Bloco cerâmico - 30x20x10 cm",
    price: 0.76,
    quantity: 5822,
    total: 4424.32,
    store: "Ikea - Braga Sul",
  },
  {
    uuid: "3",
    image: "/images/tijolo.jpg",
    name: "Bloco cerâmico - 30x20x10 cm",
    price: 0.9,
    quantity: 5822,
    total: 5239.8,
    store: "Bricolage - Ponte de Lima",
  },
];

export const MaterialCostExplorer = () => {
  const router = useRouter();
  return (
    <div className="bg-white border-l w-[500px] fixed right-0 bottom-0 top-[112px]">
      <div className="min-w-[400px] px-4 py-8 space-y-4">
        <div className="flex justify-between items-center">
          <h4 className="text-xl font-bold tracking-wide">Preço médio</h4>
          <Button
            variant="ghost"
            onClick={() => {
              const searchParams = new URLSearchParams(window.location.search);
              searchParams.delete("selectedMaterialEvaluationUuid");
              router.push(
                `${window.location.pathname}?${searchParams.toString()}`
              );
            }}
          >
            <XIcon className="w-20 h-20" />
          </Button>
        </div>
        <div className="flex flex-col border-b pb-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-sm">Produto: </span>
            <span className="text-sm font-medium">Tijolo 30x20x10 cm</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="font-bold text-sm">Quantidade: </span>
            <span className="text-sm font-medium">5822 unidades</span>
          </div>
        </div>
        <div className="overflow-y-scroll h-[calc(100vh-112px)] p-2 custom-scrollbar">
          <h4 className="font-bold text-xs mb-10">24 Resultados encontrados</h4>
          <div className="space-y-2">
            {mockData.map((item) => (
              <div
                key={item.uuid}
                className={cn("border-b rounded flex items-center p-2 gap-4")}
              >
                <div className="">
                  <Image
                    src="/images/tijolo.jpg"
                    alt="Tijolo"
                    width={100}
                    height={100}
                  />
                </div>
                <div className="flex flex-col flex-1">
                  <div className="flex justify-between gap-2">
                    <div className="flex flex-col">
                      <span className="text-anchor text-xs">{item.store}</span>
                      <h4 className="font-medium">{item.name}</h4>
                      <div className="flex items-center gap-1 text-sm">
                        <span className="">€{item.price}</span>
                        <span className="">unidade</span>
                      </div>
                      <div className="flex items-center gap-2 mt-2">
                        <span className="text-xl font-bold">
                          total: €{item.total}
                        </span>
                      </div>
                    </div>
                    <div className="flex flex-col items-end"></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
