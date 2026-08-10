from agent.decision import Decision
from agent.registry import ToolRegistry
from agent.state import AgentState
from services import LLM

class Planner:
    """Plans the next action for the application agent."""

    def __init__(
        self,
        llm: LLM,
        registry: ToolRegistry
    ) -> None:
        self.llm = llm
        self.registry = registry

    def plan(self, state: AgentState) -> Decision:
        """Determine the next tool to execute."""

        return self.llm.generate(
            prompt=self._build_prompt(state),
            schema=Decision
        )

    def _build_prompt(self, state: AgentState) -> str:
        return f"""
You are an AI application agent.

Your job is to determine the SINGLE next tool that should execute.

You are NOT responsible for solving the user's request yourself.
You are ONLY responsible for selecting the next tool.

============================================================
Overall Goal
============================================================

{state.goal}

============================================================
Latest User Request
============================================================

{state.latest_user_message()}

============================================================
Conversation
============================================================

{state.conversation()}

============================================================
Application State
============================================================

{state.summary()}

============================================================
Available Tools
============================================================

{self.registry.describe()}

IMPORTANT:

You MUST return EXACTLY ONE of the tool names listed above.

Never invent tool names.

If none of the available tools are needed, return:

finish

============================================================
Tool History
============================================================

{state.tool_history_text()}

============================================================
Planning Instructions
============================================================

Use the latest user request to determine what the user wants, but also use the application goal and current application state to determine what workflow steps remain necessary.

If the user asks to tailor their resume, treat that as a request to complete the resume tailoring workflow, including generating the cover letter afterward.

If the user explicitly asks only for interview questions, generate interview questions without unnecessarily repeating resume or cover-letter work.

Use the application state to determine what information already exists.

Use the tool history to determine what work has already been completed.

Only select ONE tool.

Do NOT plan multiple steps ahead.

Do NOT execute prerequisites that are already satisfied.

Do NOT execute tools whose prerequisites are missing.

Do NOT invent new tools.

Do NOT repeatedly execute the same tool unless the latest user request explicitly requires running it again.

A previous execution of a tool counts as satisfying that step unless there is evidence that it failed or the user explicitly requested another revision.

Return finish only when:

- The user's request has been completed.
- All required downstream steps for the requested workflow are complete.
- No additional tool execution is necessary.
- The next tool would only repeat completed work.

============================================================
When to return finish
============================================================

Return finish when:

- No additional tool execution is necessary.
- The latest user request has already been completed.
- Executing another tool would simply repeat work.
- The assistant can now respond using the existing application state.

============================================================
Examples
============================================================

Example 1

User:
Tailor my resume.

History:
(none)

Decision:
extract_job


Example 2

History:
extract_job

Decision:
match_skills


Example 3

History:
extract_job
match_skills

Decision:
analyze_resume


Example 4

History:
extract_job
match_skills
analyze_resume

Decision:
tailor_resume

Example 5

User:
Tailor my resume.

History:
extract_job
match_skills
analyze_resume

Decision:
tailor_resume


Example 6

User:
Tailor my resume.

History:
extract_job
match_skills
analyze_resume
tailor_resume

State:
Resume Tailored: Yes
Cover Letter Generated: No

Decision:
generate_cover_letter


Example 7

User:
Tailor my resume.

History:
extract_job
match_skills
analyze_resume
tailor_resume
generate_cover_letter

State:
Resume Tailored: Yes
Cover Letter Generated: Yes

Decision:
finish

Example 8

User:
Generate a cover letter.

History:
extract_job
match_skills
analyze_resume
tailor_resume

Decision:
generate_cover_letter


Example 9

User:
Make the professional summary stronger.

History:
tailor_resume
Result:
The professional summary was rewritten to better match the target job.

Decision:
finish


Example 10

User:
Can you explain why you changed my summary?

History:
tailor_resume

Decision:
finish


Example 11

User:
Generate another cover letter with a more formal tone.

History:
generate_cover_letter

Decision:
generate_cover_letter

Example 12

User:
Give me some interview questions.

History:
extract_job
match_skills
analyze_resume
tailor_resume
generate_cover_letter

Decision:
generate_interview_questions

Example 13

User:
Give me some interview questions.

History:
generate_interview_questions

Decision:
finish

============================================================
Output
============================================================

Return ONLY a valid Decision object.

The tool field MUST be either:

- one of the available tool names
- finish

Never return explanations outside the Decision object.
"""