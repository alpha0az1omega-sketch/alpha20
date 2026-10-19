interface Env {
  AI: any;
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;
  const { message, history } = await request.json() as { message: string, history: any[] };

  if (!message) {
    return new Response(JSON.stringify({ error: "Message required" }), { status: 400 });
  }

  const systemPrompt = `You are the L.E.U. Tutor (Lingua Executabilis Universalis). 
You understand the 20 primitives (L0-L4): EXIST, SAME, ONE, ALL, NOT, IF, TRUE, CAUSE, PART, BIG, DO, HAPPEN, MOVE, KNOW, SEE, THINK, SAY, LIVE, DIE, GOOD.
Answer concisely in the language of the user. Provide an L.E.U. expression if relevant.`;

  try {
    const response = await env.AI.run("@cf/meta/llama-3-8b-instruct", {
      messages: [
        { role: "system", content: systemPrompt },
        ...(history || []),
        { role: "user", content: message }
      ]
    });
    return new Response(JSON.stringify({ reply: response.response }), {
      headers: { "Content-Type": "application/json" }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: "AI service unavailable" }), { status: 500 });
  }
};
