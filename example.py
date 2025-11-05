import json
import argparse
from financial_health import compute_financial_health

def main():
    p = argparse.ArgumentParser(description="Calculadora de saúde financeira")
    p.add_argument("--renda", type=float, required=True)
    p.add_argument("--despesas", type=float, required=True)
    p.add_argument("--dividas", type=float, default=0.0)
    p.add_argument("--poupanca", type=float, default=0.0)
    p.add_argument("--json", action="store_true", help="Saída em JSON")
    args = p.parse_args()

    res = compute_financial_health(
        renda=args.renda,
        despesas=args.despesas,
        dividas=args.dividas,
        poupanca=args.poupanca,
    )

    if args.json:
        print(json.dumps(res.__dict__, ensure_ascii=False, indent=2))
    else:
        print(f"Score: {res.score} | Classificação: {res.classificacao}")
        print("Componentes:", res.componentes)
        if res.dicas:
            print("Dicas:")
            for d in res.dicas:
                print("-", d)

if __name__ == "__main__":
    main()

