/**
 * Ejemplo 5.1 - LangChain Basico: Modelos, Templates y Chains
 * ML2 - Unidad 3, Sesion 2: Acceso Programatico a LLMs
 *
 * LangChain es un framework de orquestacion que proporciona:
 *   - Interfaz unificada para multiples proveedores
 *   - Prompt Templates parametrizados
 *   - Chains (composicion de operaciones con .pipe())
 *
 * Usa OpenRouter como proveedor via ChatOpenAI.
 *
 * Requiere: npm install langchain @langchain/openai dotenv
 */

import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";
import dotenv from "dotenv";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

// ============================================
// CONFIGURACION
// ============================================
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
dotenv.config({ path: join(__dirname, ".env") });

async function main() {
  // ============================================
  // PARTE 1: Chat Model con OpenRouter
  // ============================================
  console.log("=".repeat(60));
  console.log("PARTE 1: Chat Model unificado con LangChain + OpenRouter");
  console.log("=".repeat(60));

  // Crear modelo apuntando a OpenRouter
  const modelo = new ChatOpenAI({
    model: "arcee-ai/trinity-large-preview:free",
    temperature: 0.7,
    apiKey: process.env.OPENROUTER_API_KEY,
    configuration: {
      baseURL: "https://openrouter.ai/api/v1",
    },
  });

  // Llamada simple
  const mensajes = [
    new SystemMessage("Eres un asistente util. Responde en espanol."),
    new HumanMessage("Que es Python en una frase?"),
  ];

  const respuesta = await modelo.invoke(mensajes);
  console.log(`\n  Respuesta: ${respuesta.content}`);

  // ============================================
  // PARTE 2: Prompt Templates
  // ============================================
  console.log("\n" + "=".repeat(60));
  console.log("PARTE 2: Prompt Templates parametrizados");
  console.log("=".repeat(60));

  // Definir un template reutilizable
  const template = ChatPromptTemplate.fromMessages([
    [
      "system",
      "Eres un traductor experto. Traduces de {idioma_origen} a {idioma_destino}.",
    ],
    ["human", "Traduce el siguiente texto:\n\n{texto}"],
  ]);

  // Usar el template con diferentes parametros
  const prompt1 = await template.invoke({
    idioma_origen: "espanol",
    idioma_destino: "ingles",
    texto: "La inteligencia artificial esta transformando el mundo.",
  });

  const prompt2 = await template.invoke({
    idioma_origen: "espanol",
    idioma_destino: "frances",
    texto: "Buenos dias, como estas?",
  });

  const respuesta1 = await modelo.invoke(prompt1);
  const respuesta2 = await modelo.invoke(prompt2);
  console.log(`\n  Espanol -> Ingles: ${respuesta1.content}`);
  console.log(`  Espanol -> Frances: ${respuesta2.content}`);

  // ============================================
  // PARTE 3: Chains con .pipe()
  // ============================================
  console.log("\n" + "=".repeat(60));
  console.log("PARTE 3: Chains (composicion con .pipe())");
  console.log("=".repeat(60));

  // Definir componentes
  const promptExperto = ChatPromptTemplate.fromMessages([
    [
      "system",
      "Eres un experto en {tema}. Responde de forma concisa en 2-3 frases.",
    ],
    ["human", "{pregunta}"],
  ]);

  const parser = new StringOutputParser();

  // Componer la cadena con .pipe()
  const cadena = promptExperto.pipe(modelo).pipe(parser);

  // Ejecutar
  const resultado = await cadena.invoke({
    tema: "Python",
    pregunta: "Cuales son las ventajas de usar type hints?",
  });
  console.log(`\n  Resultado de la cadena: ${resultado}`);

  // ============================================
  // PARTE 4: Cadena secuencial (multi-paso)
  // ============================================
  console.log("\n" + "=".repeat(60));
  console.log("PARTE 4: Cadena secuencial (resumen -> traduccion)");
  console.log("=".repeat(60));

  // Paso 1: Generar un resumen
  const promptResumen = ChatPromptTemplate.fromMessages([
    ["human", "Resume el siguiente texto en 1-2 oraciones:\n\n{texto}"],
  ]);

  // Paso 2: Traducir el resumen
  const promptTraduccion = ChatPromptTemplate.fromMessages([
    ["human", "Traduce al ingles:\n\n{resumen}"],
  ]);

  // Cadenas individuales
  const cadenaResumen = promptResumen.pipe(modelo).pipe(parser);
  const cadenaTraduccion = promptTraduccion.pipe(modelo).pipe(parser);

  // Ejecutar secuencialmente
  const textoLargo =
    "La inteligencia artificial generativa ha experimentado un crecimiento " +
    "exponencial en los ultimos anos. Los modelos de lenguaje grande como " +
    "GPT-4, Claude y Gemini pueden generar texto, codigo y contenido " +
    "creativo con una calidad que hace pocos anos parecia ciencia ficcion. " +
    "Esto ha abierto nuevas posibilidades en educacion, medicina, " +
    "programacion y muchos otros campos.";

  console.log(`\n  Texto original: ${textoLargo.slice(0, 80)}...`);

  const resumen = await cadenaResumen.invoke({ texto: textoLargo });
  console.log(`\n  Resumen: ${resumen}`);

  const traduccion = await cadenaTraduccion.invoke({ resumen });
  console.log(`  Traduccion: ${traduccion}`);

  console.log("\n" + "=".repeat(60));
  console.log("LangChain simplifica:");
  console.log(
    "   - Cambiar de proveedor: solo cambia ChatOpenAI por ChatAnthropic"
  );
  console.log("   - Reutilizar prompts: templates con variables {variable}");
  console.log("   - Componer operaciones: prompt.pipe(modelo).pipe(parser)");
  console.log("=".repeat(60));
}

main().catch(console.error);
