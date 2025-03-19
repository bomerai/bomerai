"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Textarea } from "@/components/ui/textarea";
import { Project } from "@/lib/rest-types";
import Cookies from "js-cookie";
import { useEffect } from "react";

export default function ProjectCreateForm() {
  const formSchema = z.object({
    name: z.string().min(1),
    description: z.string().min(1),
    reference: z.string().min(1),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      description: "",
      reference: "",
    },
  });

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
      console.log(data);
      Cookies.set("csrftoken", data.csrfToken);
    };

    fetchCSRFToken();
  }, []);

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/projects/`,
      {
        method: "POST",
        credentials: "include",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken") || "",
        },
        body: JSON.stringify(data),
      }
    );

    if (response.ok) {
      const project = (await response.json()) as Project;
      window.location.href = `/projects/${project.uuid}`;
    }
  };

  return (
    <div className="w-full max-w-md">
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <Label htmlFor="project_name">Nome do projeto</Label>
          <Input type="text" id="project_name" {...form.register("name")} />
        </div>

        <div>
          <Label htmlFor="project_description">Descrição do projeto</Label>
          <Textarea
            id="project_description"
            {...form.register("description")}
          />
        </div>

        <div>
          <Label htmlFor="project_reference">Referência do projeto</Label>
          <Input
            type="text"
            id="project_reference"
            {...form.register("reference")}
          />
        </div>

        <div className="flex justify-end">
          <Button type="submit">Criar projeto</Button>
        </div>
      </form>
    </div>
  );
}
