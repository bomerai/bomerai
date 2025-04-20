"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FileUpload } from "@/components/ui/file-upload";
import {
  Cuboid,
  Plus,
  HammerIcon,
  Minus,
  ArrowRight,
  Check,
  Copy,
  TrashIcon,
  Box,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import Cookies from "js-cookie";
import { useNotificationContext } from "@/hooks/notification-context";
import { Badge } from "@/components/ui/badge";
import Asterisc from "@/components/ui/icons/asterisc";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import z from "zod";
import { cn } from "@/lib/utils";
import {
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";
import { Select } from "@/components/ui/select";
import { PencilIcon } from "@heroicons/react/24/outline";
import { Controller } from "react-hook-form";
import { Switch } from "@/components/ui/switch";
import { useCsrfToken } from "@/hooks/useCsrfToken";

interface FormData {
  files: File[];
  type: string;
}

export default function BuildingMeasure() {
  const { uuid: buildingDesignUuid } = useParams();
  const searchParams = useSearchParams();
  const [step, setStep] = useState<number>(1);
  const { addNotification } = useNotificationContext();
  const csrfToken = useCsrfToken();

  const handleNextStep = () => {
    const newStep = step + 1;
    setStep(newStep);

    // Store step in cookie with UUID-specific key
    Cookies.set(`measureStep_${buildingDesignUuid}`, newStep.toString(), {
      expires: 7,
    }); // Cookie expires in 7 days

    // Update URL parameters
    const params = new URLSearchParams(window.location.search);
    params.set("step", newStep.toString());
    window.history.replaceState({}, "", `?${params.toString()}`);
  };

  useEffect(() => {
    // Check for step in cookie first using UUID-specific key
    const cookieStep = parseInt(
      Cookies.get(`measureStep_${buildingDesignUuid}`) || "0"
    );

    if (cookieStep) {
      setStep(cookieStep);

      // Ensure URL reflects the cookie value
      const params = new URLSearchParams(window.location.search);
      params.set("step", cookieStep.toString());
      window.history.replaceState({}, "", `?${params.toString()}`);
    } else {
      // If no cookie, check URL params
      if (searchParams.get("step")) {
        const urlStep = parseInt(searchParams.get("step") as string);
        setStep(urlStep);
        // Store in cookie for future use
        Cookies.set(`measureStep_${buildingDesignUuid}`, urlStep.toString(), {
          expires: 7,
        });
      } else {
        // Default to step 1 and store in both cookie and URL
        setStep(1);
        Cookies.set(`measureStep_${buildingDesignUuid}`, "1", { expires: 7 });

        const params = new URLSearchParams(window.location.search);
        params.set("step", "1");
        window.history.replaceState({}, "", `?${params.toString()}`);
      }
    }
  }, [searchParams, buildingDesignUuid]);

  const handleSubmit = async ({ files, type }: FormData) => {
    if (!csrfToken) {
      addNotification({
        message: "Error: CSRF token not available. Please try again.",
        type: "error",
      });
      return;
    }

    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });
    formData.append("draft_building_design_uuid", buildingDesignUuid as string);
    formData.append("type", type);

    try {
      const resp = await fetch(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/${buildingDesignUuid}/upload-files/`,
        {
          method: "POST",
          body: formData,
          credentials: "include",
          mode: "cors",
          headers: {
            "X-CSRFToken": csrfToken,
          },
        }
      );

      if (resp.ok) {
        console.log("Pormenor dos pilares carregado com sucesso");
        handleNextStep();
      } else {
        const errorData = await resp.json().catch(() => null);
        console.error("Erro ao carregar pormenor dos pilares", errorData);
        addNotification({
          message: errorData?.detail || "Erro ao carregar pormenor dos pilares",
          type: "error",
        });
      }
    } catch (error) {
      console.error(error);
      addNotification({
        message: "Erro ao iniciar leitura",
        type: "error",
      });
    }
  };

  return (
    <div className="p-8 space-y-12 bg-white h-screen">
      <div>
        <h1 className="text-2xl font-bold">Leitura de pormenores</h1>
        <p className="text-sm text-muted-foreground">
          Medir uma construção é um processo que consiste em medir as
          características da construção e calcular a quantidade de cada
          componente.
        </p>
      </div>
      <div className="space-y-4 flex flex-col">
        <Step1 onSubmit={handleSubmit} currentStep={step} />
        <Step2 onSubmit={handleSubmit} currentStep={step} />
        <Step3 handleNextStep={handleNextStep} currentStep={step} />
        <Step4 currentStep={step} />
      </div>
    </div>
  );
}

// Footings
const Step1 = ({
  onSubmit,
  currentStep,
}: {
  onSubmit: (formData: FormData) => Promise<void>;
  currentStep: number;
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleContinue = async () => {
    setIsLoading(true);
    await onSubmit({ files, type: "FOOTING" });
    setIsLoading(false);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-bold flex items-center gap-2">
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center gap-2">
              <Box className="w-4 h-4" /> Sapatas{" "}
              <Badge
                variant="outline"
                className="text-xs text-anchor items-center flex gap-2"
              >
                <Asterisc className="w-4 h-4" />
                AI leitura
              </Badge>
            </div>
            <div
              className={cn(
                "h-5 w-5 bg-green-500 rounded-full flex items-center justify-center border-2 border-green-200/30",
                currentStep > 1 && "opacity-100"
              )}
            >
              <Check className="w-3 h-3 text-white" />
            </div>
          </div>
        </CardTitle>
        <CardDescription
          className={cn("hidden", currentStep === 1 && "opacity-100")}
        >
          Faça o upload das imagens dos pormenores das sapatas
        </CardDescription>
      </CardHeader>
      <CardContent className={cn("hidden", currentStep === 1 && "opacity-100")}>
        <div className="space-y-6">
          <FileUpload
            onFilesSelected={(files) => setFiles(files)}
            maxFiles={100}
          />
          <Button onClick={handleContinue} disabled={isLoading}>
            {isLoading ? "Aguarde..." : "Continuar"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

// Columns
const Step2 = ({
  onSubmit,
  currentStep,
}: {
  onSubmit: (formData: FormData) => Promise<void>;
  currentStep: number;
}) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleContinue = async () => {
    setIsLoading(true);
    await onSubmit({ files, type: "COLUMN" });
    setIsLoading(false);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-bold flex items-center gap-2">
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center gap-2">
              <Box className="w-4 h-4" /> Pilares{" "}
              <Badge
                variant="outline"
                className="text-xs text-anchor items-center flex gap-2"
              >
                <Asterisc className="w-4 h-4" />
                AI leitura
              </Badge>
            </div>
            <div
              className={cn(
                "h-5 w-5 bg-green-500 rounded-full flex items-center justify-center border-2 border-green-200/30",
                currentStep > 2 && "opacity-100"
              )}
            >
              <Check className="w-3 h-3 text-white" />
            </div>
          </div>
        </CardTitle>
        <CardDescription
          className={cn("hidden", currentStep === 2 && "opacity-100")}
        >
          Faça o upload das imagens dos pormenores dos pilares
        </CardDescription>
      </CardHeader>
      <CardContent className={cn("hidden", currentStep === 2 && "opacity-100")}>
        <div className="space-y-6">
          <FileUpload
            onFilesSelected={(files) => setFiles(files)}
            maxFiles={100}
          />
          <Button onClick={handleContinue} disabled={isLoading}>
            {isLoading ? "Aguarde..." : "Continuar"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

// Beams
const Step3 = ({
  handleNextStep,
  currentStep,
}: {
  handleNextStep: () => void;
  currentStep: number;
}) => {
  type Beam = {
    length: number;
    width: number;
    height: number;
    longitudinal_reinforcement_diameter: number;
    longitudinal_reinforcement_quantity: number;
    stirrups_diameter: number;
    stirrups_quantity: number;
    stirrups_spacing: number;
  };

  const { uuid: buildingDesignUuid } = useParams();
  const [showAllBeams, setShowAllBeams] = useState(false);
  const [isAddBeamDialogOpen, setIsAddBeamDialogOpen] = useState(false);

  const [beams, setBeams] = useState<Beam[]>([]);

  const beamFormSchema = z.object({
    length: z.number().min(1, "Length must be at least 1"),
    width: z.number().min(1, "Width must be at least 1"),
    height: z.number().min(1, "Height must be at least 1"),
    longitudinal_reinforcement_diameter: z
      .number()
      .min(1, "Diameter must be at least 1"),
    longitudinal_reinforcement_quantity: z
      .number()
      .min(1, "Quantity must be at least 1"),
    stirrups_diameter: z.number().min(1, "Diameter must be at least 1"),
    stirrups_quantity: z.number().min(1, "Quantity must be at least 1"),
    stirrups_spacing: z.number().min(1, "Spacing must be at least 1"),
  });

  type BeamFormValues = z.infer<typeof beamFormSchema>;

  const form = useForm<BeamFormValues>({
    resolver: zodResolver(beamFormSchema),
    defaultValues: {
      length: 24,
      width: 24,
      height: 24,
      longitudinal_reinforcement_diameter: 12,
      longitudinal_reinforcement_quantity: 4,
      stirrups_diameter: 8,
      stirrups_quantity: 2,
      stirrups_spacing: 20,
    },
  });

  // Watch for changes in height and spacing to calculate stirrups quantity
  const length = form.watch("length");
  const spacing = form.watch("stirrups_spacing");

  // Calculate stirrups quantity whenever height or spacing changes
  useEffect(() => {
    if (length && spacing && spacing > 0) {
      // Calculate the number of stirrups based on length and spacing
      // We add 1 to account for the stirrup at the top
      const calculatedQuantity = Math.floor(length / spacing);
      form.setValue("stirrups_quantity", calculatedQuantity);
    }
  }, [length, spacing, form]);

  const handleAddBeam = (data: BeamFormValues) => {
    // Ensure stirrups_quantity is calculated before adding

    setBeams([...beams, data]);
    setIsAddBeamDialogOpen(false);
    form.reset();
  };

  const handleDuplicateBeam = (index: number) => {
    const beam = beams[index];
    setBeams([...beams, beam]);
  };

  const handleSubmit = async () => {
    const payload = beams.map((beam) => ({
      type: "BEAM",
      component_data: beam,
      draft_building_design_id: buildingDesignUuid as string,
    }));

    const resp = await fetch(
      `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/building-components/bulk-create/`,
      {
        method: "POST",
        body: JSON.stringify(payload),
        credentials: "include",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken") || "",
        },
      }
    );

    if (resp.ok) {
      handleNextStep();
    } else {
      console.error("Erro ao enviar vigas");
    }
  };

  const lazyBeams = showAllBeams ? beams : beams.slice(0, 4);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-bold flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Vigas{" "}
            <Badge
              variant="outline"
              className="text-xs text-amber-500 items-center flex gap-2"
            >
              <HammerIcon className="w-4 h-4" />
              Manual
            </Badge>
          </div>
          <div
            className={cn(
              "h-5 w-5 bg-green-500 rounded-full items-center justify-center border-2 border-green-200/30 hidden",
              currentStep > 3 && "flex"
            )}
          >
            <Check className="w-3 h-3 text-white" />
          </div>
          <div
            className={cn("hidden", currentStep === 3 && "block opacity-100")}
          >
            <Dialog
              open={isAddBeamDialogOpen}
              onOpenChange={setIsAddBeamDialogOpen}
            >
              <DialogTrigger asChild>
                <Button variant="outline" size="icon">
                  <Plus className="w-4 h-4" />
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md lg:max-w-lg xl:max-w-xl">
                <DialogHeader>
                  <DialogTitle>Adicionar nova viga</DialogTitle>
                  <DialogDescription>
                    Preencha os detalhes da nova viga
                  </DialogDescription>
                </DialogHeader>
                <form
                  onSubmit={form.handleSubmit(handleAddBeam)}
                  className="space-y-4"
                >
                  <div className="flex flex-col gap-2">
                    <div className="grid grid-cols-2 gap-10">
                      <label htmlFor="length" className="text-sm font-medium">
                        Comprimento (cm)
                      </label>
                      <Input
                        id="length"
                        type="number"
                        min="0"
                        step="0.01"
                        {...form.register("length", {
                          valueAsNumber: true,
                        })}
                      />
                      {form.formState.errors.length && (
                        <p className="text-xs text-red-500">
                          {form.formState.errors.length.message}
                        </p>
                      )}
                    </div>
                    <div className="grid grid-cols-2 gap-10">
                      <label htmlFor="width" className="text-sm font-medium">
                        Largura (cm)
                      </label>
                      <Input
                        id="width"
                        type="number"
                        min="0"
                        step="0.01"
                        {...form.register("width", {
                          valueAsNumber: true,
                        })}
                      />
                      {form.formState.errors.width && (
                        <p className="text-xs text-red-500">
                          {form.formState.errors.width.message}
                        </p>
                      )}
                    </div>
                    <div className="grid grid-cols-2 gap-10">
                      <label htmlFor="height" className="text-sm font-medium">
                        Altura (cm)
                      </label>
                      <Input
                        id="height"
                        type="number"
                        {...form.register("height", {
                          valueAsNumber: true,
                        })}
                      />
                      {form.formState.errors.height && (
                        <p className="text-xs text-red-500">
                          {form.formState.errors.height.message}
                        </p>
                      )}
                    </div>
                    <div className="grid grid-cols-2 gap-10">
                      <label
                        htmlFor="longitudinal_reinforcement_diameter"
                        className="text-sm font-medium"
                      >
                        Diâmetro da armadura longitudinal (mm)
                      </label>
                      <Input
                        id="longitudinal_reinforcement_diameter"
                        type="number"
                        {...form.register(
                          "longitudinal_reinforcement_diameter",
                          {
                            valueAsNumber: true,
                          }
                        )}
                      />
                      {form.formState.errors
                        .longitudinal_reinforcement_diameter && (
                        <p className="text-xs text-red-500">
                          {
                            form.formState.errors
                              .longitudinal_reinforcement_diameter.message
                          }
                        </p>
                      )}
                    </div>
                    <div className="grid grid-cols-2 gap-10">
                      <label
                        htmlFor="longitudinal_reinforcement_quantity"
                        className="text-sm font-medium"
                      >
                        Quantidade de armadura longitudinal
                      </label>
                      <Input
                        id="longitudinal_reinforcement_quantity"
                        type="number"
                        {...form.register(
                          "longitudinal_reinforcement_quantity",
                          {
                            valueAsNumber: true,
                          }
                        )}
                      />
                      {form.formState.errors
                        .longitudinal_reinforcement_quantity && (
                        <p className="text-xs text-red-500">
                          {
                            form.formState.errors
                              .longitudinal_reinforcement_quantity.message
                          }
                        </p>
                      )}
                    </div>
                    <div className="grid grid-cols-2 gap-10">
                      <label
                        htmlFor="stirrups_diameter"
                        className="text-sm font-medium"
                      >
                        Diâmetro dos estribos (mm)
                      </label>
                      <Input
                        id="stirrups_diameter"
                        type="number"
                        {...form.register("stirrups_diameter", {
                          valueAsNumber: true,
                        })}
                      />
                      {form.formState.errors.stirrups_diameter && (
                        <p className="text-xs text-red-500">
                          {form.formState.errors.stirrups_diameter.message}
                        </p>
                      )}
                    </div>
                    <div className="grid grid-cols-2 gap-10">
                      <label
                        htmlFor="stirrups_spacing"
                        className="text-sm font-medium"
                      >
                        Espaçamento dos estribos (cm)
                      </label>
                      <Input
                        id="stirrups_spacing"
                        type="number"
                        {...form.register("stirrups_spacing")}
                      />
                      {form.formState.errors.stirrups_spacing && (
                        <p className="text-xs text-red-500">
                          {form.formState.errors.stirrups_spacing.message}
                        </p>
                      )}
                    </div>
                    <div className="grid grid-cols-2 gap-10">
                      <label
                        htmlFor="stirrups_quantity"
                        className="text-sm font-medium"
                      >
                        Quantidade de estribos
                      </label>
                      <Input
                        id="stirrups_quantity"
                        type="number"
                        {...form.register("stirrups_quantity")}
                      />
                      {form.formState.errors.stirrups_quantity && (
                        <p className="text-xs text-red-500">
                          {form.formState.errors.stirrups_quantity.message}
                        </p>
                      )}
                    </div>
                  </div>
                  <DialogFooter className="sm:justify-end">
                    <DialogClose asChild>
                      <Button variant="outline">Cancelar</Button>
                    </DialogClose>
                    <Button type="submit">Adicionar</Button>
                  </DialogFooter>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        </CardTitle>
        <CardDescription
          className={cn("hidden", currentStep === 3 && "opacity-100")}
        >
          Faça o upload das imagens dos pormenores das vigas
        </CardDescription>
      </CardHeader>
      <CardContent
        className={cn(
          "hidden",
          currentStep === 3 && "space-y-4 block opacity-100"
        )}
      >
        <div className="flex justify-between items-center">
          <div className="text-sm font-medium">Total: {beams.length}</div>
          <Button
            onClick={() => setShowAllBeams(!showAllBeams)}
            variant="link"
            size="sm"
          >
            {showAllBeams ? (
              <Minus className="w-4 h-4" />
            ) : (
              <Plus className="w-4 h-4" />
            )}
            {showAllBeams ? "Ocultar" : "Exibir todas"}
          </Button>
        </div>
        <div className="grid grid-cols-4 gap-4">
          {lazyBeams.map((beam, index) => (
            <div
              key={index}
              className="p-4 border rounded-md space-y-4 border-t-4 border-t-orange-300"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Cuboid className="w-4 h-4" />
                  <span className="text-md font-bold">Viga {index + 1}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Button
                    onClick={() => handleDuplicateBeam(index)}
                    variant="outline"
                    size="icon"
                  >
                    <Copy className="w-4 h-4" />
                  </Button>
                  <Button variant="outline" size="icon">
                    <PencilIcon className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className="text-sm border-r pr-4">
                  {beam.length}x{beam.width}x{beam.height}cm
                </div>
                <div>
                  <div className="text-sm">
                    {beam.longitudinal_reinforcement_quantity}Ø
                    {beam.longitudinal_reinforcement_diameter}
                    {"//"}
                    {beam.stirrups_spacing}
                  </div>
                </div>
              </div>
            </div>
          ))}
          <div
            onClick={() => setIsAddBeamDialogOpen(true)}
            className="border-2 border-dashed p-4 rounded flex items-center gap-2 cursor-pointer hover:border-anchor h-fit bg-muted text-muted-foreground hover:text-anchor"
          >
            <Plus className="w-4 h-4" />
            <span className="text-sm font-medium">Adicionar viga</span>
          </div>
        </div>
        <Button onClick={handleSubmit}>
          Continuar <ArrowRight className="w-4 h-4" />
        </Button>
      </CardContent>
    </Card>
  );
};

// Slabs
const Step4 = ({
  currentStep,
}: {
  currentStep: number;
}): React.ReactElement => {
  type Slab = {
    length?: number;
    width?: number;
    area?: number;
    thickness: number;
    type: "Aligeirada" | "Maciça" | "Fungiforme" | "Nervurada";
  };

  const [showAllSlabs, setShowAllSlabs] = useState(false);
  const [isAddSlabDialogOpen, setIsAddSlabDialogOpen] = useState(false);
  const [useArea, setUseArea] = useState(false);
  const buildingDesignUuid = useParams().uuid as string;
  const csrfToken = useCsrfToken();
  const router = useRouter();

  const [slabs, setSlabs] = useState<Slab[]>([]);

  const slabFormSchema = z
    .object({
      length: z.preprocess(
        (val) => (val === "" || val === null ? undefined : Number(val)),
        z.number().min(1, "Comprimento mínimo de 1m").optional()
      ),
      width: z.preprocess(
        (val) => (val === "" || val === null ? undefined : Number(val)),
        z.number().min(1, "Largura mínima de 1m").optional()
      ),
      thickness: z.preprocess(
        (val) => (val === "" || val === null ? undefined : Number(val)),
        z.number().min(1, "Espessura mínima de 1m")
      ),
      type: z.enum(["Aligeirada", "Maciça", "Fungiforme", "Nervurada"]),
      area: z.preprocess(
        (val) => (val === "" || val === null ? undefined : Number(val)),
        z.number().min(1, "Área mínima de 1m²")
      ),
    })
    .refine(
      (data) => {
        // If area is provided directly, it's valid
        if (data.area) return true;
        // If length and width are provided, we can calculate area
        if (data.length && data.width) return true;
        // Otherwise, it's invalid
        return false;
      },
      {
        message:
          "Forneça a área diretamente ou as dimensões (comprimento e largura)",
      }
    );

  const form = useForm<z.infer<typeof slabFormSchema>>({
    resolver: zodResolver(slabFormSchema),
    defaultValues: {
      type: "Maciça",
    },
    mode: "onChange",
  });

  // Watch length and width to auto-calculate area
  const length = form.watch("length");
  const width = form.watch("width");

  useEffect(() => {
    // Only calculate if both length and width are provided and area wasn't manually entered
    if (length && width && !useArea) {
      form.setValue("area", length * width);
    }
  }, [length, width, useArea, form]);

  const handleAddSlab = (values: z.infer<typeof slabFormSchema>) => {
    if (!values.thickness) return;

    const slab: Slab = {
      length: values.length,
      width: values.width,
      thickness: values.thickness,
      type: values.type,
      area: values.area,
    };

    setSlabs([...slabs, slab]);
    setIsAddSlabDialogOpen(false);
    form.reset({
      type: "Maciça",
    });
  };

  const lazySlabs = showAllSlabs ? slabs : slabs.slice(0, 4);

  const handleSubmit = async () => {
    const payload = slabs.map((slab) => ({
      type: "SLAB",
      draft_building_design_id: buildingDesignUuid,
      component_data: {
        length: slab.length,
        width: slab.width,
        area: slab.area,
        thickness: slab.thickness,
        type: slab.type,
      },
    }));
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/building-components/bulk-create/`,
      {
        method: "POST",
        body: JSON.stringify(payload),
        credentials: "include",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken || "",
        },
      }
    );

    if (res.ok) {
      router.push(`/buildings/${buildingDesignUuid}/loading`);
    } else {
      console.error("Erro ao carregar pormenor dos pilares");
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-bold flex items-cente justify-between gap-2">
          <div className="flex items-center gap-2">
            <Cuboid className="w-4 h-4" /> Lajes{" "}
            <Badge
              variant="outline"
              className="text-xs text-amber-500 items-center flex gap-2"
            >
              <HammerIcon className="w-4 h-4" />
              Manual
            </Badge>
          </div>
          <div
            className={cn("hidden", currentStep === 4 && "block opacity-100")}
          >
            <Dialog
              open={isAddSlabDialogOpen}
              onOpenChange={setIsAddSlabDialogOpen}
            >
              <DialogTrigger asChild>
                <Button variant="outline" size="icon">
                  <Plus className="w-4 h-4" />
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md lg:max-w-lg xl:max-w-xl">
                <DialogHeader>
                  <DialogTitle>Adicionar nova laje</DialogTitle>
                  <DialogDescription>
                    Preencha os detalhes da nova laje
                  </DialogDescription>
                </DialogHeader>
                <form
                  onSubmit={form.handleSubmit(handleAddSlab)}
                  className="space-y-4"
                >
                  <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-2 mb-10">
                      <Switch
                        id="useArea"
                        checked={useArea}
                        onCheckedChange={setUseArea}
                      />
                      <label htmlFor="useArea" className="text-sm font-medium">
                        Usar área
                      </label>
                    </div>
                    <div
                      className={cn("grid grid-cols-2", useArea && "hidden")}
                    >
                      <label htmlFor="length" className="text-sm font-medium">
                        Comprimento (m)
                      </label>
                      <div>
                        <Input
                          id="length"
                          type="number"
                          min="0"
                          step="0.01"
                          {...form.register("length")}
                        />
                        {form.formState.errors.length && (
                          <p className="text-xs text-red-500">
                            {form.formState.errors.length.message}
                          </p>
                        )}
                      </div>
                    </div>
                    <div
                      className={cn("grid grid-cols-2", useArea && "hidden")}
                    >
                      <label htmlFor="width" className="text-sm font-medium">
                        Largura (m)
                      </label>
                      <div>
                        <Input
                          id="width"
                          type="number"
                          min="0"
                          step="0.01"
                          {...form.register("width")}
                        />
                        {form.formState.errors.width && (
                          <p className="text-xs text-red-500">
                            {form.formState.errors.width.message}
                          </p>
                        )}
                      </div>
                    </div>
                    <div
                      className={cn("grid grid-cols-2", !useArea && "hidden")}
                    >
                      <label htmlFor="area" className="text-sm font-medium">
                        Área (m²)
                      </label>
                      <div>
                        <Input
                          id="area"
                          type="number"
                          min="0"
                          step="0.01"
                          {...form.register("area")}
                        />
                        {form.formState.errors.area && (
                          <p className="text-xs text-red-500">
                            {form.formState.errors.area.message}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="grid grid-cols-2">
                      <label
                        htmlFor="thickness"
                        className="text-sm font-medium"
                      >
                        Espessura (cm)
                      </label>
                      <div>
                        <Input
                          id="thickness"
                          type="number"
                          min="0"
                          step="0.01"
                          {...form.register("thickness")}
                        />
                        {form.formState.errors.thickness && (
                          <p className="text-xs text-red-500">
                            {form.formState.errors.thickness.message}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="grid grid-cols-2">
                      <label htmlFor="type" className="text-sm font-medium">
                        Tipo
                      </label>
                      <Controller
                        name="type"
                        control={form.control}
                        defaultValue="Maciça"
                        render={({ field }) => (
                          <Select
                            onValueChange={field.onChange}
                            value={field.value}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Selecione o tipo" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="Aligeirada">
                                Aligeirada
                              </SelectItem>
                              <SelectItem value="Maciça">Maciça</SelectItem>
                              <SelectItem value="Fungiforme">
                                Fungiforme
                              </SelectItem>
                              <SelectItem value="Nervurada">
                                Nervurada
                              </SelectItem>
                            </SelectContent>
                          </Select>
                        )}
                      />
                    </div>
                  </div>
                  <DialogFooter className="sm:justify-end">
                    <DialogClose asChild>
                      <Button variant="outline">Cancelar</Button>
                    </DialogClose>
                    <Button type="submit">Adicionar</Button>
                  </DialogFooter>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent
        className={cn("hidden", currentStep === 4 && "space-y-4 block")}
      >
        <div className="flex justify-between items-center">
          <div className="text-sm font-medium">Total: {slabs.length}</div>
          <Button
            onClick={() => setShowAllSlabs(!showAllSlabs)}
            variant="link"
            size="sm"
          >
            {showAllSlabs ? (
              <Minus className="w-4 h-4" />
            ) : (
              <Plus className="w-4 h-4" />
            )}
            {showAllSlabs ? "Ocultar" : "Exibir todas"}
          </Button>
        </div>
        <div className="grid grid-cols-4 gap-4">
          {lazySlabs.map((slab, index) => (
            <div
              key={index}
              className="p-4 border rounded-md space-y-2 border-t-4 border-t-orange-300"
            >
              <div className="flex justify-between items-center">
                <div className="flex items-center gap-2">
                  <Cuboid className="w-4 h-4" />
                  <span className="text-md font-bold">Laje {index + 1}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Button variant="outline" size="icon">
                    <Copy className="w-4 h-4" />
                  </Button>
                  <Button variant="outline" size="icon">
                    <PencilIcon className="w-4 h-4" />
                  </Button>
                  <Button variant="outline" size="icon">
                    <TrashIcon className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div>
                  <div className="text-xs text-muted-foreground">Área</div>
                  <div className="text-sm font-medium">{slab.area} m²</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Espessura</div>
                  <div className="text-sm font-medium">{slab.thickness} cm</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground">Tipo</div>
                  <div className="text-sm font-medium">{slab.type}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <Button onClick={handleSubmit}>
          Continuar <ArrowRight className="w-4 h-4" />
        </Button>
      </CardContent>
    </Card>
  );
};
