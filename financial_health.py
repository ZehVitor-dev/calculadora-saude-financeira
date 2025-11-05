from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class FinancialHealthResult:
    score: float
    classificacao: str
    componentes: Dict[str, float]
    dicas: List[str]

def _clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))

def _classificar(score: float) -> str:
    if score >= 80:
        return "Saudável"
    if score >= 60:
        return "Atenção leve"
    if score >= 40:
        return "Atenção"
    return "Crítico"

def compute_financial_health(
    renda: float,
    despesas: float,
    dividas: float,
    poupanca: float,
    pesos: Tuple[float, float, float, float] = (0.35, 0.25, 0.25, 0.15),
) -> FinancialHealthResult:
    """
    Calcula um score (0–100) de saúde financeira + classificação.
    Entradas em moeda local (mesmo padrão). 'renda' e 'despesas' são mensais.
    pesos = (reserva, taxa_poupanca, endividamento, comprometimento_renda)
    """
    # Segurança numérica
    renda = max(0.0, float(renda))
    despesas = max(0.0, float(despesas))
    dividas = max(0.0, float(dividas))
    poupanca = max(0.0, float(poupanca))

    # Componentes (transformados para 0–100)
    # 1) Reserva de emergência: 6 meses = 100 (linear até 6)
    meses_reserva = (poupanca / (despesas if despesas > 0 else 1e-9)) if despesas > 0 else 0.0
    score_reserva = _clamp((meses_reserva / 6.0) * 100.0)

    # 2) Taxa de poupança: (renda - despesas)/renda (quanto maior, melhor)
    taxa_poupanca = ((renda - despesas) / renda) if renda > 0 else 0.0
    score_taxa = _clamp(taxa_poupanca * 100.0)

    # 3) Endividamento: dívida/renda (quanto menor, melhor). >=1 => 0.
    divida_renda = (dividas / renda) if renda > 0 else 10.0
    score_endiv = _clamp((1.0 - divida_renda) * 100.0)

    # 4) Comprometimento da renda: despesas/renda (quanto menor, melhor)
    comp_renda = (despesas / renda) if renda > 0 else 1.0
    score_comp = _clamp((1.0 - comp_renda) * 100.0)

    w1, w2, w3, w4 = pesos
    total_peso = max(1e-9, w1 + w2 + w3 + w4)
    score = (
        w1 * score_reserva +
        w2 * score_taxa +
        w3 * score_endiv +
        w4 * score_comp
    ) / total_peso
    score = round(_clamp(score), 2)

    classificacao = _classificar(score)

    dicas: List[str] = []
    if meses_reserva < 6:
        faltam = max(0.0, 6.0 - meses_reserva)
        dicas.append(f"Aumente a reserva de emergência (+{faltam:.1f} meses).")
    if taxa_poupanca < 0.2:
        dicas.append("Tente poupar pelo menos 20% da renda mensal (ou reduzir despesas).")
    if divida_renda > 0.3:
        dicas.append("Reduza a razão dívida/renda para abaixo de 30%.")
    if comp_renda > 0.7:
        dicas.append("Comprometimento alto da renda; revise custos fixos/variáveis.")

    componentes = {
        "reserva_emergencia": round(score_reserva, 2),
        "taxa_poupanca": round(score_taxa, 2),
        "endividamento": round(score_endiv, 2),
        "comprometimento_renda": round(score_comp, 2),
    }

    return FinancialHealthResult(
        score=score,
        classificacao=classificacao,
        componentes=componentes,
        dicas=dicas
    )

