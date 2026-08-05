# Voriq AI Agentic Architecture

Voriq AI employs a LangGraph multi-agent supervisor-router architecture.

## Core Agents

1. **Supervisor Router Agent**: Classifies incoming queries by intent, language, complexity, and modality.
2. **General Assistant Agent**: General reasoning, conversation, and task handling.
3. **Indian Language Agent**: Native script & code-mixed (Hinglish, Manglish, Tanglish, Tenglish) handling, transliteration, and cultural nuances.
4. **Translation Agent**: High-accuracy translation preserving brand names, medical/legal terminology, and formal/conversational tone.
5. **Research Agent**: Multi-source web search, freshness verification, credibility scoring, and structured report synthesis.
6. **Document Intelligence Agent**: Parsing, OCR, RAG retrieval over PDFs, DOCX, XLSX, and CSVs with exact line/page citations.
7. **Coding Agent**: Software engineering, code generation, refactoring, and execution trace analysis.
8. **Data Analysis Agent**: Spreadsheet computation, statistical summaries, and chart generation.
9. **Image Director Agent**: Prompt enhancement, negative prompting, Indian contextual styling, and character consistency control.
10. **Video Director Agent**: Storyboard scriptwriting, shot list generation, keyframe creation, and scene-by-scene motion directing.
11. **Scriptwriting Agent**: Dialogue, screenplay formatting, and narrative flow in Indian regional languages.
12. **Voice Production Agent**: Speech-to-text, text-to-speech, emotion/pitch selection, and subtitle alignment.
13. **Business Analyst Agent**: Market research, financial forecasting, pitch deck drafting, and strategy analysis.
14. **Marketing Agent**: Campaign creation, ad copy, social media graphics planning, and localized brand tone.
15. **Finance Agent**: Financial reporting, invoice analysis, compliance, and budget planning.
16. **Healthcare Agent**: Clinical context parsing, medical report summaries, and safety-verified healthcare information.
17. **Education Agent**: Curriculum design, automated tutoring, quiz generation, and simplified concept explanations.
18. **Customer Support Agent**: Automated support workflows, ticket resolution, and multi-lingual customer interaction.

## Agent Capabilities & Contracts
Each agent enforces:
- `name`: Unique identifier
- `purpose`: Functional mandate
- `allowed_tools`: Whitelist of accessible execution tools
- `input_schema` / `output_schema`: Structured Pydantic contracts
- `max_steps`: Step-limit cap to prevent loops
- `approval_requirements`: Human-in-the-loop triggers for destructive/financial actions
