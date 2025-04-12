import { PlusIcon } from "lucide-react";
import { BeamComponentCard } from "./build-component/beam-component-card";
import { Button } from "@/components/ui/button";
import { SparklesIcon } from "@heroicons/react/24/outline";

const Section = ({ children }: { children: React.ReactNode }) => {
  return <div className="flex flex-col gap-4">{children}</div>;
};

const SectionHeader = ({ children }: { children: React.ReactNode }) => {
  return <div className="flex items-center justify-between">{children}</div>;
};

const SectionContent = ({ children }: { children: React.ReactNode }) => {
  return <div className="border rounded p-4 space-y-4">{children}</div>;
};

export function BuildComponentMeasurer() {
  return (
    <div className="flex flex-col space-y-12">
      <Section>
        <SectionHeader>
          <h4 className="text-lg font-bold">Vigas</h4>
          <Button variant="outline">
            <SparklesIcon className="w-4 h-4 text-anchor" />
            <span className="text-anchor font-medium">Medir com AI</span>
          </Button>
        </SectionHeader>
        <SectionContent>
          <BeamComponentCard />
          <div className="w-full border-dashed border-2 rounded flex items-center gap-2 p-4 hover:bg-anchor/10 cursor-pointer hover:border-anchor">
            <PlusIcon className="w-4 h-4 text-anchor" />
            <span className="text-anchor font-medium">Adicionar medição</span>
          </div>
        </SectionContent>
      </Section>
    </div>
  );
}
