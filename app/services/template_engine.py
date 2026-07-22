from typing import Dict, Any, List, Optional
from datetime import datetime

class RedFlag:
    def __init__(self, id: str, description: str, severity: str = "high"):
        self.id = id
        self.description = description
        self.severity = severity
        self.status = "excluded"  # "excluded" or "present"

class TemplateEngine:
    def __init__(self, template_data: Dict[str, Any], answers: Dict[str, Any]):
        self.template = template_data
        self.answers = answers
        self.red_flags: List[RedFlag] = []
        self._extract_red_flags()

    def _extract_red_flags(self):
        """Extract red flags from template data"""
        if "red_flags" in self.template:
            for flag in self.template["red_flags"]:
                self.red_flags.append(
                    RedFlag(
                        id=flag.get("id", ""),
                        description=flag.get("description", ""),
                        severity=flag.get("severity", "high")
                    )
                )

    def _evaluate_red_flag(self, flag: RedFlag) -> str:
        """Evaluate if a red flag is present or excluded"""
        # Check if the answer exists for this red flag
        if flag.id in self.answers:
            answer = self.answers[flag.id]
            # If answer is "yes", "present", or True, flag is present
            if answer in [True, "yes", "present", "Yes", "Present", "Yes, documented"]:
                return "present"
        return "excluded"

    def render(self) -> str:
        """Render the full template with red flags"""
        sections = self.template.get("sections", [])
        output = []

        # Add title
        output.append(f"# {self.template.get('title', 'Untitled')}")
        output.append("")

        # Render each section
        for section in sections:
            section_title = section.get("title", "Section")
            questions = section.get("questions", [])
            output.append(f"## {section_title}")
            
            for question in questions:
                qid = question.get("id", "")
                label = question.get("label", "")
                answer = self.answers.get(qid, "")
                
                if answer:
                    output.append(f"{label}: {answer}")
            
            output.append("")

        # Render Red Flags section
        if self.red_flags:
            output.append("## ⚠️ Red Flags")
            for flag in self.red_flags:
                status = self._evaluate_red_flag(flag)
                # Check if the answer indicates documented
                is_documented = self.answers.get(f"{flag.id}_documented", False)
                
                if status == "present":
                    doc_status = "and documented" if is_documented else "and NOT documented"
                    output.append(f"• {flag.description}: **PRESENT** {doc_status}")
                else:
                    output.append(f"• {flag.description}: **EXCLUDED**")
            output.append("")

        return "\n".join(output)

    def get_red_flags_status(self) -> List[Dict[str, str]]:
        """Get status of all red flags"""
        return [
            {
                "id": flag.id,
                "description": flag.description,
                "status": self._evaluate_red_flag(flag),
                "severity": flag.severity
            }
            for flag in self.red_flags
        ]