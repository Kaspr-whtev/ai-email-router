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

1. human-resources@example.com
    -sprawy rekrutacyjne
    -pytania o oferty pracy
    -wszelkie maile zwiazane z procesem rekrutacji
    Oto kilka przykładów maili które powinny trafić do tego działu:
        -"Chciałbym aplikować na stanowisko programisty"
        -"Czy Państwa firma wciąż szuka Project Managera?"
        -"Przesyłam moje CV"
        -"Nie mogę przesłać CV przez formularz rekrutacyjny"
2. help-desk@example.com
    -problemy z aplikacjami biznesowymi
    -zmiana i reset haseł
    -podstawowe problemy techniczne
    Oto kilka przykładów maili które powinny trafić do tego działu:
        -"Zapomniałem swojego hasła do konta"
        -"Aplikacja wyświetla błąd kiedy próbuję zapisać"
        -"Potrzebuję pomocy przy skonfigurowaniu podpisu w outlooku"
        -"Nie mogę zalogować się do portalu urlopowego"
3. it@example.com
    -tematy sprzętowe: komputery, laptopy, drukarki
    -sieć, VPN
    -awarie systemów lub sprzętu
    -przyznawanie dostępów i uprawnień 
    Oto kilka przykładów maili które powinny trafić do tego działu:
        -"Mam problem z laptopem"
        -"W biurze nie ma WiFi"
        -"Wnioskuję o dodatkowy monitor przy moim stanowisku"
        -"Potrzebuję dostępu do systemu kadrowego"
4. kadry@example.com
    -sprawy już zatrudnionych pracowników
    -umowy i świadczenia pracy
    -urlopy i zwolnienia lekarskie
    -wynagrodzenie
    Oto kilka przykładów maili które powinny trafić do tego działu:
        -"Chciałbym zawnioskować o urlop na przyszły tydzień"
        -"Proszę o informację o liczbie pozostałych dni urlopu"
        -"Zmieniłem adres zamieszkania i proszę o aktualizację danych"
        -"Mam pytanie dotyczące naliczenia urlopu"
5. other@example.com
    -wiadomości które nie pasują do żadnej z powyższych kategorii
    -wiadomości o niejednoznacznej treści
    Oto kilka przykładów maili które powinny trafić do tego działu:
        -"Proszę o kontakt z działem sprzedaży"
        -"Chciałbym zamówić pizzę"
        -"ASDASDASDsadfa"


Po wybraniu działu MUSISZ wywołać narzędzie send_email_tool.
Nie odpowiadaj zwykłym tekstem.
"""
)

@agent.tool
def send_email_tool(
    ctx: RunContext[EmailDeps],
    department: DepartmentEmail
) -> str:
    """
    Przesyła email użytkownika do odpowiedniego nadawcy

    tool potrzebuje wyłącznie department,
    temat i treść są załączone automatycznie, NIE podawaj ich
    """
    send_email(
        to_email=department,
        sender_email=ctx.deps.sender_email,
        message_text=ctx.deps.original_message,
    )

    return {"Sent"}

