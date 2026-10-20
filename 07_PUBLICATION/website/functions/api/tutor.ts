interface Env {
  AI: any;
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { request, env } = context;
  const { message, history } = await request.json() as { message: string, history: any[] };

  if (!message) {
    return new Response(JSON.stringify({ error: "Message required" }), { status: 400 });
  }

  const systemPrompt = `You are the L.E.U. Tutor (Lingua Executabilis Universalis). You understand the 20 primitives (L0-L4). Answer concisely in the language of the user. Provide an L.E.U. expression if relevant.`;

  // Liste des modèles par ordre de préférence (du plus rapide au plus stable)
  const models = [
    "@cf/meta/llama-3.1-8b-instruct-fast",
    "@cf/meta/llama-3.1-8b-instruct",
    "@cf/meta/llama-3-8b-instruct"
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
      
      // Si on arrive ici, c'est que le modèle a répondu
      return new Response(JSON.stringify({ reply: response.response, model_used: model }), {
        headers: { "Content-Type": "application/json" }
      });
      
    } catch (error) {
      lastError = String(error);
      console.warn(`Le modèle ${model} a échoué, essai du suivant...`);
      // On continue vers le modèle suivant
    }
  }

  // Si tous les modèles ont échoué
  return new Response(JSON.stringify({ error: "Tous les modèles IA sont indisponibles.", details: lastError }), { status: 500 });
};
