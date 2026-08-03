"""
Periodização AB-AB-FullBody (5 dias)

Programa completo de hipertrofia com 5 treinos semanais:
  - Treino 1: Pernas (Posterior de Coxa e Glúteos)
  - Treino 2: Costas e Peito
  - Treino 3: Bíceps, Tríceps e Deltoides
  - Treino 4: Pernas (Quadríceps)
  - Treino 5: Full Upper (Membros Superiores)
"""

from typing import Any, Dict

PROGRAM: Dict[str, Any] = {
    "name": "Periodização AB-AB-FullBody",
    "workouts": [
        # ──────────────────────────────────────────────────────────
        # TREINO 1: PERNAS 2/2 (POSTERIOR DE COXA E GLÚTEOS)
        # ──────────────────────────────────────────────────────────
        {
            "title": "Treino 1 — Pernas (Posterior + Glúteos)",
            "notes": "Foco em isquiotibiais e glúteos. Controle excêntrico em todos os movimentos.",
            "exercises": [
                {
                    "name": "Deadlift (Barbell)",
                    "rest_seconds": 180,
                    "notes": "Quadril projetado para trás, coluna neutra e barra próxima ao corpo.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 100},
                        {"type": "normal", "reps": 8, "weight_kg": 100},
                        {"type": "normal", "reps": 8, "weight_kg": 100},
                        {"type": "normal", "reps": 8, "weight_kg": 100},
                    ]
                },
                {
                    "name": "Lying Leg Curl (Machine)",
                    "rest_seconds": 90,
                    "notes": "Controle total da fase excêntrica e pausa isométrica de 1s na flexão máxima.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 40},
                        {"type": "normal", "reps": 10, "weight_kg": 40},
                        {"type": "normal", "reps": 10, "weight_kg": 40},
                        {"type": "normal", "reps": 10, "weight_kg": 40},
                    ]
                },
                {
                    "name": "Good Morning (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Manter postura da coluna e foco no padrão de dobradiça do quadril.",
                    "sets": [
                        {"type": "normal", "reps": 6, "weight_kg": 40},
                        {"type": "normal", "reps": 6, "weight_kg": 40},
                        {"type": "normal", "reps": 6, "weight_kg": 40},
                    ]
                },
                {
                    "name": "Seated Leg Curl (Machine)",
                    "rest_seconds": 90,
                    "notes": "Manter o quadril bem posicionado no banco para evitar compensações.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 35},
                        {"type": "normal", "reps": 10, "weight_kg": 35},
                        {"type": "normal", "reps": 10, "weight_kg": 35},
                    ]
                },
                {
                    "name": "Hip Thrust (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Pausa isométrica de 2s no topo, mantendo retroversão pélvica.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 90},
                        {"type": "normal", "reps": 8, "weight_kg": 90},
                        {"type": "normal", "reps": 8, "weight_kg": 90},
                        {"type": "normal", "reps": 8, "weight_kg": 90},
                    ]
                },
                {
                    "name": "Single Leg Romanian Deadlift (Dumbbell)",
                    "rest_seconds": 90,
                    "notes": "Amplitude máxima segura com controle total de rotação do tronco e quadril. Cada lado.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 16},
                        {"type": "normal", "reps": 10, "weight_kg": 16},
                        {"type": "normal", "reps": 10, "weight_kg": 16},
                    ]
                },
                {
                    "name": "Hip Thrust (Machine)",
                    "rest_seconds": 90,
                    "notes": "Foco no esmagamento no topo do movimento.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                    ]
                },
                {
                    "name": "Calf Press (Machine)",
                    "rest_seconds": 60,
                    "notes": "Amplitude completa de alongamento e contração no Leg Press horizontal.",
                    "sets": [
                        {"type": "normal", "reps": 15, "weight_kg": 120},
                        {"type": "normal", "reps": 15, "weight_kg": 120},
                        {"type": "normal", "reps": 15, "weight_kg": 120},
                        {"type": "normal", "reps": 15, "weight_kg": 120},
                    ]
                },
            ]
        },

        # ──────────────────────────────────────────────────────────
        # TREINO 2: COSTAS E PEITO
        # ──────────────────────────────────────────────────────────
        {
            "title": "Treino 2 — Costas e Peito",
            "notes": "Costas com foco em largura e espessura. Peito com foco em massa e peitoral superior.",
            "exercises": [
                {
                    "name": "Pull Up (Assisted)",
                    "rest_seconds": 120,
                    "notes": "Iniciar o movimento pela depressão escapular antes de flexionar os cotovelos.",
                    "sets": [
                        {"type": "normal", "reps": 10},
                        {"type": "normal", "reps": 10},
                        {"type": "normal", "reps": 10},
                        {"type": "normal", "reps": 10},
                    ]
                },
                {
                    "name": "Bent Over Row (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Tronco estável, coluna neutra e puxar a barra na linha do umbigo. Pegada pronada.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                    ]
                },
                {
                    "name": "Lat Pulldown (Cable)",
                    "rest_seconds": 90,
                    "notes": "Evitar balanço corporal e manter cotovelos próximos ao tronco.",
                    "sets": [
                        {"type": "normal", "reps": 15, "weight_kg": 45},
                        {"type": "normal", "reps": 15, "weight_kg": 45},
                        {"type": "normal", "reps": 15, "weight_kg": 45},
                    ]
                },
                {
                    "name": "Seated Cable Row - V Grip (Cable)",
                    "rest_seconds": 90,
                    "notes": "Retração escapular completa no final do movimento. Pegada neutra fechada.",
                    "sets": [
                        {"type": "normal", "reps": 15, "weight_kg": 50},
                        {"type": "normal", "reps": 15, "weight_kg": 50},
                        {"type": "normal", "reps": 15, "weight_kg": 50},
                    ]
                },
                {
                    "name": "Bench Press (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Escápulas retraídas, trajetória controlada e pés firmes no solo.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 60},
                        {"type": "normal", "reps": 8, "weight_kg": 60},
                        {"type": "normal", "reps": 8, "weight_kg": 60},
                        {"type": "normal", "reps": 8, "weight_kg": 60},
                    ]
                },
                {
                    "name": "Incline Bench Press (Dumbbell)",
                    "rest_seconds": 90,
                    "notes": "Banco ajustado entre 25° e 30°, com controle total da descida.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 22},
                        {"type": "normal", "reps": 10, "weight_kg": 22},
                        {"type": "normal", "reps": 10, "weight_kg": 22},
                        {"type": "normal", "reps": 10, "weight_kg": 22},
                    ]
                },
                {
                    "name": "Incline Chest Fly (Dumbbell)",
                    "rest_seconds": 90,
                    "notes": "Fase excêntrica lenta e amplitude máxima segura. Foco em alongamento sob tensão.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 14},
                        {"type": "normal", "reps": 10, "weight_kg": 14},
                        {"type": "normal", "reps": 10, "weight_kg": 14},
                    ]
                },
                {
                    "name": "Chest Fly (Machine)",
                    "rest_seconds": 60,
                    "notes": "Manter tensão contínua e cruzar levemente as mãos no final (Peck Deck).",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 40},
                        {"type": "normal", "reps": 12, "weight_kg": 40},
                        {"type": "normal", "reps": 12, "weight_kg": 40},
                    ]
                },
            ]
        },

        # ──────────────────────────────────────────────────────────
        # TREINO 3: BÍCEPS, TRÍCEPS E DELTOIDES
        # ──────────────────────────────────────────────────────────
        {
            "title": "Treino 3 — Bíceps, Tríceps e Deltoides",
            "notes": "Ombros primeiro, depois braços. Foco em massa e isolamento.",
            "exercises": [
                {
                    "name": "Seated Shoulder Press (Machine)",
                    "rest_seconds": 90,
                    "notes": "Escápulas estabilizadas, core ativo e barra descendo até a linha do queixo.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 30},
                        {"type": "normal", "reps": 10, "weight_kg": 30},
                        {"type": "normal", "reps": 10, "weight_kg": 30},
                    ]
                },
                {
                    "name": "Shoulder Press (Dumbbell)",
                    "rest_seconds": 120,
                    "notes": "Sentado no banco inclinado. Movimento convergente e controle total da fase excêntrica.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 18},
                        {"type": "normal", "reps": 8, "weight_kg": 18},
                        {"type": "normal", "reps": 8, "weight_kg": 18},
                        {"type": "normal", "reps": 8, "weight_kg": 18},
                    ]
                },
                {
                    "name": "Lateral Raise (Dumbbell)",
                    "rest_seconds": 60,
                    "notes": "Leve inclinação do tronco, subida até a linha do ombro e descida controlada.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 10},
                        {"type": "normal", "reps": 10, "weight_kg": 10},
                        {"type": "normal", "reps": 10, "weight_kg": 10},
                        {"type": "normal", "reps": 10, "weight_kg": 10},
                    ]
                },
                {
                    "name": "Bicep Curl (Barbell)",
                    "rest_seconds": 90,
                    "notes": "Cotovelos fixos ao lado do corpo, totalmente sem balanço. Barra reta.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 25},
                        {"type": "normal", "reps": 8, "weight_kg": 25},
                        {"type": "normal", "reps": 8, "weight_kg": 25},
                        {"type": "normal", "reps": 8, "weight_kg": 25},
                    ]
                },
                {
                    "name": "Seated Incline Curl (Dumbbell)",
                    "rest_seconds": 90,
                    "notes": "Sentado no banco inclinado. Supinação completa e pausa de 1s no topo. Alternado.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 10},
                        {"type": "normal", "reps": 12, "weight_kg": 10},
                        {"type": "normal", "reps": 12, "weight_kg": 10},
                        {"type": "normal", "reps": 12, "weight_kg": 10},
                    ]
                },
                {
                    "name": "Concentration Curl",
                    "rest_seconds": 60,
                    "notes": "Evitar extensão total agressiva do cotovelo na descida. Cada lado.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 10},
                        {"type": "normal", "reps": 10, "weight_kg": 10},
                        {"type": "normal", "reps": 10, "weight_kg": 10},
                        {"type": "normal", "reps": 10, "weight_kg": 10},
                    ]
                },
                {
                    "name": "Bench Press - Close Grip (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Pegada média e cotovelos passando bem próximos ao tronco.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                    ]
                },
                {
                    "name": "Skullcrusher (Barbell)",
                    "rest_seconds": 90,
                    "notes": "Cotovelos bem estáveis e descida controlada até a linha da testa. Barra W.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 25},
                        {"type": "normal", "reps": 10, "weight_kg": 25},
                        {"type": "normal", "reps": 10, "weight_kg": 25},
                        {"type": "normal", "reps": 10, "weight_kg": 25},
                    ]
                },
                {
                    "name": "Triceps Rope Pushdown",
                    "rest_seconds": 60,
                    "notes": "Abertura da corda no final do movimento com contração máxima. 20 reps — estresse metabólico.",
                    "sets": [
                        {"type": "normal", "reps": 20, "weight_kg": 20},
                        {"type": "normal", "reps": 20, "weight_kg": 20},
                        {"type": "normal", "reps": 20, "weight_kg": 20},
                    ]
                },
            ]
        },

        # ──────────────────────────────────────────────────────────
        # TREINO 4: PERNAS 1/2 (FOCO: QUADRÍCEPS)
        # ──────────────────────────────────────────────────────────
        {
            "title": "Treino 4 — Pernas (Quadríceps)",
            "notes": "Foco em quadríceps com sobrecarga progressiva e volume.",
            "exercises": [
                {
                    "name": "Front Squat",
                    "rest_seconds": 180,
                    "notes": "Manter tronco ereto e cotovelos elevados durante o movimento.",
                    "sets": [
                        {"type": "normal", "reps": 6, "weight_kg": 60},
                        {"type": "normal", "reps": 6, "weight_kg": 60},
                        {"type": "normal", "reps": 6, "weight_kg": 60},
                        {"type": "normal", "reps": 6, "weight_kg": 60},
                    ]
                },
                {
                    "name": "Hack Squat (Machine)",
                    "rest_seconds": 120,
                    "notes": "Pés levemente à frente. Amplitude máxima sem perder contato lombar com o encosto.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 80},
                        {"type": "normal", "reps": 10, "weight_kg": 80},
                        {"type": "normal", "reps": 10, "weight_kg": 80},
                        {"type": "normal", "reps": 10, "weight_kg": 80},
                    ]
                },
                {
                    "name": "Leg Press (Machine)",
                    "rest_seconds": 120,
                    "notes": "Pés em posição média na plataforma. Descida controlada até ~90° de flexão de joelho.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 150},
                        {"type": "normal", "reps": 12, "weight_kg": 150},
                        {"type": "normal", "reps": 12, "weight_kg": 150},
                        {"type": "normal", "reps": 12, "weight_kg": 150},
                    ]
                },
                {
                    "name": "Bulgarian Split Squat (Dumbbell)",
                    "rest_seconds": 90,
                    "notes": "Tronco levemente ereto para maior ênfase no quadríceps. Cada lado.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 16},
                        {"type": "normal", "reps": 8, "weight_kg": 16},
                        {"type": "normal", "reps": 8, "weight_kg": 16},
                    ]
                },
                {
                    "name": "Leg Extension (Machine)",
                    "rest_seconds": 90,
                    "notes": "Pausa isométrica de 2s na extensão completa do movimento.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 50},
                        {"type": "normal", "reps": 10, "weight_kg": 50},
                        {"type": "normal", "reps": 10, "weight_kg": 50},
                        {"type": "normal", "reps": 10, "weight_kg": 50},
                    ]
                },
                {
                    "name": "Hip Thrust (Machine)",
                    "rest_seconds": 90,
                    "notes": "Contração máxima no topo e descida controlada.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                    ]
                },
                {
                    "name": "Calf Press (Machine)",
                    "rest_seconds": 60,
                    "notes": "Amplitude completa, focando no alongamento máximo na descida.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 60},
                        {"type": "normal", "reps": 12, "weight_kg": 60},
                        {"type": "normal", "reps": 12, "weight_kg": 60},
                        {"type": "normal", "reps": 12, "weight_kg": 60},
                    ]
                },
            ]
        },

        # ──────────────────────────────────────────────────────────
        # TREINO 5: FULL UPPER (MEMBROS SUPERIORES)
        # ──────────────────────────────────────────────────────────
        {
            "title": "Treino 5 — Full Upper (MMSS)",
            "notes": "Treino completo de membros superiores: costas, peito, ombros e braços.",
            "exercises": [
                {
                    "name": "Lat Pulldown (Cable)",
                    "rest_seconds": 120,
                    "notes": "Controle da descida e escápulas estáveis.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                        {"type": "normal", "reps": 8, "weight_kg": 50},
                    ]
                },
                {
                    "name": "Seated Cable Row - V Grip (Cable)",
                    "rest_seconds": 120,
                    "notes": "Pegada fechada neutra, focando na retração das escápulas.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 55},
                        {"type": "normal", "reps": 8, "weight_kg": 55},
                        {"type": "normal", "reps": 8, "weight_kg": 55},
                        {"type": "normal", "reps": 8, "weight_kg": 55},
                    ]
                },
                {
                    "name": "Bench Press (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Escápulas retraídas, peito estufado e pés firmes no solo.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 60},
                        {"type": "normal", "reps": 8, "weight_kg": 60},
                        {"type": "normal", "reps": 8, "weight_kg": 60},
                        {"type": "normal", "reps": 8, "weight_kg": 60},
                    ]
                },
                {
                    "name": "Incline Bench Press (Dumbbell)",
                    "rest_seconds": 90,
                    "notes": "Alternando os braços, mantendo estabilidade do tronco e core ativo.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 22},
                        {"type": "normal", "reps": 8, "weight_kg": 22},
                        {"type": "normal", "reps": 8, "weight_kg": 22},
                        {"type": "normal", "reps": 8, "weight_kg": 22},
                    ]
                },
                {
                    "name": "Seated Shoulder Press (Machine)",
                    "rest_seconds": 90,
                    "notes": "Evitar travar totalmente o cotovelo no topo para manter tensão constante.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 30},
                        {"type": "normal", "reps": 8, "weight_kg": 30},
                        {"type": "normal", "reps": 8, "weight_kg": 30},
                        {"type": "normal", "reps": 8, "weight_kg": 30},
                    ]
                },
                {
                    "name": "Bicep Curl (Barbell)",
                    "rest_seconds": 60,
                    "notes": "Barra W. Cotovelos fixos sem balanço do tronco.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 25},
                        {"type": "normal", "reps": 10, "weight_kg": 25},
                        {"type": "normal", "reps": 10, "weight_kg": 25},
                        {"type": "normal", "reps": 10, "weight_kg": 25},
                    ]
                },
                {
                    "name": "Hammer Curl (Dumbbell)",
                    "rest_seconds": 60,
                    "notes": "Alternando os braços com supinação controlada.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 12},
                        {"type": "normal", "reps": 10, "weight_kg": 12},
                        {"type": "normal", "reps": 10, "weight_kg": 12},
                        {"type": "normal", "reps": 10, "weight_kg": 12},
                    ]
                },
                {
                    "name": "Triceps Extension (Dumbbell)",
                    "rest_seconds": 60,
                    "notes": "Cotovelos bem fechados, apontados para cima. Controlar bem a amplitude na descida.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 16},
                        {"type": "normal", "reps": 10, "weight_kg": 16},
                        {"type": "normal", "reps": 10, "weight_kg": 16},
                        {"type": "normal", "reps": 10, "weight_kg": 16},
                    ]
                },
            ]
        },
    ]
}
