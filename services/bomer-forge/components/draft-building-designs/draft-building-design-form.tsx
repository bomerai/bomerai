"use client";

import { Button } from "@/components/ui/button";
import z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { DraftBuildingDesign } from "@/lib/rest-types";
import Cookies from "js-cookie";
import { useEffect } from "react";
import { useParams } from "next/navigation";
import { Input } from "../ui/input";
import { Label } from "@radix-ui/react-label";
import { Textarea } from "../ui/textarea";

export default function DraftBuildingDesignForm() {
  const { uuid: projectUuid } = useParams();

  const formSchema = z.object({
    name: z.string().min(1),
    description: z.string().min(1),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      description: "",
    },
  });

  console.log(form.formState.errors);

  useEffect(() => {
    const fetchCSRFToken = async () => {
      console.log("fetching CSRF token...");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/auth/csrf/`,
        {
          method: "GET",
          credentials: "include",
          mode: "cors",
        }
      );
      const data = await response.json();
      Cookies.set("csrftoken", data.csrfToken);
    };

    fetchCSRFToken();
  }, []);

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    console.log(data);
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/draft-building-designs/`,
      {
        method: "POST",
        credentials: "include",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken") || "",
        },
        body: JSON.stringify({
          ...data,
          project_uuid: projectUuid,
        }),
      }
    );

    if (response.ok) {
      const draftBuildingDesign =
        (await response.json()) as DraftBuildingDesign;
      window.location.href = `/buildings/${draftBuildingDesign.uuid}/measure`;
    }
  };

  return (
    <div className="w-full max-w-md">
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <Label htmlFor="name">Nome da construção</Label>
          <Input type="text" id="name" {...form.register("name")} />
        </div>

        <div>
          <Label htmlFor="description">Descrição da construção</Label>
          <Textarea id="description" {...form.register("description")} />
        </div>

        <div className="flex justify-end">
          <Button type="submit">Criar construção</Button>
        </div>
      </form>
    </div>
  );
}
