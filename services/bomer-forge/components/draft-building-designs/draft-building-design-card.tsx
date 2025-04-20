import { Card, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowUpRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { formatDate } from "@/lib/utils";
import { components } from "@/lib/rest-api.types";

export default function DraftBuildingDesignCard({
  draftBuildingDesign,
}: {
  draftBuildingDesign: components["schemas"]["DraftBuildingDesign"];
}) {
  const router = useRouter();

  return (
    <Card
      className="h-[300px] justify-between flex flex-col hover:cursor-pointer"
      onClick={() => router.push(`/buildings/${draftBuildingDesign.uuid}`)}
    >
      <CardHeader>
        <CardTitle className="space-y-2">
          <div className="flex justify-between">
            <div>
              <h4 className="font-bold text-lg">{draftBuildingDesign.name}</h4>
              <p className="text-sm text-muted-foreground">
                {draftBuildingDesign.description}
              </p>
            </div>
            <div>
              <ArrowUpRight className="w-5 h-5" />
            </div>
          </div>
        </CardTitle>
      </CardHeader>
      <CardFooter>
        <div className="flex justify-between border-t-2 w-full py-4">
          <div className="flex justify-between text-xs text-muted-foreground">
            <div>
              <p>
                <span className="font-bold">Data de criação:</span>{" "}
                {formatDate(draftBuildingDesign.created_at)}
              </p>
            </div>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
