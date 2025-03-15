/**
 * Fetches data from the API
 * @param url The URL to fetch from
 * @param options The options for the fetch request
 * @param method The method to use for the fetch request
 * @param body The body to send with the fetch request
 */
export const fetcher = <T>(
  url: string,
  options: RequestInit = {},
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  body: Record<string, unknown> | null = null
) =>
  fetch(url, {
    method,
    credentials: "include",
    mode: "cors",
    ...options,
    body: body ? JSON.stringify(body) : undefined,
  }).then((res) => res.json() as Promise<T>);
