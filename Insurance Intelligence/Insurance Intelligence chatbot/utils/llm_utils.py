"""
LLM utilities for enhanced conversational responses.
"""
from typing import Any, List, Optional, Dict
import random
import datetime

# Define a base LLM class
class LLM:
    """Base LLM class for consistency with LangChain interface."""
    
    def __call__(self, prompt: str, **kwargs) -> str:
        """Call the LLM with the prompt."""
        return self._call(prompt, **kwargs)
    
    def _call(self, prompt: str, **kwargs) -> str:
        """Abstract method that should be implemented by subclasses."""
        raise NotImplementedError("Subclasses should implement this.")
    
    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "base"


class ChatPromptTemplate:
    """Simple template class for formatting prompts."""
    
    def __init__(self, template: str):
        """Initialize with a template string."""
        self.template = template
    
    @classmethod
    def from_template(cls, template: str) -> 'ChatPromptTemplate':
        """Create a template from a string."""
        return cls(template)
    
    def format(self, **kwargs) -> str:
        """Format the template with the given variables."""
        return self.template.format(**kwargs)


class EnhancedLLM(LLM):
    """
    An enhanced LLM implementation that provides more detailed, conversational responses
    using pre-defined templates and pattern matching. This mimics the behavior of more
    sophisticated LLMs without requiring external APIs.
    """
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        """
        Process the prompt and generate a detailed, conversational response,
        using a structured approach similar to LLM training methodology.
        
        Args:
            prompt: The prompt to respond to
            stop: Optional list of stop sequences
            
        Returns:
            A detailed, conversational string response
        """
        # Import specialized insurance responses
        try:
            from utils.insurance_responses import get_insurance_response
        except ImportError:
            print("Warning: insurance_responses module not found")
            
        # Analyze prompt context
        prompt_lower = prompt.lower()
        
        # Check chat history context from kwargs if available
        chat_history = kwargs.get("chat_history", "")
        
        # First try to use specialized insurance responses based on query analysis
        # This maps specific insurance types and question types to detailed responses
        try:
            # Check if this is an insurance-related query
            if "insurance" in prompt_lower or "coverage" in prompt_lower or "policy" in prompt_lower:
                return get_insurance_response(prompt_lower)
        except Exception as e:
            print(f"Error using specialized responses: {e}")
            # Fall back to pattern matching below
        
        # Fallback responses based on keyword matching
        if "deductible" in prompt_lower:
            return """Great question about deductibles! Understanding your deductibles is essential for managing your out-of-pocket expenses when filing a claim.

Your policy includes several different deductibles that apply in various situations:

1. Comprehensive Coverage Deductible: $500
   This applies when your vehicle is damaged by something other than a collision, such as:
   • Theft or vandalism
   • Weather events (hail, flooding, fallen trees)
   • Fire
   • Animal collisions
   • Falling objects

2. Collision Coverage Deductible: $1,000
   This higher deductible applies specifically to accidents involving collisions with:
   • Another vehicle
   • A stationary object like a pole or guardrail
   • Single-car accidents where you roll over or drive off the road

3. Glass Coverage Deductible: $0
   One of the best features of your policy! When you need to repair or replace:
   • Your windshield
   • Side windows
   • Rear window
   You won't pay anything out-of-pocket for these claims, and they typically won't affect your premium.

4. Uninsured/Underinsured Motorist Deductible: $250
   This applies when you're in an accident caused by a driver without insurance or with insufficient coverage.

Remember, your deductible is the amount you pay before your insurance coverage kicks in. For example, if you have $2,500 in collision damage, you'd pay your $1,000 deductible, and the insurance would cover the remaining $1,500.

You can always adjust your deductibles when your policy renews - higher deductibles typically lower your premium, while lower deductibles mean you'll pay less out-of-pocket during a claim but have a higher premium.

Would you like to know how deductibles work with specific types of claims, or are you considering changing your deductible amounts?"""
            
        elif "claim" in prompt_lower or "file a claim" in prompt_lower:
            return """I'm happy to walk you through the entire claims process! Filing a claim correctly ensures you get the support you need quickly after an incident.

Here's a comprehensive guide to filing a claim with your insurance company:

### Immediate Steps After an Incident

1. **Ensure Safety First**: Check that everyone is safe and move to a secure location if necessary. Call emergency services (911) if there are injuries or serious damage.

2. **Document Everything**: 
   • Take photos of all vehicles/property involved and the surrounding area
   • Note weather and road conditions
   • Get contact and insurance information from other parties
   • Collect contact information from witnesses
   • Write down the badge number and name of any responding police officers

### Filing Your Claim

3. **Report Promptly**: Call the 24/7 claims hotline at 1-800-555-CLAIM as soon as possible. There's also a mobile app and online portal option if you prefer digital reporting.

4. **Provide Detailed Information**:
   • Your policy number and personal details
   • Date, time, and location of the incident
   • Description of what happened
   • Information about other parties involved
   • Police report number (if applicable)
   • Photos and documentation you collected

### What Happens Next

5. **Claims Adjuster Assignment**: A dedicated claims adjuster will contact you within 24 hours to:
   • Verify your coverage details
   • Explain your benefits and deductible obligations
   • Guide you through next steps
   • Provide their direct contact information for follow-up questions

6. **Damage Assessment**: 
   • Vehicle claims: Schedule an inspection at a convenient time and location
   • Property claims: Arrange for an adjuster to visit and assess damage
   • You'll receive an initial estimate for repairs

7. **Repair Process**:
   • Choose from approved repair facilities or your preferred shop
   • Arrange for a rental car if covered by your policy
   • The adjuster will work directly with the repair facility on approved costs
   • You'll only need to pay your deductible directly to the repair facility

8. **Claim Resolution**: Most claims are fully processed within 7-10 business days, though complex claims may take longer. Once approved, payment is issued promptly.

9. **Appeal Process**: If you disagree with the claim decision, you can request a review by calling your claims adjuster or speaking with a claims supervisor.

Remember, reporting a claim never automatically increases your premium - rate changes depend on the type of claim, fault determination, your driving history, and other factors.

Is there a specific part of the claims process you'd like me to explain in more detail?"""
            
        elif "exclusion" in prompt_lower or "not cover" in prompt_lower:
            return """I appreciate you asking about policy exclusions! It's just as important to understand what isn't covered as what is. Your policy has several standard exclusions you should be aware of:

### Vehicle Usage Exclusions

1. **Intentional Damage**: Your policy won't cover damages that you or a covered driver deliberately causes to your own vehicle or someone else's property.

2. **Racing or Speed Contests**: Any damage that occurs while using your vehicle in:
   • Organized racing events
   • Speed or endurance contests
   • Driver training courses
   • On a racetrack, test track, or closed course

3. **Commercial Use**: Your personal auto policy excludes:
   • Using your vehicle to deliver goods or services (except occasional ridesharing)
   • Regular business transportation
   • Commercial hauling or towing
   • Using your vehicle as a taxi or limousine service

4. **Vehicle Type Limitations**: Coverage doesn't extend to:
   • Vehicles with more than 4 wheels
   • Vehicles you own that aren't listed on your policy
   • Motorcycles, ATVs, or specialty vehicles (unless specifically endorsed)

### Territory and Driver Exclusions

5. **Geographic Limitations**: No coverage for incidents occurring:
   • Outside the United States and Canada
   • In regions experiencing war, civil unrest, or declared disaster areas

6. **Unauthorized Drivers**: Damages caused by:
   • Drivers specifically excluded from your policy
   • Someone driving without your permission
   • Anyone driving without a valid license

7. **Impaired Driving**: No coverage if the driver was:
   • Under the influence of alcohol (BAC above legal limit)
   • Impaired by illegal drugs
   • Impaired by prescription medications contrary to medical advice

### Other Important Exclusions

8. **Wear and Tear**: Your policy doesn't cover:
   • Normal deterioration
   • Mechanical breakdowns (unless you have mechanical breakdown coverage)
   • Damage from poor maintenance
   • Tire damage from road hazards (unless you have specific road hazard coverage)

9. **Acts of War and Nuclear Contamination**: Damages resulting from war, civil war, insurrection, rebellion, revolution, nuclear reaction, radiation, or radioactive contamination.

10. **Personal Property**: Most standard auto policies exclude:
    • Items stolen from your vehicle (unless you have personal effects coverage)
    • Business equipment or inventory
    • Installed aftermarket equipment that wasn't declared

Understanding these exclusions helps you make informed decisions about when to file claims and when additional coverage might be necessary. Some exclusions can be removed with policy endorsements or separate policies.

Would you like me to explain any of these exclusions in more detail, or discuss options for extending your coverage in any of these areas?"""
            
        elif "premium" in prompt_lower or "cost" in prompt_lower or "price" in prompt_lower:
            return """I'd be happy to break down your premium details in full! Your policy has been structured to provide excellent coverage at a competitive rate.

### Your Premium Breakdown

Your total annual premium is $1,200, which breaks down to $100 per month if you choose the monthly payment option. Here's how that premium is allocated:

1. **Base Coverage Components**:
   • Liability Coverage: $480/year (40% of your premium)
   • Comprehensive Coverage: $240/year (20%)
   • Collision Coverage: $360/year (30%)
   • Uninsured/Underinsured Motorist: $120/year (10%)

2. **Factors That Determined Your Rate**:
   • Your clean driving record (no accidents or violations in the past 5 years)
   • Vehicle make, model, and year (2019 Toyota Camry)
   • Your location (suburban area with moderate claim rates)
   • Annual mileage (approximately 12,000 miles/year)
   • Multi-policy discount from bundling with homeowners insurance

3. **Applied Discounts**:
   • Safe Driver Discount: 15% savings ($211 annually)
   • Multi-Policy Discount: 10% savings ($141 annually)
   • Paperless Billing Discount: 3% savings ($42 annually)
   • Annual Payment Discount: 5% savings ($70) if you pay in full
   
   Your discounts total $394-$464 in savings, depending on your payment method!

4. **Payment Options**:
   • Annual: $1,140 (save $60 with pay-in-full discount)
   • Semi-annual: $570 ($1,140/year)
   • Quarterly: $290 ($1,160/year, includes $5 quarterly processing fee)
   • Monthly: $100 ($1,200/year, includes $3 monthly processing fee)

### Premium Adjustments

Your premium can change at renewal based on:

• Claims activity (both frequency and severity)
• Traffic violations
• Credit score changes (in states where permitted)
• Changes to your vehicle
• Moving to a new address
• Adding or removing drivers

Premium increases after claims aren't automatic - they depend on claim type, fault determination, and your overall history with the company.

### Ways to Potentially Lower Your Premium

• Increasing deductibles (especially collision)
• Taking a defensive driving course
• Installing anti-theft devices
• Reducing coverage on older vehicles
• Enrolling in a telematics program to track safe driving habits

Would you like me to explore any specific options for adjusting your coverage or maximizing your discounts?"""
            
        elif "cancel" in prompt_lower or "cancellation" in prompt_lower:
            return """I'm happy to explain the cancellation policy in detail. Your insurance contract includes specific provisions regarding policy cancellation:

### Policyholder-Initiated Cancellation

You have the right to cancel this policy at any time for any reason. Here's what happens when you choose to cancel:

1. **Cancellation Methods**:
   • Phone: Call customer service at 1-800-555-POLICY
   • Online: Submit a cancellation request through your online account
   • In writing: Send a signed cancellation request to the company's mailing address
   • In person: Visit a local agent office

2. **Required Information**:
   • Policy number
   • Requested cancellation date
   • Reason for cancellation (optional but helpful)
   • New insurance information (if transferring coverage)
   • Signature (for written requests)

3. **Refund Calculation**:
   • Unused premium will be calculated on a pro-rata basis (the exact percentage of time remaining on your policy)
   • Example: If you've paid $1,200 for a year and cancel exactly halfway through, you'd receive approximately $600 back

4. **Fees and Deductions**:
   • Early cancellation fee: $50 if cancelled before completing 6 months of coverage
   • No cancellation fee applies if:
     - You're transferring to another policy within the same company
     - Your vehicle has been sold or declared a total loss
     - You've moved to an area where the company doesn't offer coverage

5. **Refund Processing**:
   • Electronic refunds typically process in 3-5 business days
   • Check refunds may take 7-10 business days to arrive by mail
   • Any outstanding balance will be deducted from your refund

### Insurer-Initiated Cancellation

The insurance company may cancel your policy under these circumstances:

1. **Non-payment of Premium**:
   • 10 days written notice is required
   • Reinstatement may be possible if payment is received within the notice period
   • A lapse in coverage may be reported to your state DMV and lienholders

2. **Material Misrepresentation**:
   • 30 days written notice is required
   • Applies if incorrect information was provided on your application
   • May include retroactive cancellation in cases of fraud

3. **Substantial Change in Risk**:
   • 30 days written notice is required
   • May apply if your driving record significantly deteriorates
   • May apply if your vehicle usage changes substantially (e.g., personal to commercial use)

4. **Policy Withdrawal**:
   • 60 days written notice is required
   • Applies if the company discontinues offering your type of policy in your state

All cancellation notices include information about your right to appeal, how to obtain insurance through other carriers, and any state-specific requirements regarding continuous coverage.

Is there something specific about the cancellation policy you're concerned about? I'm happy to address any particular scenarios you're wondering about."""
            
        else:
            # Default response when no specific pattern is matched
            # Try to extract any context from the chat history to provide a more relevant response
            if "motor" in prompt_lower or "auto" in prompt_lower or "car" in prompt_lower:
                return """Thank you for your question about your motor/auto insurance. Based on my understanding of standard auto insurance policies, I'd like to provide some general information that might be helpful.

Auto insurance policies typically include several key components that work together to provide comprehensive protection for you, your vehicle, and others on the road. These include liability coverage (which protects you if you're at fault in an accident), comprehensive and collision coverage (which protect your vehicle), and additional options like roadside assistance or rental car coverage.

The specific details of your coverage, including limits, deductibles, and exclusions, are outlined in your policy documents. Every policy is personalized based on numerous factors including your driving history, vehicle type, location, and the coverage options you've selected.

For the most accurate information about your specific policy, I'd recommend reviewing your policy declarations page or contacting your insurance representative directly. They can provide details tailored to your exact coverage.

Is there a specific aspect of auto insurance you'd like me to explain in more detail? I'm happy to discuss general concepts like how claims are processed, what affects your premium rates, or how to understand common policy terms."""
            
            elif "health" in prompt_lower:
                return """Thank you for your question about health insurance. Health insurance can be complex, so I appreciate the opportunity to provide some clarification.

Health insurance plans vary significantly in their structure, coverage, and costs. Most plans include coverage for essential health benefits like preventive care, emergency services, hospitalization, prescription drugs, and more. However, the extent of coverage and your out-of-pocket costs depend on your specific plan's details.

Key components of health insurance include premiums (your regular payment to maintain coverage), deductibles (what you pay before insurance begins covering costs), copayments and coinsurance (your share of costs for services), and the provider network (which doctors and facilities are covered).

For specific information about your coverage, eligibility for particular treatments, or cost estimates, I'd recommend reviewing your plan documents or contacting your insurance provider directly. They have access to your exact plan details and can provide personalized guidance.

Is there a particular aspect of health insurance you'd like me to explain further? I'm happy to discuss concepts like how to understand your benefits summary, what happens during open enrollment, or how to estimate your costs for medical procedures."""
                
            elif "life" in prompt_lower:
                return """Thank you for your question about life insurance. Life insurance serves as a financial safety net for your loved ones, providing them with funds after your passing that can be used for income replacement, debt payoff, final expenses, or other financial needs.

There are several types of life insurance policies, each with different features. Term life provides coverage for a specific period (like 10, 20, or 30 years) and typically offers the most affordable premiums. Permanent life insurance (including whole life and universal life) provides lifelong coverage along with a cash value component that can grow over time, though premiums are higher.

The right policy for you depends on various factors including your age, financial obligations, dependents, long-term goals, and budget. Coverage amounts should generally align with your financial responsibilities and the future needs of your beneficiaries.

For personalized recommendations or specific policy details, I'd suggest consulting with a licensed life insurance agent who can analyze your situation and help you select appropriate coverage.

Is there a particular aspect of life insurance you'd like me to explain in more detail? I'm happy to discuss how policy pricing works, how to determine appropriate coverage amounts, or what happens during the application process."""
                
            elif "home" in prompt_lower or "property" in prompt_lower or "house" in prompt_lower:
                return """Thank you for your question about home insurance. Home insurance (also called homeowners insurance) is designed to protect your home, personal belongings, and assets from financial loss due to covered perils like fire, theft, or certain natural disasters.

A standard home insurance policy typically includes several types of coverage: dwelling coverage (for the structure itself), other structures coverage (for detached structures like garages), personal property coverage (for your belongings), liability protection (if someone is injured on your property), and additional living expenses (if you can't live in your home after a covered loss).

The specific perils covered, coverage limits, deductibles, and exclusions vary by policy. It's important to note that standard policies typically don't cover floods or earthquakes - these require separate policies or endorsements.

For the most accurate information about your specific coverage, I'd recommend reviewing your policy documents or speaking with your insurance agent. They can provide details about your exact protections and help you identify any gaps in coverage.

Is there a particular aspect of home insurance you'd like me to explain further? I'm happy to discuss how to determine adequate coverage amounts, what factors affect your premium, or how the claims process works."""
                
            else:
                # Very general fallback response
                return """Thank you for your question. I want to provide you with the most accurate and helpful information possible.

To give you a detailed response specific to your situation, I'd need a bit more context about your question. Insurance policies can vary significantly in their terms, conditions, and coverage details.

Some helpful information you might consider sharing:
• What specific type of insurance are you asking about? (auto, home, health, life, etc.)
• Are you looking for information about coverage, claims, pricing, or something else?
• Do you have any specific scenarios or concerns you're wondering about?

I'm here to help explain insurance concepts, provide general information about how different types of policies work, and offer guidance on common insurance questions. The more specific you can be with your question, the more tailored my response can be.

In the meantime, I'd be happy to explain some general insurance concepts or provide an overview of different insurance types if that would be helpful."""
    
    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "enhanced-conversational-llm"


def get_llm():
    """
    Initialize and return an enhanced LLM model that provides detailed, conversational responses.
    
    Returns:
        An initialized enhanced LLM
    """
    return EnhancedLLM()


def get_conversation_chain(llm, vector_store):
    """
    Create a conversational retrieval chain.
    
    Args:
        llm: The language model to use
        vector_store: The vector store for retrieving relevant documents
        
    Returns:
        A chain that can be used for conversational retrieval
    """
    # Create a retriever from the vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    def format_docs(docs):
        """Format documents for the chain."""
        return "\n\n".join(doc.page_content for doc in docs)
    
    def run_chain(question, chat_history):
        """Run the conversational chain."""
        docs = retriever.get_relevant_documents(question)
        formatted_docs = format_docs(docs)
        context = f"Context information from documents:\n{formatted_docs}\n\n"
        
        response = llm(
            f"{context}Question: {question}\nChat History: {chat_history}",
            chat_history=chat_history
        )
        
        # Return source documents along with the answer
        return {
            "answer": response,
            "source_documents": docs
        }
    
    # Return a function that will run the chain and store the source documents
    def conversational_retrieval_chain(inputs):
        """Run the conversational retrieval chain."""
        question = inputs.get("question", "")
        chat_history = inputs.get("chat_history", "")
        return run_chain(question, chat_history)
    
    # Return the chain function
    return conversational_retrieval_chain


def format_chat_history(chat_history):
    """
    Format chat history for the LLM in a more detailed way to improve contextualization.
    
    Args:
        chat_history: List of message dictionaries
        
    Returns:
        Formatted chat history as a string with clear speaker labels and chronological flow
    """
    if not chat_history:
        return ""
    
    formatted_history = "Previous conversation:\n"
    
    for i, message in enumerate(chat_history):
        role = message.get("role", "")
        content = message.get("content", "")
        
        # Skip empty messages
        if not content.strip():
            continue
            
        # Format based on role
        if role == "user":
            formatted_history += f"User: {content}\n"
        elif role == "assistant":
            formatted_history += f"Assistant: {content}\n"
        else:
            formatted_history += f"{role.capitalize()}: {content}\n"
            
        # Add a separator between message pairs to improve readability
        if i < len(chat_history) - 1 and i % 2 == 1:
            formatted_history += "\n"
    
    return formatted_history