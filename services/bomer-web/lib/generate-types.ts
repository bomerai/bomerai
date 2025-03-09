/**
 * Fetches a Pydantic JSON schema from a Django API endpoint and updates TypeScript types
 * @param schemaUrl The URL of the endpoint that returns the Pydantic model_json_schema()
 * @param outputPath Path to the rest-types.tsx file (defaults to './lib/rest-types.tsx')
 * @param options Optional fetch options (headers, auth tokens, etc.)
 */
export async function updateTypesFromPydanticEndpoint(
  schemaUrl: string,
  outputPath: string = "./lib/rest-types.tsx",
  options: RequestInit = {}
): Promise<void> {
  const fs = require("fs");
  const path = require("path");

  try {
    // Fetch the schema from the Django endpoint
    console.log(`Fetching schema from ${schemaUrl}...`);
    const response = await fetch(schemaUrl, {
      method: "GET",
      headers: {
        Accept: "application/json",
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(
        `Failed to fetch schema: ${response.status} ${response.statusText}`
      );
    }

    const schema = await response.json();

    // Helper function to convert JSON schema types to TypeScript types
    function convertSchemaToTypeScript(
      schema: any,
      definitions: Record<string, any> = {}
    ): string {
      if (!schema) return "any";

      // Handle references to definitions
      if (schema.$ref) {
        const refName = schema.$ref.split("/").pop();
        return refName;
      }

      // Handle different types
      switch (schema.type) {
        case "string":
          if (schema.enum) {
            return schema.enum.map((val: string) => `'${val}'`).join(" | ");
          }
          if (schema.format === "date-time") return "Date";
          return "string";

        case "integer":
        case "number":
          return "number";

        case "boolean":
          return "boolean";

        case "null":
          return "null";

        case "array":
          const itemType = convertSchemaToTypeScript(schema.items, definitions);
          return `${itemType}[]`;

        case "object":
          if (!schema.properties) return "Record<string, any>";

          const properties = Object.entries(schema.properties)
            .map(([propName, propSchema]: [string, any]) => {
              const isRequired = schema.required?.includes(propName);
              const typeStr = convertSchemaToTypeScript(
                propSchema,
                definitions
              );
              return `  ${propName}${isRequired ? "" : "?"}: ${typeStr};`;
            })
            .join("\n");

          return `{\n${properties}\n}`;

        default:
          if (schema.anyOf || schema.oneOf) {
            const types = (schema.anyOf || schema.oneOf).map((s: any) =>
              convertSchemaToTypeScript(s, definitions)
            );
            return types.join(" | ");
          }
          return "any";
      }
    }

    // Process definitions/components into TypeScript interfaces
    let typesOutput =
      "// Auto-generated TypeScript types from Pydantic schema\n\n";

    // Handle newer JSON Schema format (OpenAPI 3.0+)
    const definitions = schema.definitions || schema.components?.schemas || {};

    for (const [name, def] of Object.entries(definitions)) {
      typesOutput += `export interface ${name} ${convertSchemaToTypeScript(
        def,
        definitions
      )}\n\n`;
    }

    // If there's a main schema (not in definitions), add it as well
    if (schema.type === "object" && schema.properties && !schema.$ref) {
      const mainTypeName = "MainSchema"; // You might want to customize this name
      typesOutput += `export interface ${mainTypeName} ${convertSchemaToTypeScript(
        schema,
        definitions
      )}\n\n`;
    }

    // Create directory if it doesn't exist
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // Read existing file to preserve any manual additions
    let existingContent = "";
    try {
      existingContent = fs.readFileSync(outputPath, "utf8");
    } catch (error) {
      // File doesn't exist yet, that's fine
    }

    // Find auto-generated section or append to end
    let updatedContent;
    const autoGenPattern =
      /\/\/ Auto-generated TypeScript types from Pydantic schema\n\n[\s\S]*?(?=\/\/ End auto-generated)/;

    if (existingContent.match(autoGenPattern)) {
      updatedContent = existingContent.replace(
        autoGenPattern,
        `${typesOutput}// End auto-generated\n\n`
      );
    } else {
      // If no auto-generated section exists, add it at the beginning
      updatedContent = `${typesOutput}// End auto-generated\n\n${existingContent}`;
    }

    // Write updated content back to file
    fs.writeFileSync(outputPath, updatedContent, "utf8");

    console.log(`Updated TypeScript types in ${outputPath}`);
  } catch (error) {
    console.error("Error updating types from Pydantic schema:", error);
    throw error;
  }
}

updateTypesFromPydanticEndpoint(
  "http://localhost:8000/api/schema/draft-building-designs/design-drawing-component-metadata/schema/"
);
