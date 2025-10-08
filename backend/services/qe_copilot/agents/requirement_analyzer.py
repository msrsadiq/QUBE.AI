from typing import Dict, Any, List
from .base_agent import BaseAgent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import time

class RequirementAnalyzer(BaseAgent):
    """Agent for analyzing requirements for clarity, completeness, risks, etc."""
    
    def get_prompt_template(self) -> str:
        return """
        Analyze the following requirement for a QA testing perspective:
        
        Requirement Title: {title}
        Description: {description}
        Acceptance Criteria: {acceptance_criteria}
        
        Please analyze and provide:
        1. Clarity Score (1-10): Is the requirement unambiguous?
        2. Completeness Score (1-10): Does it cover all scenarios?
        3. Consistency Check: Any contradictions with common patterns?
        4. Feasibility Assessment: Can it be realistically tested?
        5. Identified Risks:
           - QE/Architecture risks
           - Delivery risks
           - Automation feasibility
        6. User Journeys identified
        7. Required Permissions/Access
        8. INVEST Compliance (for user stories)
        9. Testability Assessment
        10. Integration Points
        11. Suggested Test Coverage Areas
        
        Provide the analysis in JSON format.
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        
        prompt = PromptTemplate(
            input_variables=["title", "description", "acceptance_criteria"],
            template=self.get_prompt_template()
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            result = await chain.arun(
                title=input_data.get("title", ""),
                description=input_data.get("description", ""),
                acceptance_criteria=str(input_data.get("acceptance_criteria", []))
            )
            
            # Parse the LLM response (assuming JSON format)
            import json
            analysis_results = json.loads(result)
            
            output_data = {
                "requirement_id": input_data.get("requirement_id"),
                "analysis": analysis_results,
                "recommendations": self._generate_recommendations(analysis_results)
            }
            
            execution_time = int((time.time() - start_time) * 1000)
            await self.store_io(input_data, output_data, execution_time)
            
            return output_data
            
        except Exception as e:
            self.logger.error(f"Error analyzing requirement: {str(e)}")
            execution_time = int((time.time() - start_time) * 1000)
            await self.store_io(input_data, {"error": str(e)}, execution_time, "failed")
            raise
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        recommendations = []
        
        if analysis.get("clarity_score", 0) < 7:
            recommendations.append("Requirement needs more clarity. Consider adding specific examples.")
        
        if analysis.get("completeness_score", 0) < 7:
            recommendations.append("Add edge cases and error scenarios to the requirement.")
        
        if not analysis.get("testability_assessment", {}).get("is_testable"):
            recommendations.append("Requirement needs more specific acceptance criteria for testing.")
        
        return recommendations