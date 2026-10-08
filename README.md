# price-generator

Cálculo de custo e preço de venda para marketplaces (Shopee, Mercado Livre).
Sem dependências externas — apenas a biblioteca padrão do Python.

## Instalação via Git

```bash
pip install git+https://github.com/GabMalta/price_generator.git
```

Para fixar uma tag ou branch específica:

```bash
pip install git+https://github.com/GabMalta/price_generator.git@0.1.0
```

Em `requirements.txt`:

```
price-generator @ git+https://github.com/GabMalta/price_generator.git@0.1.0
```

## Uso

```python
from price_generator import calculate_price

preco, custo = calculate_price(cost_price=20.0, multiplier=1.5, profit_margin=20)
print(preco, custo)  # 48.99 22.95
```

## API

- `calculate_price`: preço de venda e custo total a partir do custo do produto.
- `price_generator`: cálculo do preço dado o divisor de comissões.
- `calculate_commission_range`: resolve a comissão por faixa de preço do marketplace.
- `commission_marketplace`: monta o dicionário de custos fixos e variáveis.
- `get_divisor`: divisor a partir da lista de percentuais.
- `rounded_number`: arredondamento comercial do preço final.
