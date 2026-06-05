# System przekierowywania wiadomości email AI / AI email router
Ta aplikacja udostępnia edpoint POST, który przyjmuje wiadomość email, treść tej wiadomości jest analizowana przez LLM i przekazywana do odpowiedniego działu.

## Instalacja i uruchomienie
Wymagane są Docker oraz git (do sklonowania repozytorium).

1. W wybranym folderze należy skolować repozytorium: ```git clone https://github.com/Kaspr-whtev/ai-email-router.git```
2. Upewnić się że silnik Dockera jest włączony (Docker Engine running)
3. Wewnątrz głównego folderu sklonowanego repozytorium uruchomić: ```docker compose up -d```

Po tych krokach i odczekaniu na pęłną instalację aplikacji jest ona gotowa do użycia:
1. ```localhost:8000/api/v1/docs``` pod tym adresem jest Swagger/dokumentacja endpointu
2. ```localhost:8025``` pod tym adresem jest "skrzynka mailowa" MailHog

Można przetestować działanie ze strony Swaggera, naciskając 'try it out' lub przykładowym cURL:
```
curl -X 'POST' \
  'http://localhost:8000/api/v1/route-messages' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "jan.nowak@example.com",
  "message": "Nie działa mi komputer"
}'
```

## Struktura plików
W głównym folderze znajduje się docker-compose.yml, który definiuje jakie kontenery są inicjalizowane.
W katalogu api są 2 dodatkowe pliki pomocnicze, requirements.txt (który definiuje potrzebne paczki) oraz Dockerfile (który je instaluje).
Dalej jest katalog v1 który przechowuje kod aplikacji:
  1. main.py: przy uruchomieniu upewnia się że model llm został pobrany oraz udostępnia endpoint
  2. agent.py: przechowuje agenta AI, wraz z promptem oraz toolem który wywołuje
  3. tools.py: ma metodę wysyłającą email
  4. schemas.py: ma schematy danych (klasy) jakie są przekazywane w aplikacji

## Model LLM
Model jakiego używa ta aplikacja to Llama3.1:8b, jest to ciężki model, który może zająć kilka minut aby się zainstalować. Ten model wydaje się na zbyt złożony dla skomplikowania problemu, jednak był on pierwszym, który spełniał wszytkie potrzeby aplikacji na akceptowalnym poziomie.
Oto lista modeli jakie przetestowałem oraz powód dlaczego przeszedłem do kolejnego:
 1. Qwen3:1.7b - problem z kompatybilnością z wersją pydantic_ai
 2. Qwen3:4b - problemy z poprawną klasyfikacją oraz dłuższe wywołanie narzędzia przez jego "myślenie" (thinking/reasoning)
 3. Llama3.2:3b - problemy z wywołaniem tool
 4. Qwen3:8b - problem z długością "myślenia", który mógł zająć nawet kilka minut
Dlatego skończyłem na modelu Llama3.1:8b.

### Możliwości usprawnienia
Jeśli pisałbym tę aplikację od nowa, spróbowałbym rozwiązać problem kompatybilności modelu Qwen3:1.7 z pydantic_ai, na który natrafiłem.
Alternatywą jest wykorzystanie jednego z innych modeli Qwen3 i stworzenie własnej wersji z wyłączonym "thinking".

## Kontenery docker
W trakcie działania aplikacji działają 3 kontenery:
  1. mailhog (obraz mailhog/mailhog): uruchamiany na portach 1025 i 8025, serwer ten wysyła i odbiera emaile wysyłane przez system
  2. ollama (obraz ollama/ollama): uruchamiany na porcie 11434, przechowuje on model językowy
  3. api: uruchamiany na porcie 8000: hostuje kod i polega on na statusie healthy kontenera ollama
Dodatkowo jest 4ty kontener odpowiedzialny za pobranie modelu LLM: ollama-init (obraz curlimages/curl). Pobiera on LLM, ładuje go do wolumenu (volume) i wysyła do ai "ping", aby ten załadował wagi do pamięci.
Ostatnim elementem dockerowym jest wolumen (volume) ollama_data, który głównie przechowuje dane LLM.
