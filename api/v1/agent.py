from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from v1.schemas import DepartmentEmail
from v1.tools import send_email

provider = OllamaProvider(
    base_url="http://ollama:11434/v1"
)

model = OllamaModel(
    "llama3.2:3b",
    provider=provider
)

class EmailDeps:
    def __init__(self, sender_email: str, original_message: str):
        self.sender_email = sender_email
        self.original_message = original_message

agent = Agent(
    model=model,
    deps_type=EmailDeps,
    system_prompt="""
Jesteś systemem routingu zgłoszeń.

Na podstawie treści wiadomości wybierz dokładnie jeden dział:

- human-resources@example.com
- help-desk@example.com
- it@example.com
- kadry@example.com
- other@example.com

Po wybraniu działu MUSISZ wywołać narzędzie send_email.
Nie odpowiadaj zwykłym tekstem.
"""
)

@agent.tool
def send_email_tool(
    ctx: RunContext[EmailDeps],
    department_email: DepartmentEmail
) -> str:
    send_email(
        to_email=department_email,
        sender_email=ctx.deps.sender_email,
        message_text=ctx.deps.original_message,
    )

    return f"Email sent to {department_email}"

