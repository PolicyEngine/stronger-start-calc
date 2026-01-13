# Stronger Start for Working Families Act Calculator

Analysis of the Stronger Start for Working Families Act, bipartisan legislation that would eliminate the $2,500 earnings requirement for the refundable portion of the federal Child Tax Credit.

## Key Findings

- **Cost**: $789 million in 2026
- **Beneficiaries**: 3.4% of Americans
- **Child Poverty Reduction**: 0.11%
- **Maximum Household Benefit**: $375

## Usage

### Installation

```bash
pip install -e .
```

### Generate Charts

```bash
python generate_post.py
```

This will create HTML chart files in `output/charts/`:
- `net-income-change.html` - Figure 1: Change in net income for a single parent with two children
- `winners-by-decile.html` - Figure 2: Winners by income decile
- `avg-benefit-by-decile.html` - Figure 3: Average benefit by income decile

## Charts

After deployment, charts are available at:
- https://policyengine.github.io/stronger-start-calc/net-income-change.html
- https://policyengine.github.io/stronger-start-calc/winners-by-decile.html
- https://policyengine.github.io/stronger-start-calc/avg-benefit-by-decile.html

## License

MIT
