"use client";
import { DownloadIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

// Mock data for demonstration
const mockData = {
  footings: [
    { id: "F1", steelWeight: 120.5, concreteVolume: 2.3 },
    { id: "F2", steelWeight: 150.2, concreteVolume: 2.8 },
    { id: "F3", steelWeight: 120.5, concreteVolume: 2.3 },
    { id: "F4", steelWeight: 150.2, concreteVolume: 2.8 },
    { id: "F5", steelWeight: 120.5, concreteVolume: 2.3 },
    { id: "F6", steelWeight: 150.2, concreteVolume: 2.8 },
  ],
  columns: [
    { id: "C1", steelWeight: 85.3, concreteVolume: 1.5 },
    { id: "C2", steelWeight: 92.7, concreteVolume: 1.6 },
    { id: "C3", steelWeight: 85.3, concreteVolume: 1.5 },
    { id: "C4", steelWeight: 92.7, concreteVolume: 1.6 },
    { id: "C5", steelWeight: 85.3, concreteVolume: 1.5 },
    { id: "C6", steelWeight: 92.7, concreteVolume: 1.6 },
  ],
  beams: [
    { id: "B1", steelWeight: 95.8, concreteVolume: 1.8 },
    { id: "B2", steelWeight: 88.4, concreteVolume: 1.7 },
    { id: "B3", steelWeight: 95.8, concreteVolume: 1.8 },
    { id: "B4", steelWeight: 88.4, concreteVolume: 1.7 },
    { id: "B5", steelWeight: 95.8, concreteVolume: 1.8 },
    { id: "B6", steelWeight: 88.4, concreteVolume: 1.7 },
  ],
  slabs: [
    { id: "S1", steelWeight: 250.6, concreteVolume: 4.2 },
    { id: "S2", steelWeight: 275.3, concreteVolume: 4.5 },
    { id: "S3", steelWeight: 250.6, concreteVolume: 4.2 },
    { id: "S4", steelWeight: 275.3, concreteVolume: 4.5 },
  ],
};

export function DraftBuildingDesignBomSection() {
  // Calculate subtotals for each section
  const subtotals = {
    footings: mockData.footings.reduce(
      (acc, curr) => ({
        steelWeight: acc.steelWeight + curr.steelWeight,
        concreteVolume: acc.concreteVolume + curr.concreteVolume,
      }),
      { steelWeight: 0, concreteVolume: 0 }
    ),
    columns: mockData.columns.reduce(
      (acc, curr) => ({
        steelWeight: acc.steelWeight + curr.steelWeight,
        concreteVolume: acc.concreteVolume + curr.concreteVolume,
      }),
      { steelWeight: 0, concreteVolume: 0 }
    ),
    beams: mockData.beams.reduce(
      (acc, curr) => ({
        steelWeight: acc.steelWeight + curr.steelWeight,
        concreteVolume: acc.concreteVolume + curr.concreteVolume,
      }),
      { steelWeight: 0, concreteVolume: 0 }
    ),
    slabs: mockData.slabs.reduce(
      (acc, curr) => ({
        steelWeight: acc.steelWeight + curr.steelWeight,
        concreteVolume: acc.concreteVolume + curr.concreteVolume,
      }),
      { steelWeight: 0, concreteVolume: 0 }
    ),
  };

  return (
    <div className="p-8 space-y-8 w-full">
      <div className="flex items-center justify-between">
        <h2 className="font-bold text-xl">Caderno de encargos</h2>
        <div className="flex items-center justify-between">
          <Button variant="tertiary">
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
              {mockData.footings.map((footing) => (
                <TableRow key={footing.id}>
                  <TableCell>{footing.id}</TableCell>
                  <TableCell>{footing.steelWeight}</TableCell>
                  <TableCell>{footing.concreteVolume}</TableCell>
                </TableRow>
              ))}
              <TableRow className="font-semibold bg-muted/50">
                <TableCell>Subtotal</TableCell>
                <TableCell>
                  {subtotals.footings.steelWeight.toFixed(1)}
                </TableCell>
                <TableCell>
                  {subtotals.footings.concreteVolume.toFixed(1)}
                </TableCell>
              </TableRow>
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
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockData.columns.map((column) => (
                <TableRow key={column.id}>
                  <TableCell>{column.id}</TableCell>
                  <TableCell>{column.steelWeight}</TableCell>
                  <TableCell>{column.concreteVolume}</TableCell>
                </TableRow>
              ))}
              <TableRow className="font-semibold bg-muted/50">
                <TableCell>Subtotal</TableCell>
                <TableCell>
                  {subtotals.columns.steelWeight.toFixed(1)}
                </TableCell>
                <TableCell>
                  {subtotals.columns.concreteVolume.toFixed(1)}
                </TableCell>
              </TableRow>
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
              {mockData.beams.map((beam) => (
                <TableRow key={beam.id}>
                  <TableCell>{beam.id}</TableCell>
                  <TableCell>{beam.steelWeight}</TableCell>
                  <TableCell>{beam.concreteVolume}</TableCell>
                </TableRow>
              ))}
              <TableRow className="font-semibold bg-muted/50">
                <TableCell>Subtotal</TableCell>
                <TableCell>{subtotals.beams.steelWeight.toFixed(1)}</TableCell>
                <TableCell>
                  {subtotals.beams.concreteVolume.toFixed(1)}
                </TableCell>
              </TableRow>
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
              {mockData.slabs.map((slab) => (
                <TableRow key={slab.id}>
                  <TableCell>{slab.id}</TableCell>
                  <TableCell>{slab.steelWeight}</TableCell>
                  <TableCell>{slab.concreteVolume}</TableCell>
                </TableRow>
              ))}
              <TableRow className="font-semibold bg-muted/50">
                <TableCell>Subtotal</TableCell>
                <TableCell>{subtotals.slabs.steelWeight.toFixed(1)}</TableCell>
                <TableCell>
                  {subtotals.slabs.concreteVolume.toFixed(1)}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
