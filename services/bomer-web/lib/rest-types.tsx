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

export const DraftBuildingDesignSchema = z.object({
  uuid: z.string(),
  status: z.enum(["DRAFT", "IN_PROGRESS", "PUBLISHED"]),
  phase: z.enum(["PHASE_1", "PHASE_2", "PHASE_3"]),
  created_at: z.string(),
  updated_at: z.string(),
});

export type DraftBuildingDesign = z.infer<typeof DraftBuildingDesignSchema>;

export const ColumnReinforcementMetadataSchema = z.object({
  uuid: z.string(),
  component_metadata: z.array(z.any()),
  created_at: z.string(),
  updated_at: z.string(),
});

export type ColumnReinforcementMetadata = z.infer<
  typeof ColumnReinforcementMetadataSchema
>;
