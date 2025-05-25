# Stalowa Wola: Kosmos i Obronność Dashboard

Interaktywny dashboard prezentujący dane i analizy dotyczące projektów kosmicznych i obronnych w Stalowej Woli.

## Wymagania

- Python 3.8+
- pip (Python package manager)

## Instalacja

1. Sklonuj repozytorium lub rozpakuj pliki do wybranego folderu

2. Zainstaluj wymagane zależności:
```bash
pip install -r requirements.txt
```

3. Upewnij się, że plik `Stalowa Wola_ Kosmos i Obronność_.docx` znajduje się w głównym katalogu projektu

## Uruchomienie aplikacji

1. W terminalu przejdź do katalogu projektu

2. Uruchom aplikację Streamlit:
```bash
streamlit run projekt26.py
```

3. Aplikacja otworzy się automatycznie w domyślnej przeglądarce pod adresem `http://localhost:8501`

## Funkcjonalności

- Interaktywna mapa Stalowej Woli
- Analiza SWOT
- Wizualizacja projektów flagowych
- Sieć współpracy partnerów
- Analiza finansowania
- Wskaźniki KPI
- Chatbot z dokumentacją

## Uwaga

Aby chatbot działał poprawnie, należy ustawić zmienną środowiskową `OPENAI_API_KEY` z kluczem API OpenAI:

Windows:
```bash
set OPENAI_API_KEY=your-api-key-here
```

Linux/MacOS:
```bash
export OPENAI_API_KEY=your-api-key-here
```

## Kontakt

W razie pytań lub problemów, proszę o kontakt przez formularz w aplikacji. 