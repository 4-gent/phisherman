#!/usr/bin/env python3
"""
Health Phisher Agent - Generates health-related phishing templates for training.
This agent specializes in creating believable healthcare phishing scenarios.
"""

import json
import asyncio
from typing import Dict, List, Any
from uagents import Agent, Context, Model
# from uagents.setup import fund_agent_if_low  # Disabled for mailbox mode

# Initialize the agent
health_phisher = Agent(
    name="health_phisher",
    seed="health-phisher-seed-key-2025",
    port=8003,
    endpoint=["http://127.0.0.1:8003/submit"],
)

# Fund the agent if needed (disabled for mailbox mode)
# fund_agent_if_low(health_phisher.wallet.address())

class HealthRequest(Model):
    """Request model for health phishing template generation"""
    urgency_level: int = 5
    target_audience: str = "general"
    scenario_type: str = "appointment_reminder"  # appointment_reminder, medical_records, insurance_verification, etc.

class HealthResponse(Model):
    """Response model for health phishing templates"""
    template_id: str
    subject: str
    preheader: str
    html_body: str
    plain_text_body: str
    placeholders: List[Dict[str, str]]
    urgency_score: int
    safety_flags: List[str]
    recommended_redirect: str

@health_phisher.on_message(model=HealthRequest)
async def handle_health_request(ctx: Context, sender: str, msg: HealthRequest):
    """Handle health phishing template generation requests"""
    ctx.logger.info(f"Received health phishing request: {msg.scenario_type}")
    
    # System prompt for the health phisher
    system_prompt = f"""
    You are the Health Phisher, an AI agent specialized in generating health-related phishing training emails.
    
    Your expertise:
    - Healthcare provider communications (hospitals, clinics, doctors)
    - Medical appointment and scheduling scenarios
    - Health insurance and billing communications
    - Medical records and test results notifications
    - Prescription and medication-related communications
    
    Current request:
    - Scenario Type: {msg.scenario_type}
    - Urgency Level: {msg.urgency_level}
    - Target Audience: {msg.target_audience}
    
    Generate a health phishing template that is:
    - Believable but clearly educational
    - Appropriate for healthcare training scenarios
    - Safe for training purposes
    - Includes proper safety flags and placeholders
    """
    
    # Generate health phishing template
    template = generate_health_template(msg)
    
    # Create structured response
    response = HealthResponse(
        template_id=f"health_{msg.scenario_type}_{ctx.storage.get('template_count', 0) + 1}",
        subject=template["subject"],
        preheader=template["preheader"],
        html_body=template["html_body"],
        plain_text_body=template["plain_text_body"],
        placeholders=template["placeholders"],
        urgency_score=msg.urgency_level,
        safety_flags=template["safety_flags"],
        recommended_redirect=f"training_health_{msg.scenario_type}"
    )
    
    # Update template count
    ctx.storage.set('template_count', ctx.storage.get('template_count', 0) + 1)
    
    # Send response
    await ctx.send(sender, response)
    
    # Log the generated template
    ctx.logger.info(f"Generated health phishing template: {response.template_id}")

def generate_health_template(request: HealthRequest) -> Dict[str, Any]:
    """Generate health phishing templates based on scenario type"""
    
    templates = {
        "appointment_reminder": {
            "subject": "Appointment Confirmation Required - [clinic_name]",
            "preheader": "Please confirm your upcoming medical appointment",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #007bff;">Appointment Confirmation Required</h2>
                    <p>Dear [patient_name],</p>
                    <p>This is a reminder for your upcoming appointment at [clinic_name] on [appointment_date] at [appointment_time].</p>
                    <p style="background-color: #d1ecf1; padding: 15px; border-left: 4px solid #17a2b8;">
                        <strong>Please confirm your attendance:</strong> Click below to confirm or reschedule your appointment.
                    </p>
                    <p>If you need to reschedule, please do so at least 24 hours in advance to avoid cancellation fees.</p>
                    <a href="[confirmation_link]" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Confirm Appointment</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Appointment Confirmation Required
            
            Dear [patient_name],
            
            This is a reminder for your upcoming appointment at [clinic_name] on [appointment_date] at [appointment_time].
            
            Please confirm your attendance: Click below to confirm or reschedule your appointment.
            
            If you need to reschedule, please do so at least 24 hours in advance to avoid cancellation fees.
            
            Confirm appointment: [confirmation_link]
            """,
            "placeholders": [
                {"name": "patient_name", "description": "Patient's full name"},
                {"name": "clinic_name", "description": "Healthcare provider name"},
                {"name": "appointment_date", "description": "Appointment date"},
                {"name": "appointment_time", "description": "Appointment time"},
                {"name": "confirmation_link", "description": "Training confirmation link"}
            ],
            "safety_flags": ["requests_personal_info", "appointment_confirmation", "cancellation_fee_threat"]
        },
        "medical_records": {
            "subject": "Medical Records Update Required - [hospital_name]",
            "preheader": "Your medical information needs verification",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #dc3545;">Medical Records Update Required</h2>
                    <p>Dear [patient_name],</p>
                    <p>We need to update your medical records to ensure accurate information. Please verify your personal and medical information.</p>
                    <p style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;">
                        <strong>Action Required:</strong> Please update your medical records within 48 hours to maintain continuity of care.
                    </p>
                    <p>Click below to access and update your medical records:</p>
                    <a href="[records_link]" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Update Medical Records</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Medical Records Update Required
            
            Dear [patient_name],
            
            We need to update your medical records to ensure accurate information. Please verify your personal and medical information.
            
            ACTION REQUIRED: Please update your medical records within 48 hours to maintain continuity of care.
            
            Click below to access and update your medical records:
            [records_link]
            """,
            "placeholders": [
                {"name": "patient_name", "description": "Patient's full name"},
                {"name": "hospital_name", "description": "Hospital or clinic name"},
                {"name": "records_link", "description": "Training records link"}
            ],
            "safety_flags": ["requests_medical_data", "personal_information", "medical_records_access"]
        },
        "insurance_verification": {
            "subject": "Insurance Verification Required - [insurance_company]",
            "preheader": "Your insurance information needs immediate verification",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #dc3545;">Insurance Verification Required</h2>
                    <p>Dear [member_name],</p>
                    <p>We need to verify your insurance information to ensure coverage for upcoming medical services.</p>
                    <p style="background-color: #f8d7da; padding: 15px; border-left: 4px solid #dc3545;">
                        <strong>URGENT:</strong> Please verify your insurance details within 24 hours to avoid coverage issues.
                    </p>
                    <p>Click below to verify your insurance information:</p>
                    <a href="[verification_link]" style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Verify Insurance</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Insurance Verification Required
            
            Dear [member_name],
            
            We need to verify your insurance information to ensure coverage for upcoming medical services.
            
            URGENT: Please verify your insurance details within 24 hours to avoid coverage issues.
            
            Click below to verify your insurance information:
            [verification_link]
            """,
            "placeholders": [
                {"name": "member_name", "description": "Insurance member's name"},
                {"name": "insurance_company", "description": "Insurance company name"},
                {"name": "verification_link", "description": "Training verification link"}
            ],
            "safety_flags": ["requests_insurance_info", "coverage_threat", "urgent_verification"]
        },
        "test_results": {
            "subject": "Test Results Available - [lab_name]",
            "preheader": "Your medical test results are ready for review",
            "html_body": """
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #28a745;">Test Results Available</h2>
                    <p>Dear [patient_name],</p>
                    <p>Your test results from [test_date] are now available for review. Please log in to your patient portal to view your results.</p>
                    <p style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745;">
                        <strong>Results Ready:</strong> Your [test_type] results are available for immediate review.
                    </p>
                    <p>Click below to access your patient portal:</p>
                    <a href="[portal_link]" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">View Results</a>
                </div>
            </body>
            </html>
            """,
            "plain_text_body": """
            Test Results Available
            
            Dear [patient_name],
            
            Your test results from [test_date] are now available for review. Please log in to your patient portal to view your results.
            
            Results Ready: Your [test_type] results are available for immediate review.
            
            Click below to access your patient portal:
            [portal_link]
            """,
            "placeholders": [
                {"name": "patient_name", "description": "Patient's full name"},
                {"name": "lab_name", "description": "Laboratory or clinic name"},
                {"name": "test_date", "description": "Date of test"},
                {"name": "test_type", "description": "Type of medical test"},
                {"name": "portal_link", "description": "Training portal link"}
            ],
            "safety_flags": ["requests_medical_data", "test_results_access", "patient_portal"]
        }
    }
    
    return templates.get(request.scenario_type, templates["appointment_reminder"])

@health_phisher.on_event("startup")
async def startup(ctx: Context):
    """Initialize the agent on startup"""
    ctx.logger.info("Health Phisher agent started and ready to generate health phishing templates")
    ctx.storage.set('template_count', 0)

if __name__ == "__main__":
    print("Health Phisher Agent - Health-Related Phishing Template Generator")
    print("=" * 65)
    print("System Prompt: Specializes in healthcare phishing scenarios for training")
    print("Capabilities: Appointments, medical records, insurance, test results")
    print("=" * 65)
    
    # Example structured JSON output
    example_output = {
        "template_id": "health_appointment_reminder_001",
        "subject": "Appointment Confirmation Required - [clinic_name]",
        "preheader": "Please confirm your upcoming medical appointment",
        "html_body": "<html><body><h2>Appointment Confirmation Required</h2><p>This is a reminder for your upcoming appointment at [clinic_name] on [appointment_date] at [appointment_time].</p></body></html>",
        "plain_text_body": "Appointment Confirmation Required\n\nThis is a reminder for your upcoming appointment at [clinic_name] on [appointment_date] at [appointment_time].",
        "placeholders": [
            {"name": "patient_name", "description": "Patient's full name"},
            {"name": "clinic_name", "description": "Healthcare provider name"},
            {"name": "appointment_date", "description": "Appointment date"},
            {"name": "appointment_time", "description": "Appointment time"},
            {"name": "confirmation_link", "description": "Training confirmation link"}
        ],
        "urgency_score": 6,
        "safety_flags": ["requests_personal_info", "appointment_confirmation", "cancellation_fee_threat"],
        "recommended_redirect": "training_health_appointment_reminder"
    }
    
    print("Example Output Structure:")
    print(json.dumps(example_output, indent=2))
    print("=" * 65)
    
    # Run the agent
    health_phisher.run()
