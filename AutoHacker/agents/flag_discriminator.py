"""
CTF Flag Discriminator Agent with test
"""
import os
from cai.sdk.agents import Agent, handoff
from cai.sdk.agents.models.model_factory import get_model_provider
from cai.agents.one_tool import one_tool_agent

model = os.getenv('CAI_MODEL', "alias0")

flag_discriminator = Agent(
    name="Flag discriminator",
    description="Agent focused on extracting the flag from the output",
    instructions="""INSTRUCTIONS:
                1. You are an agent tailored to extract the flag from a given output.
                2. ONLY return the flag, nothing else.
                3. Flags can be in any format (not always CTF{...}).
                4. If you do not find a flag, call `ctf_agent` to continue investigating.
                """,
    model=get_model_provider(
        model_name="alias0" if os.getenv('CAI_MODEL') == "o3-mini" else model,
        agent_name="Flag discriminator",
        agent_type="flag_discriminator",
    ),
    handoffs=[
        handoff(
            agent=one_tool_agent,
            tool_name_override="ctf_agent",
            tool_description_override="Call the CTF agent to continue investigating if no flag is found"
        )
    ]
)

# Transfer Function
def transfer_to_flag_discriminator(**kwargs):  # pylint: disable=W0613
    """Transfer flag discriminator.
    Accepts any keyword arguments but ignores them."""
    return flag_discriminator
