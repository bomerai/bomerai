import { Card, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowUpRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { Project } from "@/lib/rest-types";
import { formatDate } from "@/lib/utils";
export interface ProjectCardProps {
  project: Project;
}

export default function ProjectCard({ project }: ProjectCardProps) {
  const router = useRouter();
  return (
    <Card
      className="h-[300px] justify-between flex flex-col hover:cursor-pointer"
      onClick={() => router.push(`/projects/${project.uuid}`)}
    >
      <CardHeader>
        <CardTitle className="space-y-2">
          <div className="flex justify-between">
            <div>
              <p className="text-sm font-medium tracking-wide text-anchor">
                {project.description}
              </p>
              <h4 className="font-bold text-lg">{project.name}</h4>
            </div>
            <ArrowUpRight className="w-4 h-4 mr-1" />
          </div>
        </CardTitle>
      </CardHeader>
      <CardFooter>
        <div className="flex justify-between border-t-2 w-full py-4">
          <div className="flex justify-between text-xs text-muted-foreground">
            <div>
              <p>
                <span className="font-bold">Referência:</span>{" "}
                {project.reference}
              </p>
              <p>
                <span className="font-bold">Data de criação:</span>{" "}
                {formatDate(project.created_at)}
              </p>
            </div>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
