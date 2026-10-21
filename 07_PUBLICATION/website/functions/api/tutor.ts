interface Env { AI: any; }

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;
  const { message } = await request.json() as { message: string };

  // 1. Le Contexte Strict (Grounding) : On injecte les faits de L.E.U.
  const context = `
  You are the L.E.U. Tutor. You ONLY answer based on the following facts.
  FACTS:
  - Creator: Alpha0az1omega (collaboration with DeepSeek).
  - L.E.U. stands for Lingua Executabilis Universalis.
  - It is based on 20 primitives (L0-L4).
  - DOI: 10.5281/zenodo.23476518.
  - Website: alpha0az1omega.com.
  - If the user asks a question NOT covered by these facts, you MUST respond with: "I don't have this information in my knowledge base."
  `;

  try {
    const response = await env.AI.run("@cf/meta/llama-3.1-8b-instruct-fast", {
      messages: [
        { role: "system", content: context },
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
