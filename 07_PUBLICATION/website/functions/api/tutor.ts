interface Env {
  AI: any;
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;
  const { message, history } = await request.json() as { message: string, history: any[] };

  if (!message) {
    return new Response(JSON.stringify({ error: "Message required" }), { status: 400 });
  }

  // Prompt strict pour éviter les hallucinations
  const systemPrompt = `You are the L.E.U. Tutor (Lingua Executabilis Universalis). 
You are an AI assistant created by the collaboration between Alpha0az1omega and DeepSeek. 
Do NOT invent facts about L.E.U. The creator is Alpha0az1omega, not anyone else.
L.E.U. is a language based on 20 primitives (L0-L4). Answer concisely based strictly on this context.`;

  const models = [
    "@cf/meta/llama-3.1-8b-instruct-fast",
    "@cf/meta/llama-3.1-8b-instruct"
  ];

  let lastError = "";

  for (const model of models) {
    try {
      const response = await env.AI.run(model, {
        messages: [
          { role: "system", content: systemPrompt },
          ...(history || []),
          { role: "user", content: message }
        ]
      });
      
      return new Response(JSON.stringify({ reply: response.response, model_used: model }), {
        headers: { "Content-Type": "application/json" }
      });
      
    } catch (error) {
      lastError = String(error);
      console.warn(`Le modèle ${model} a échoué, essai du suivant...`);
    }
  }

  return new Response(JSON.stringify({ error: "Tous les modèles IA sont indisponibles.", details: lastError }), { status: 500 });
};
