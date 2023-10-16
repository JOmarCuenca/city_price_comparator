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
    assert city_cost_1.currency == city_cost_2.currency, "The currency must be the same"

    logger.debug(f"Comparing costs using {city_cost_1.currency} as currency")

    assert len(city_cost_1.costs) == len(
        city_cost_2.costs), "The number of costs must be the same"

    result = []

    for name, (cost1, cost2) in zip(COST_TAGS, zip(city_cost_1.costs, city_cost_2.costs)):
        result.append(
            CostComparison(name, cost1, cost2)
        )

    return result
