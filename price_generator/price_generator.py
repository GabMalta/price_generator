from typing import List, Literal

faixas_comissoes = {
    "shopee": {
        1: {"preco_max": 79.99, "taxa_fixa": 4.50, "comissao_percentual": 0.2},
        2: {"preco_max": 99.99, "taxa_fixa": 16.00, "comissao_percentual": 0.14},
        3: {"preco_max": 199.99, "taxa_fixa": 20.00, "comissao_percentual": 0.14},
        4: {"preco_max": 499.99, "taxa_fixa": 26.00, "comissao_percentual": 0.14},
    },
    "mercadolivre": {
        1: {"preco_max": 18.99, "taxa_fixa": 8.93, "comissao_percentual": 0.17},
        2: {"preco_max": 48.99, "taxa_fixa": 9.93, "comissao_percentual": 0.17},
        3: {"preco_max": 78.99, "taxa_fixa": 11.64, "comissao_percentual": 0.17},
        4: {"preco_max": 99.99, "taxa_fixa": 28.90, "comissao_percentual": 0.17},
        5: {"preco_max": 119.99, "taxa_fixa": 33.70, "comissao_percentual": 0.17},
        6: {"preco_max": 149.99, "taxa_fixa": 38.50, "comissao_percentual": 0.17},
        7: {"preco_max": 199.99, "taxa_fixa": 43.30, "comissao_percentual": 0.17},
        8: {"preco_max": 200, "taxa_fixa": 49.30, "comissao_percentual": 0.17},
    },
}


# DEPRECEATED
def commission_marketplace(fixed_cost: list = [4], variable_cost: list = [20]) -> dict:
    cost_f = 0
    cost_v = 0

    for x in fixed_cost:
        cost_f += x

    for x in variable_cost:
        cost_v += x

    return {"fixed_cost": cost_f, "variable_cost": cost_v}


# DEPRECEATED
def price_generator(
    cost_price: float,
    multiplier: float,
    profit_margin: float,
    discount: float = 23.5,
    tax: float = 5,
    rule_comission: callable = commission_marketplace,
) -> float:

    cost_commission = rule_comission()

    cost = (cost_price - (cost_price * (discount / 100))) * multiplier

    cost_total = cost + cost_commission["fixed_cost"]

    divisor_number = (
        100 - profit_margin - tax - cost_commission["variable_cost"]
    ) / 100

    price = cost_total / divisor_number

    return rounded_number(price), rounded_number(cost)


def rounded_number(value) -> float:
    # Separar a parte inteira e a parte decimal
    integer_part = int(value)
    decimal_part = value % 1

    # Encontrar a primeira casa decimal
    first_decimal = int(decimal_part * 10) / 10

    # Ajustar o valor com base na parte decimal
    if decimal_part < first_decimal + 0.05:
        return integer_part + first_decimal - 0.01
    else:
        return integer_part + first_decimal + 0.09


def get_divisor(variables: List[float]) -> float:
    variables_in_percentage = sum([var / 100 for var in variables])

    if variables_in_percentage >= 1:
        raise ValueError("A soma das variáveis de percentual deve ser menor que 100%.")

    return 1 - variables_in_percentage


def calculate_commission_range(variables: List[float], marketplace="shopee"):
    commission_range_calculations = {}

    faixa_comissoes_marketplace = faixas_comissoes.get(marketplace)

    if not faixa_comissoes_marketplace:
        return None

    for key, range_info in faixa_comissoes_marketplace.items():
        variables_with_commission = variables + [
            range_info["comissao_percentual"] * 100
        ]
        divisor = get_divisor(variables_with_commission)

        preco_max = range_info["preco_max"]
        taxa_fixa = range_info["taxa_fixa"]
        comissao_percentual = range_info["comissao_percentual"]
        custo_max = (preco_max * divisor) - taxa_fixa

        commission_range_calculations[key] = {
            "preco_max": preco_max,
            "custo_max": round(custo_max, 2),
            "taxa_fixa": taxa_fixa,
            "comissao_percentual": comissao_percentual,
            "divisor": round(divisor, 3),
        }

    return commission_range_calculations


def calculate_price(
    cost_price: float,
    multiplier: float,
    profit_margin: float,
    discount: float = 23.5,
    imposto=5.00,
    marketplace: Literal["shopee", "mercadolivre"] = "shopee",
) -> float:

    last_range = None

    custo = (cost_price - (cost_price * (discount / 100))) * multiplier

    variables = [imposto, profit_margin]

    commission_ranges = calculate_commission_range(variables, marketplace)

    if not commission_ranges:
        return

    for key, value in commission_ranges.items():
        last_range = value

        if custo <= value["custo_max"]:
            preco_ideal = (custo + value["taxa_fixa"]) / value["divisor"]

            return rounded_number(preco_ideal), round(custo, 2)

    # If custo exceeds all ranges, use the last (highest) range
    if last_range is not None:
        preco_ideal = (custo + last_range["taxa_fixa"]) / last_range["divisor"]

        return rounded_number(preco_ideal), round(custo, 2)
    # This should never happen, but as a safety fallback
    raise ValueError(
        "Custo excede o máximo permitido para todas as faixas de comissão."
    )
