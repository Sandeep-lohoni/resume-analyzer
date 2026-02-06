import json
import logging
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)

load_dotenv()

prompt = ChatPromptTemplate.from_template("""
You are an AI career assistant.

Use ONLY the provided data.
DO NOT add new skills or assumptions.

Resume-Job Match Score: {match_score}%

Matched Skills:
{matched_skills}

Missing Skills with Priority:
{missing_skills}

Task:
1. Explain the match score clearly.
2. Highlight strengths.
3. Identify critical gaps.
4. Suggest a realistic learning roadmap.

Return a valid JSON object with these keys:
- overall_feedback: string
- strengths: list of strings
- skill_gaps: list of strings
- learning_roadmap: list of strings
""")

def _coerce_list(value):
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        lines = [line.strip("- ").strip() for line in value.splitlines()]
        return [line for line in lines if line]
    return []

def _parse_llm_text(text: str):
    candidates = [text.strip()]
    if "```" in text:
        # Strip markdown fences if present.
        stripped = text.replace("```json", "```").replace("```", "").strip()
        candidates.append(stripped)
    # Try to extract a JSON object if the response has extra text.
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(text[start:end + 1])

    data = None
    for candidate in candidates:
        try:
            data = json.loads(candidate)
            break
        except json.JSONDecodeError:
            continue
    if data is None:
        return None
    if not isinstance(data, dict):
        return None
    return {
        "overall_feedback": str(data.get("overall_feedback", "")).strip(),
        "strengths": _coerce_list(data.get("strengths", [])),
        "skill_gaps": _coerce_list(data.get("skill_gaps", [])),
        "learning_roadmap": _coerce_list(data.get("learning_roadmap", []))
    }

def generate_llm_feedback(analysis_data: dict):
    env_model = os.getenv("GEMINI_MODEL")
    model_candidates = [env_model] if env_model else []
    # 1.5 models were shut down; prefer latest/2.x aliases.
    model_candidates += [
        "gemini-flash-latest",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.5-pro"
    ]

    last_exc = None
    for model_name in model_candidates:
        try:
            llm = ChatGoogleGenerativeAI(
                temperature=0.2,
                model=model_name
            )

            chain = prompt | llm

            response = chain.invoke({
                "match_score": analysis_data["match_score"],
                "matched_skills": analysis_data["matched_skills"],
                "missing_skills": analysis_data["missing_skills"]
            })

            content = response.content if hasattr(response, "content") else str(response)
            parsed = _parse_llm_text(content)
            if parsed:
                return parsed
            return {
                "overall_feedback": content.strip(),
                "strengths": [],
                "skill_gaps": [],
                "learning_roadmap": []
            }
        except Exception as exc:
            last_exc = exc
            continue

    logger.exception("LLM feedback generation failed.")
    return {
        "overall_feedback": (
            "LLM feedback unavailable. Check your Gemini API key and model "
            f"configuration. Details: {last_exc}"
        ),
        "strengths": [],
        "skill_gaps": [],
        "learning_roadmap": []
    }
