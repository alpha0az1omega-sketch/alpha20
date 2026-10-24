interface Env {
  AI: any;
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;
  const { message } = await request.json() as { message: string };

  if (!message) {
    return new Response(JSON.stringify({ error: "Message required" }), { status: 400 });
  }

  // LE GROUNDING : On donne les faits exacts et on interdit d'inventer
  const facts = `
  You are the L.E.U. Tutor. 
  FACTS:
  - L.E.U. means Lingua Executabilis Universalis.
  - Creator: Alpha0az1omega (in collaboration with DeepSeek).
  - 20 Primitives: 
    L0: EXIST, SAME, ONE, ALL, NOT, IF, TRUE
    L1: CAUSE, PART, BIG
    L2: DO, HAPPEN, MOVE
    L3: KNOW, SEE, THINK, SAY
    L4: LIVE, DIE, GOOD
  - Website: https://alpha0az1omega.com
  - DOI: 10.5281/zenodo.23476518
  RULES:
  - If the user asks about L.E.U., answer ONLY based on these facts.
  - If the user asks a question outside of this scope, say: "I am the L.E.U. Tutor. I can only answer questions about the Lingua Executabilis Universalis."
  - NEVER invent new primitives, creators, or definitions.
  `;

  try {
    const response = await env.AI.run("@cf/meta/llama-3.1-8b-instruct-fast", {
      messages: [
        { role: "system", content: facts },
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
