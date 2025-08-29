from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import math
import random

# Coordenadas base do AlphaVille São Luís (aproximadas)
BASE_COORDS = {"lat": -2.5307, "lng": -44.2075}

@dataclass
class Setor:
    id: str
    nome: str
    coordenadas: Dict[str, float]
    cor: str

@dataclass
class PontoReferencia:
    id: str
    nome: str
    tipo: str
    coordenadas: Dict[str, float]
    descricao: str

@dataclass
class Lote:
    numero: str
    setor: str
    coordenadas: Dict[str, float]
    endereco: str
    ocupado: bool
    tipo: str  # 'residencial' | 'comercial' | 'area_comum'

# Setores (réplica do TS)
setores: List[Setor] = [
    Setor(id="residencial-a", nome="Setor Residencial A",
          coordenadas={"lat": BASE_COORDS["lat"] + 0.001, "lng": BASE_COORDS["lng"] + 0.001},
          cor="#10b981"),
    Setor(id="residencial-b", nome="Setor Residencial B",
          coordenadas={"lat": BASE_COORDS["lat"] + 0.002, "lng": BASE_COORDS["lng"] + 0.002},
          cor="#3b82f6"),
    Setor(id="residencial-c", nome="Setor Residencial C",
          coordenadas={"lat": BASE_COORDS["lat"] + 0.003, "lng": BASE_COORDS["lng"] + 0.001},
          cor="#8b5cf6"),
    Setor(id="comercial", nome="Setor Comercial",
          coordenadas={"lat": BASE_COORDS["lat"] + 0.0005, "lng": BASE_COORDS["lng"] + 0.003},
          cor="#f59e0b"),
    Setor(id="lazer", nome="Área de Lazer",
          coordenadas={"lat": BASE_COORDS["lat"] + 0.0015, "lng": BASE_COORDS["lng"] + 0.0025},
          cor="#ef4444"),
]

pontos_referencia: List[PontoReferencia] = [
    PontoReferencia(id="portaria-principal", nome="Portaria Principal", tipo="entrada",
                    coordenadas=BASE_COORDS, descricao="Entrada principal do condomínio"),
    PontoReferencia(id="portaria-secundaria", nome="Portaria Secundária", tipo="entrada",
                    coordenadas={"lat": BASE_COORDS["lat"] + 0.004, "lng": BASE_COORDS["lng"] + 0.003},
                    descricao="Entrada secundária"),
    PontoReferencia(id="centro-comercial", nome="Centro Comercial", tipo="comercio",
                    coordenadas={"lat": BASE_COORDS["lat"] + 0.0005, "lng": BASE_COORDS["lng"] + 0.003},
                    descricao="Área comercial com lojas e serviços"),
    PontoReferencia(id="clube", nome="Clube", tipo="lazer",
                    coordenadas={"lat": BASE_COORDS["lat"] + 0.0015, "lng": BASE_COORDS["lng"] + 0.0025},
                    descricao="Área de lazer com piscina e quadras"),
    PontoReferencia(id="escola", nome="Escola", tipo="educacao",
                    coordenadas={"lat": BASE_COORDS["lat"] + 0.002, "lng": BASE_COORDS["lng"] + 0.0015},
                    descricao="Escola do condomínio"),
]

def _grid_offsets(i: int, step: float, ncols: int, row_step: float) -> Tuple[float, float]:
    # gera deslocamentos em grade em torno do centro do setor
    col = (i % ncols) - (ncols // 2)
    row = (i // ncols) - (ncols // 2)
    return col * step, row * row_step

def gerar_lotes() -> List[Lote]:
    lotes: List[Lote] = []

    # Setor A: A1..A100 (10x10)
    for i in range(1, 101):
        off_lat = ((i % 10) - 5) * 0.0002
        off_lng = ((i // 10) - 5) * 0.0002
        lotes.append(Lote(
            numero=f"A{i}", setor="Setor Residencial A",
            coordenadas={"lat": setores[0].coordenadas["lat"] + off_lat,
                         "lng": setores[0].coordenadas["lng"] + off_lng},
            endereco=f"Lote A{i}, Setor Residencial A",
            ocupado=(random.random() > 0.3),
            tipo="residencial"
        ))

    # Setor B: B1..B100
    for i in range(1, 101):
        off_lat = ((i % 10) - 5) * 0.0002
        off_lng = ((i // 10) - 5) * 0.0002
        lotes.append(Lote(
            numero=f"B{i}", setor="Setor Residencial B",
            coordenadas={"lat": setores[1].coordenadas["lat"] + off_lat,
                         "lng": setores[1].coordenadas["lng"] + off_lng},
            endereco=f"Lote B{i}, Setor Residencial B",
            ocupado=(random.random() > 0.3),
            tipo="residencial"
        ))

    # Setor C: C1..C100
    for i in range(1, 101):
        off_lat = ((i % 10) - 5) * 0.0002
        off_lng = ((i // 10) - 5) * 0.0002
        lotes.append(Lote(
            numero=f"C{i}", setor="Setor Residencial C",
            coordenadas={"lat": setores[2].coordenadas["lat"] + off_lat,
                         "lng": setores[2].coordenadas["lng"] + off_lng},
            endereco=f"Lote C{i}, Setor Residencial C",
            ocupado=(random.random() > 0.3),
            tipo="residencial"
        ))

    # Comercial: L1..L50 (5x10 grid)
    for i in range(1, 51):
        off_lat = ((i % 5) - 2.5) * 0.0001
        off_lng = ((i // 5) - 5) * 0.0001
        lotes.append(Lote(
            numero=f"L{i}", setor="Setor Comercial",
            coordenadas={"lat": setores[3].coordenadas["lat"] + off_lat,
                         "lng": setores[3].coordenadas["lng"] + off_lng},
            endereco=f"Loja L{i}, Setor Comercial",
            ocupado=(random.random() > 0.2),
            tipo="comercial"
        ))

    # Lazer: R1..R20
    for i in range(1, 21):
        off_lat = ((i % 4) - 2) * 0.0001
        off_lng = ((i // 4) - 2.5) * 0.0001
        lotes.append(Lote(
            numero=f"R{i}", setor="Área de Lazer",
            coordenadas={"lat": setores[4].coordenadas["lat"] + off_lat,
                         "lng": setores[4].coordenadas["lng"] + off_lng},
            endereco=f"Área R{i}, Área de Lazer",
            ocupado=True,
            tipo="area_comum"
        ))

    return lotes

lotes: List[Lote] = gerar_lotes()

def buscar_lote(numero: str) -> Optional[Lote]:
    if not numero:
        return None
    num = numero.strip().upper()
    # busca exata
    for l in lotes:
        if l.numero.upper() == num:
            return l
    # busca parcial
    for l in lotes:
        if num in l.numero.upper():
            return l
    return None

def buscar_lotes_por_setor(setor_nome: str) -> List[Lote]:
    return [l for l in lotes if l.setor == setor_nome]

def haversine_m(coord1: Dict[str, float], coord2: Dict[str, float]) -> float:
    R = 6371.0  # km
    dlat = math.radians(coord2["lat"] - coord1["lat"])
    dlng = math.radians(coord2["lng"] - coord1["lng"])
    a = math.sin(dlat/2)**2 + math.cos(math.radians(coord1["lat"])) *         math.cos(math.radians(coord2["lat"])) * math.sin(dlng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000.0

def lotes_proximos(coord: Dict[str, float], raio_m: float = 100.0) -> List[Lote]:
    return sorted([l for l in lotes if haversine_m(coord, l.coordenadas) <= raio_m],
                  key=lambda l: haversine_m(coord, l.coordenadas))

# Rotas simplificadas: escolhe portaria mais próxima do ponto inicial e traça linha até o lote.
def rota_simples(origem: Dict[str, float], destino: Dict[str, float]):
    # escolhe a portaria mais próxima da origem para efeito de visualização
    entradas = [p for p in pontos_referencia if p.tipo == "entrada"]
    if not entradas:
        waypoints = []
    else:
        entradas_ordenadas = sorted(entradas, key=lambda e: haversine_m(origem, e.coordenadas))
        waypoints = [entradas_ordenadas[0].coordenadas]
    caminho = [origem] + waypoints + [destino]
    dist_total = sum(haversine_m(caminho[i], caminho[i+1]) for i in range(len(caminho)-1))
    return caminho, dist_total