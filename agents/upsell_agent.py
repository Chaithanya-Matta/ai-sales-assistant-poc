from langgraph.types import Command
from state.state import State, Message
from typing import Literal

# Dummy Upsell Agent Node
def upsell_recommendation_agent(state: State) -> Command[Literal["supervisor"]]:
    """
    This is a placeholder upsell agent that generates dummy recommendations.
    In a real system, this would use customer profile, pest trends, etc.
    """
    # Example: hardcoded mock recommendation
    mock_recommendation = {
        "customer_id": "123456",
        "recommended_services": [
            {
                "service": "Termite Barrier Protection",
                "reason": "High termite activity in your zip code."
            },
            {
                "service": "Mosquito Monthly Plan",
                "reason": "Recommended for summer season."
            }
        ]
    }

    # Add the message to conversation history
    message_text = "I recommend the following services based on your location and season: Termite Barrier Protection and Mosquito Monthly Plan."
    state.messages.append(Message(role="upsell", content=message_text))

    return Command(
        goto="supervisor",
        update={
            "upsell_data": mock_recommendation,
            "messages": state.messages
        }
    )
