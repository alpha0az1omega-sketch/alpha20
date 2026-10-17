interface Env {
  DB: D1Database;
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;
  const body = await request.json() as {
    proposer: string;
    expression: string;
    sha256: string;
    signature?: string;
  };

  if (!body.proposer || !body.expression || !body.sha256) {
    return new Response(JSON.stringify({ error: 'Missing required fields' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const id = crypto.randomUUID();
  await env.DB.prepare(
    'INSERT INTO contracts (id, proposer, expression, sha256, signature) VALUES (?, ?, ?, ?, ?)'
  ).bind(id, body.proposer, body.expression, body.sha256, body.signature || null).run();

  return new Response(JSON.stringify({ id, status: 'created' }), {
    status: 201,
    headers: { 'Content-Type': 'application/json' },
  });
};

export const onRequestGet: PagesFunction<Env> = async (context) => {
  const { env, request } = context;
  const url = new URL(request.url);
  const id = url.searchParams.get('id');

  if (id) {
    const row = await env.DB.prepare('SELECT * FROM contracts WHERE id = ?').bind(id).first();
    if (!row) {
      return new Response(JSON.stringify({ error: 'Not found' }), { status: 404 });
    }
    return new Response(JSON.stringify(row), {
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { results } = await env.DB.prepare('SELECT * FROM contracts ORDER BY created_at DESC LIMIT 50').all();
  return new Response(JSON.stringify(results), {
    headers: { 'Content-Type': 'application/json' },
  });
};
