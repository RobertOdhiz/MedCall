from typing import List, Dict, Optional
from .watsonx import (
    analyze_symptoms,
    log_patient_info,
    evaluate_emergency,
    summarize_models_responses
)
import re

class WatsonXOrchestrator:
    def __init__(self):
        self.message_history = []
    
    def _add_message(self, role: str, content: str):
        """Add a message to the history with proper formatting"""
        cleaned_content = self._strip_mentions(content)
        self.message_history.append({"role": role, "content": cleaned_content})
    
    def _strip_mentions(self, text: str) -> str:
        """Remove Slack mentions from text"""
        return re.sub(r"<@[\w\d]+>", "", text).strip()
    
    def _determine_next_step(self, last_response: str) -> str:
        """
        Determine which agent to call next based on the last response.
        Returns the name of the next agent to call.
        """
        lower_response = last_response.lower()
        
        # Emergency detection logic
        if any(term in lower_response for term in ["emergency", "urgent", "immediate care", "911", "call for help", "hospital", "critical", "severe"]):
            return "emergency"
        
        # Incomplete information detection
        if any(term in lower_response for term in ["need more information", "not enough details", "clarify", "more details", "please specify", "specify", "elaborate", "explain", "more info"]):
            return "clarify"
            
        # Default workflow progression
        return "continue"
    
    def _handle_emergency(self) -> str:
        """Handle emergency situation workflow"""
        emergency_response = evaluate_emergency(self.message_history)
        self._add_message("assistant", f"EMERGENCY ALERT: {emergency_response}")
        return emergency_response
    
    def _handle_standard_flow(self) -> str:
        """Handle standard patient workflow"""
        # Step 1: Log patient information
        logging_response = log_patient_info(self.message_history)
        self._add_message("assistant", logging_response)
        
        # Step 2: Get final assessment
        summary_response = summarize_models_responses(self.message_history)
        self._add_message("assistant", summary_response)
        
        return summary_response
    
    def run_orchestration(self, message_history: List[Dict[str, str]]) -> str:
        """
        Main orchestration method that runs the complex workflow.
        
        Workflow:
        1. Analyze symptoms (always first)
        2. Determine if emergency
        3a. If emergency, handle immediately
        3b. If not, continue with standard flow
        4. Get final summary
        """
        self.message_history = message_history.copy()
        
        try:
            # Initial symptom analysis
            symptom_response = analyze_symptoms(self.message_history)
            self._add_message("assistant", symptom_response)
            
            # Determine next steps
            next_step = self._determine_next_step(symptom_response)
            
            if next_step == "emergency":
                return self._handle_emergency()
            elif next_step == "clarify":
                return "Please provide more details about your symptoms."
            else:
                return self._handle_standard_flow()
                
        except Exception as e:
            return f"An error occurred during processing: {str(e)}"