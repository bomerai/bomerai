"use client";

import { DownloadIcon, PlusIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useQuery } from "@tanstack/react-query";
import { components } from "@/lib/rest-api.types";
import { fetcher } from "@/lib/api-fetcher";
import { useState } from "react";

const AVG_CONCRETE_PRICE_PER_M3 = 75;
const AVG_STEEL_PRICE_PER_KG = 0.75;
export function DraftBuildingDesignBomSection({
  draftBuildingDesignId,
}: {
  draftBuildingDesignId: string;
}) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["draft-building-design-bom"],
    queryFn: () =>
      fetcher<components["schemas"]["DraftBuildingDesignBom"]>(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${draftBuildingDesignId}/bom/`
      ),
  });

  const [showFootingsDetails, setShowFootingsDetails] = useState(false);
  const [showColumnsDetails, setShowColumnsDetails] = useState(false);
  const [showBeamsDetails, setShowBeamsDetails] = useState(false);
  const [showSlabsDetails, setShowSlabsDetails] = useState(false);

  console.log(data, error, isLoading);
  // Calculate subtotals for each section
  const subtotals = {
    footings: data?.footings.reduce(
      (acc, curr) => ({
        steel_weight: acc.steel_weight + curr.steel_weight * curr.quantity,
        concrete_volume:
          acc.concrete_volume + curr.concrete_volume * curr.quantity,
      }),
      { steel_weight: 0, concrete_volume: 0 }
    ),
    columns: data?.columns.reduce(
      (acc, curr) => ({
        steel_weight: acc.steel_weight + curr.steel_weight * curr.quantity,
        concrete_volume:
          acc.concrete_volume + curr.concrete_volume * curr.quantity,
      }),
      { steel_weight: 0, concrete_volume: 0 }
    ),
    beams: data?.beams.reduce(
      (acc, curr) => ({
        steel_weight: acc.steel_weight + curr.steel_weight * curr.quantity,
        concrete_volume:
          acc.concrete_volume + curr.concrete_volume * curr.quantity,
      }),
      { steel_weight: 0, concrete_volume: 0 }
    ),
    slabs: data?.slabs.reduce(
      (acc, curr) => ({
        steel_weight: acc.steel_weight + curr.steel_weight * curr.quantity,
        concrete_volume:
          acc.concrete_volume + curr.concrete_volume * curr.quantity,
      }),
      { steel_weight: 0, concrete_volume: 0 }
    ),
  };

  return (
    <div className="p-8 space-y-8 w-full">
      <div className="flex items-center justify-between border-b pb-8">
        <div>
          <h2 className="font-bold text-xl mb-4">Caderno de encargos</h2>
        </div>
        <div className="flex items-center justify-between gap-2">
          <div className="text-sm p-1.5 px-4 font-medium h-9 rounded border-dashed border-2">
            Preço por m³ de betão:{" "}
            <span className="font-bold">{AVG_CONCRETE_PRICE_PER_M3} €</span>
          </div>
          <div className="text-sm p-1.5 px-4 font-medium h-9 rounded border-dashed border-2">
            Preço por kg de ferro:{" "}
            <span className="font-bold">{AVG_STEEL_PRICE_PER_KG} €</span>
          </div>
          <Button variant="outline">
            <DownloadIcon className="w-4 h-4 mr-2" /> Download report
          </Button>
        </div>
      </div>

      <div className="space-y-6">
        {/* Footings Section */}
        <div>
          <h3 className="font-semibold text-lg mb-4">Sapatas</h3>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Identificador</TableHead>
                <TableHead>Peso de Ferro (kg)</TableHead>
                <TableHead>Volume de Betão (m³)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow className="font-semibold bg-muted/50">
                <TableCell>Subtotal</TableCell>
                <TableCell>
                  {subtotals.footings?.steel_weight.toFixed(1)}{" "}
                  <span className="text-xs">kg</span>
                </TableCell>
                <TableCell>
                  {subtotals.footings?.concrete_volume.toFixed(1)}{" "}
                  <span className="text-xs">m³</span>
                </TableCell>
                <TableCell>
                  <Button
                    onClick={() => setShowFootingsDetails(!showFootingsDetails)}
                    variant="link"
                    size="sm"
                  >
                    <PlusIcon className="w-4 h-4" />
                    Exibir pormenores
                  </Button>
                </TableCell>
              </TableRow>
              {showFootingsDetails &&
                data?.footings.map((footing) => (
                  <TableRow key={footing.id}>
                    <TableCell>{footing.id.slice(0, 4)}</TableCell>
                    <TableCell>
                      {footing.steel_weight} <span className="text-xs">kg</span>
                    </TableCell>
                    <TableCell>
                      {footing.concrete_volume}{" "}
                      <span className="text-xs">m³</span>
                    </TableCell>
                    <TableCell></TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </div>

        {/* Columns Section */}
        <div>
          <h3 className="font-semibold text-lg mb-4">Pilares</h3>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Identificador</TableHead>
                <TableHead>Peso de Ferro (kg)</TableHead>
                <TableHead>Volume de Betão (m³)</TableHead>
                <TableHead></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow className="font-semibold bg-muted/50">
                <TableCell>Subtotal</TableCell>
                <TableCell>
                  {subtotals.columns?.steel_weight.toFixed(1)}{" "}
                  <span className="text-xs">kg</span>
                </TableCell>
                <TableCell>
                  {subtotals.columns?.concrete_volume.toFixed(1)}{" "}
                  <span className="text-xs">m³</span>
                </TableCell>
                <TableCell>
                  <Button
                    onClick={() => setShowColumnsDetails(!showColumnsDetails)}
                    variant="link"
                    size="sm"
                  >
                    <PlusIcon className="w-4 h-4" />
                    Exibir pormenores
                  </Button>
                </TableCell>
              </TableRow>
              {showColumnsDetails &&
                data?.columns.map((column) => (
                  <TableRow key={column.id}>
                    <TableCell>{column.id.slice(0, 4)}</TableCell>
                    <TableCell>{column.steel_weight}</TableCell>
                    <TableCell>{column.concrete_volume}</TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </div>

        {/* Beams Section */}
        <div>
          <h3 className="font-semibold text-lg mb-4">Vigas</h3>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Identificador</TableHead>
                <TableHead>Peso de Ferro (kg)</TableHead>
                <TableHead>Volume de Betão (m³)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow className="font-semibold bg-muted/50">
                <TableCell>Subtotal</TableCell>
                <TableCell>
                  {subtotals.beams?.steel_weight.toFixed(1)}{" "}
                  <span className="text-xs">kg</span>
                </TableCell>
                <TableCell>
                  {subtotals.beams?.concrete_volume.toFixed(1)}{" "}
                  <span className="text-xs">m³</span>
                </TableCell>
                <TableCell>
                  <Button
                    onClick={() => setShowBeamsDetails(!showBeamsDetails)}
                    variant="link"
                    size="sm"
                  >
                    <PlusIcon className="w-4 h-4" />
                    Exibir pormenores
                  </Button>
                </TableCell>
              </TableRow>
              {showBeamsDetails &&
                data?.beams.map((beam) => (
                  <TableRow key={beam.id}>
                    <TableCell>{beam.id.slice(0, 4)}</TableCell>
                    <TableCell>{beam.steel_weight}</TableCell>
                    <TableCell>{beam.concrete_volume}</TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </div>

        {/* Slabs Section */}
        <div>
          <h3 className="font-semibold text-lg mb-4">Lajes</h3>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Identificador</TableHead>
                <TableHead>Peso de Ferro (kg)</TableHead>
                <TableHead>Volume de Betão (m³)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow className="font-semibold bg-muted/50">
                <TableCell>Subtotal</TableCell>
                <TableCell>
                  {subtotals.slabs?.steel_weight.toFixed(1)}{" "}
                  <span className="text-xs">kg</span>
                </TableCell>
                <TableCell>
                  {subtotals.slabs?.concrete_volume.toFixed(1)}{" "}
                  <span className="text-xs">m³</span>
                </TableCell>
                <TableCell>
                  <Button
                    onClick={() => setShowSlabsDetails(!showSlabsDetails)}
                    variant="link"
                    size="sm"
                  >
                    <PlusIcon className="w-4 h-4" />
                    Exibir pormenores
                  </Button>
                </TableCell>
              </TableRow>
              {showSlabsDetails &&
                data?.slabs.map((slab) => (
                  <TableRow key={slab.id}>
                    <TableCell>{slab.id.slice(0, 4)}</TableCell>
                    <TableCell>{slab.steel_weight}</TableCell>
                    <TableCell>{slab.concrete_volume}</TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
