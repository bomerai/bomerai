import { z } from "zod";

export const ProjectSchema = z.object({
  uuid: z.string(),
  name: z.string(),
  description: z.string(),
  reference: z.string(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Project = z.infer<typeof ProjectSchema>;

// -

export const DraftBuildingDesignSchema = z.object({
  uuid: z.string(),
  status: z.enum(["DRAFT", "IN_PROGRESS", "PUBLISHED"]),
  phase: z.enum(["PHASE_1", "PHASE_2", "PHASE_3"]),
  created_at: z.string(),
  updated_at: z.string(),
});

export type DraftBuildingDesign = z.infer<typeof DraftBuildingDesignSchema>;

// -

export const ColumnReinforcementMetadataSchema = z.object({
  uuid: z.string(),
  component_metadata: z.array(z.any()),
  created_at: z.string(),
  updated_at: z.string(),
});

export type ColumnReinforcementMetadata = z.infer<
  typeof ColumnReinforcementMetadataSchema
>;

// -

export const DesignDrawingComponentMetadataSchema = z.object({
  uuid: z.string(),
  name: z.string(),
  description: z.string(),
  type: z.enum(["FOUNDATION_PLAN", "FRAMING_PLAN"]),
  subtype: z.enum(["FOOTING", "COLUMN", "BEAM", "SLAB"]),
  data: z.any(),
  bom: z.any(),
  is_locked: z.boolean(),
  justification: z.string(),
  task_id: z.string().optional(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type DesignDrawingComponentMetadata = z.infer<
  typeof DesignDrawingComponentMetadataSchema
>;

// -

export const DesignDrawingSchema = z.object({
  uuid: z.string(),
  type: z.enum(["STRUCTURAL_DRAWING"]),
  design_drawing_components_metadata: z.array(
    DesignDrawingComponentMetadataSchema
  ),
  created_at: z.string(),
  updated_at: z.string(),
});

export type DesignDrawing = z.infer<typeof DesignDrawingSchema>;

// -

export const CeleryTaskResultSchema = z.object({
  status: z.enum(["PENDING", "SUCCESS", "FAILURE", "RETRY", "STARTED"]),
  result: z.any(),
});

export type CeleryTaskResult = z.infer<typeof CeleryTaskResultSchema>;
