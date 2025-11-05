from financial_health import compute_financial_health

def test_basico_existe():
    res = compute_financial_health(3000, 2000, 500, 3000)
    assert 0 <= res.score <= 100
    assert res.classificacao in {"Crítico", "Atenção", "Atenção leve", "Saudável"}

def test_melhora_quando_poupanca_sobe():
    res1 = compute_financial_health(3000, 2000, 500, 0)
    res2 = compute_financial_health(3000, 2000, 500, 12000)  # 6 meses de reserva
    assert res2.score >= res1.score

