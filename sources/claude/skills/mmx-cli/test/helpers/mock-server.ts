export type RouteHandler = (req: Request) => Response | Promise<Response>;

export interface MockServerOptions {
  routes: Record<string, RouteHandler>;
}

export interface MockServer {
  url: string;
  port: number;
  close(): void;
}

export function createMockServer(opts: MockServerOptions): MockServer {
  const server = Bun.serve({
    port: 0, // Random available port
    fetch(req) {
      const url = new URL(req.url);
      const path = url.pathname;

      // Try exact match first
      const handler = opts.routes[path] || opts.routes[`${req.method} ${path}`];
      if (handler) {
        return handler(req);
      }

      // Try prefix match
      for (const [pattern, handler] of Object.entries(opts.routes)) {
        if (path.startsWith(pattern)) {
          return handler(req);
        }
      }

      return new Response(JSON.stringify({ error: 'Not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' },
      });
    },
  });

  return {
    url: `http://localhost:${server.port}`,
    port: server.port!,
    close() {
      server.stop();
    },
  };
}

export function jsonResponse(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

export function sseResponse(events: Array<{ data: string }>): Response {
  const body = events
    .map(e => `data: ${e.data}\n\n`)
    .join('') + 'data: [DONE]\n\n';

  return new Response(body, {
    headers: { 'Content-Type': 'text/event-stream' },
  });
}
