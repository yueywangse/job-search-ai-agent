import logging

from agent.planner import Planner
from agent.registry import ToolRegistry
from agent.state import AgentState
from agent.decision import Decision
from agent.tools import (
    AnalyzeResumeTool,
    ExtractJobTool,
    GenerateCoverLetterTool,
    MatchSkillsTool,
    TailorResumeTool
)
from agent.responder import Responder
from services import (
    LLM,
    CoverLetterGenerator,
    JobExtractor,
    MatchAnalyzer,
    ResumeTailor,
    SkillMatcher
)
from collections.abc import Callable

logger = logging.getLogger(__name__)

_PROGRESS = {
    "extract_job": ("Extracted job description...", 20),
    "match_skills": ("Matched skills...", 40),
    "analyze_resume": ("Analyzed resume...", 60),
    "tailor_resume": ("Tailored resume...", 80),
    "generate_cover_letter": ("Generated cover letter...", 95)
}

class ApplicationAgent:
    """AI agent for tailoring resumes and generating cover letters."""

    def __init__(
        self,
        llm: LLM,
        job_extractor: JobExtractor,
        skill_matcher: SkillMatcher,
        match_analyzer: MatchAnalyzer,
        resume_tailor: ResumeTailor,
        cover_letter_generator: CoverLetterGenerator
    ) -> None:
        self.registry = self._create_registry(
            job_extractor,
            skill_matcher,
            match_analyzer,
            resume_tailor,
            cover_letter_generator
        )

        self.planner = Planner(llm=llm, registry=self.registry)
        self.responder = Responder(llm)

    def run(
        self,
        state: AgentState,
        user_message: str,
        progress_callback: Callable[[str, int], None] | None = None
    ) -> AgentState:
        """Execute the application agent."""
        
        max_steps = 2 * len(self.registry.list()) + 5
        tools_executed_this_request = set()

        for step in range(max_steps):
            decision = self.planner.plan(state)
            
            if decision.tool in tools_executed_this_request:
                decision = Decision(
                    tool="finish",
                    reason="The requested tool was just executed."
                )

            logger.info(
                "Step %d: Planner selected '%s' (%s)",
                step + 1,
                decision.tool,
                decision.reason
            )

            if decision.tool == "finish":
                state.add_assistant_message(self.responder.respond(state))
                
                if progress_callback:
                    progress_callback("Done!", 100)
                    
                logger.info("Application agent completed successfully.")
                return state

            tool = self.registry.get(decision.tool)
            
            if progress_callback:
                message, percent = _PROGRESS.get(
                    tool.name,
                    ("Running...", 0),
                )
                progress_callback(message, percent)

            if not tool.can_run(state):
                raise RuntimeError(
                    f"Planner selected '{tool.name}', "
                    "but its requirements are not satisfied."
                )

            logger.info("Executing tool '%s'.", tool.name)
            
            print(f"Planner chose: {decision.tool}")
            print(f"Reason: {decision.reason}")
            print(f"History: {state.tool_history_text()}")

            try:
                summary = tool.run(state)
            except Exception as exc:
                logger.exception("Tool '%s' failed.", tool.name)
                
                state.add_tool_execution(
                    tool=tool.name,
                    reason=decision.reason,
                    result=f"Failed: {exc}"
                )
                raise  
                
            state.complete_tool(tool.name)
            state.add_tool_execution(
                tool=tool.name,
                reason=decision.reason,
                result=summary
            )
            
            tools_executed_this_request.add(decision.tool)
            
            logger.info(
                "Finished tool '%s'.",
                tool.name
            )     

        raise RuntimeError(
            f"Planner exceeded the maximum number of steps ({max_steps})."
        )

    @staticmethod
    def _create_registry(
        job_extractor: JobExtractor,
        skill_matcher: SkillMatcher,
        match_analyzer: MatchAnalyzer,
        resume_tailor: ResumeTailor,
        cover_letter_generator: CoverLetterGenerator
    ) -> ToolRegistry:
        """Create the tool registry."""

        registry = ToolRegistry()

        registry.register(ExtractJobTool(job_extractor))
        registry.register(MatchSkillsTool(skill_matcher))
        registry.register(AnalyzeResumeTool(match_analyzer))
        registry.register(TailorResumeTool(resume_tailor))
        registry.register(GenerateCoverLetterTool(cover_letter_generator))

        return registry