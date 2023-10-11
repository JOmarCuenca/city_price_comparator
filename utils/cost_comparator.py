import statistics
from loguru import logger
from models.city_cost import CityCostData, CostComparison

COST_TAGS = [
    "Menú del día en zona cara de la ciudad",
    "Menú completo en comida rápida",
    "Pechuga de pollo (500 gr)",
    "Leche entera (1 litro)",
    "Huevos grandes (12)",
    "Tomates (1 kg)",
    "Queso nacional (500 gr)",
    "Manzanas (1 kg)",
    "Patatas (1 kg)",
    "Cerveza nacional (0.5 l)",
    "Vino tinto de buena calidad (1 botella)",
    "Coca-cola (2 litros)",
    "Pan para dos personas",
    "Alquiler piso 85 m2 (zona cara)",
    "Alquiler piso 85 m2 (zona normal)",
    "Gastos luz, agua, electricidad para 2 personas (piso 85m2)",
    "Alquiler estudio 45 m2 (zona cara)",
    "Alquiler estudio 45 m2 (zona normal)",
    "Gastos luz, agua, electricidad para 1 persona (estudio 45m2)",
    "Internet 8 mbps (1 mes)",
    "TV pantalla plana 40 pulgadas",
    "Microondas 800/900 watt",
    "Detergente líquido (3 l)",
    "Precio por hora de limpieza doméstica",
    "Par de vaqueros (Levis 501 o similar)",
    "Vestido de señora de verano",
    "Par de zapatillas de deporte",
    "Par de zapatos de cuero caballero",
    "Volkswagen Golf 1.4 TSI 150 CV (o similar, nuevo)",
    "Gasolina (1 litro)",
    "Abono mensual transporte público",
    "Trayecto en taxi 8 km (día de diario, tarifa básica)",
    "Medicina para el resfriado (6 días)",
    "Caja de antibióticos 12 dosis",
    "Visita corta a médico privado (15 minutos)",
    "Caja de 32 tampones",
    "Desodorante roll-on (50ml)",
    "Champú 2-en-1 (400 ml)",
    "Rollos de papel higiénico (4)",
    "Tubo de pasta de dientes",
    "Corte de pelo básico (zona cara)",
    "Cena normal para dos en restaurante de barrio",
    "Entradas para cine (2, sesión normal)",
    "Entradas para teatro (2, mejores asientos)",
    "Cena para dos en restaurante italiano (zona cara, incluyendo entrantes, plato principal, vino y postre)",
    "Cocktail, copa o trago en club o disco (zona cara)",
    "Capuccino (zona cara)",
    "Cerveza medio litro en bar de barrio",
    "iPad Wi-Fi 128GB",
    "1 min. de llamadas con tarifa prepago",
    "Abono mensual a gimnasio (zona cara)",
    "Paquete de cigarrillos Marlboro",
]


@logger.catch(reraise=True)
def compare_cost(city_cost_1: CityCostData, city_cost_2: CityCostData) -> list[CostComparison]:
    amount_rate = input(
        f"Enter how much 1 {city_cost_1.currency} is in {city_cost_2.currency}: ")
    amount_rate = float(amount_rate)

    logger.info("Setting amount rate to {}", amount_rate)

    assert len(city_cost_1.costs) == len(
        city_cost_2.costs), "The number of costs must be the same"

    result = []

    for name, (cost1, cost2) in zip(COST_TAGS, zip(city_cost_1.costs, city_cost_2.costs)):
        result.append(
            CostComparison(name, amount_rate, cost1, cost2)
        )

    return result


def generate_cost_comparison_strings(compared_costs: list[CostComparison]) -> list[str]:
    cost_names = ["Cost Name"]
    base_amounts = ["Base Amount"]
    compared_amounts = ["Compared Amount"]
    percentage_differences = ["Percentage Difference"]

    for cost in compared_costs:
        cost_names.append(cost.cost_name)
        base_amounts.append(f"$ {cost.base_cost.cost:.2f}")
        compared_amounts.append(f"$ {cost.localized_compared_cost:.2f}")
        percentage_differences.append(cost.percentage_comparison)

    name_pad = max([len(name) for name in cost_names])
    base_pad = max([len(amount) for amount in base_amounts])
    compared_pad = max([len(amount) for amount in compared_amounts])
    percentage_pad = max([len(amount) for amount in percentage_differences])

    strings = []

    for name, base, compared, percentage in zip(cost_names, base_amounts, compared_amounts, percentage_differences):
        row_string = f"{name:<{name_pad}} | {base:<{base_pad}} | {compared:<{compared_pad}} | {percentage:<{percentage_pad}}"
        strings.append(row_string)
        strings.append("-" * len(row_string))

    EMPTY_CHAR = ""
    country_avg_differential_percentage = f"{statistics.mean([cost.comparison for cost in compared_costs]):.5f}%"
    strings.append(
        f"{EMPTY_CHAR:<{name_pad}} | {EMPTY_CHAR:<{base_pad}} | {EMPTY_CHAR:<{compared_pad}} | {country_avg_differential_percentage:<{percentage_pad}}")

    return strings


def print_cost_comparison(compared_costs: list[CostComparison]):
    print('\n'.join(generate_cost_comparison_strings(compared_costs)))
