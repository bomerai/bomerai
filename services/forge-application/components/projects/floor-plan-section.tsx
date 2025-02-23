import Image from "next/image";

export const FloorPlanSection = () => {
  return (
    <div className="flex flex-1 flex-col gap-4 space-y-8 p-8 w-full">
      <div className="flex flex-col space-y-6">
        <h2 className="text-xl font-bold">Planta baixa</h2>
        <div className="w-full bg-white rounded border p-4">
          <Image
            src="/images/floor_plan.png"
            alt="Planta baixa"
            className="mx-auto"
            width={400}
            height={400}
          />
        </div>
      </div>
    </div>
  );
};
