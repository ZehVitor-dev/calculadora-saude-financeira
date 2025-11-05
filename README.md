![tests](https://github.com/@ZehVitor-dev/calculadora-saude-financeira/actions/workflows/python-tests.yml/badge.svg)

# calculadora-saude-financeira

# Calculadora de Saúde Financeira (Python)

Função simples que calcula um **score (0–100)** e uma **classificação** da saúde financeira,
com base em reserva de emergência, taxa de poupança, endividamento e comprometimento da renda.

## Como usar (CLI)
```bash
python example.py --renda 3000 --despesas 2200 --dividas 800 --poupanca 2500
# ou JSON:
python example.py --renda 3000 --despesas 2200 --dividas 800 --poupanca 2500 --json
