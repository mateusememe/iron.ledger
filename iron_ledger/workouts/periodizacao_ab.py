from typing import Any, Dict

PROGRAM: Dict[str, Any] = {
    "name": "Periodização A/B",
    "workouts": [
        {
            "title": "Treino A - Superior",
            "notes": "Foco em peito, costas e ombros",
            "exercises": [
                {
                    "name": "Bench Press (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Controlar a descida. Foco no peitoral.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 60},
                        {"type": "normal", "reps": 10, "weight_kg": 60},
                        {"type": "normal", "reps": 10, "weight_kg": 60},
                        {"type": "normal", "reps": 10, "weight_kg": 60},
                    ]
                },
                {
                    "name": "Bent Over Row (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Costas retas, puxar em direção ao umbigo.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 50},
                        {"type": "normal", "reps": 10, "weight_kg": 50},
                        {"type": "normal", "reps": 10, "weight_kg": 50},
                        {"type": "normal", "reps": 10, "weight_kg": 50},
                    ]
                },
                {
                    "name": "Overhead Press (Barbell)",
                    "rest_seconds": 90,
                    "notes": "Não curvar a lombar excessivamente.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 30},
                        {"type": "normal", "reps": 12, "weight_kg": 30},
                        {"type": "normal", "reps": 12, "weight_kg": 30},
                    ]
                },
                {
                    "name": "Lat Pulldown (Cable)",
                    "rest_seconds": 90,
                    "notes": "Foco na contração das dorsais.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 45},
                        {"type": "normal", "reps": 12, "weight_kg": 45},
                        {"type": "normal", "reps": 12, "weight_kg": 45},
                    ]
                },
                {
                    "name": "Lateral Raise (Dumbbell)",
                    "rest_seconds": 60,
                    "notes": "Movimento controlado, sem usar impulso.",
                    "sets": [
                        {"type": "normal", "reps": 15, "weight_kg": 10},
                        {"type": "normal", "reps": 15, "weight_kg": 10},
                        {"type": "normal", "reps": 15, "weight_kg": 10},
                    ]
                },
                {
                    "name": "Bicep Curl (Barbell)",
                    "rest_seconds": 60,
                    "notes": "Cotovelos fixos.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 25},
                        {"type": "normal", "reps": 12, "weight_kg": 25},
                        {"type": "normal", "reps": 12, "weight_kg": 25},
                    ]
                },
                {
                    "name": "Triceps Pushdown",
                    "rest_seconds": 60,
                    "notes": "Focar na extensão completa do tríceps.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 20},
                        {"type": "normal", "reps": 12, "weight_kg": 20},
                        {"type": "normal", "reps": 12, "weight_kg": 20},
                    ]
                }
            ]
        },
        {
            "title": "Treino B - Inferior",
            "notes": "Foco em pernas completas e core",
            "exercises": [
                {
                    "name": "Squat (Barbell)",
                    "rest_seconds": 180,
                    "notes": "Agachamento profundo, mantendo o peito alto.",
                    "sets": [
                        {"type": "normal", "reps": 8, "weight_kg": 80},
                        {"type": "normal", "reps": 8, "weight_kg": 80},
                        {"type": "normal", "reps": 8, "weight_kg": 80},
                        {"type": "normal", "reps": 8, "weight_kg": 80},
                    ]
                },
                {
                    "name": "Romanian Deadlift (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Foco no alongamento dos isquiotibiais.",
                    "sets": [
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                        {"type": "normal", "reps": 10, "weight_kg": 70},
                    ]
                },
                {
                    "name": "Leg Press (Machine)",
                    "rest_seconds": 120,
                    "notes": "Não travar os joelhos na extensão máxima.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 150},
                        {"type": "normal", "reps": 12, "weight_kg": 150},
                        {"type": "normal", "reps": 12, "weight_kg": 150},
                    ]
                },
                {
                    "name": "Lying Leg Curl (Machine)",
                    "rest_seconds": 90,
                    "notes": "Contrair bem no final do movimento.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 40},
                        {"type": "normal", "reps": 12, "weight_kg": 40},
                        {"type": "normal", "reps": 12, "weight_kg": 40},
                    ]
                },
                {
                    "name": "Leg Extension (Machine)",
                    "rest_seconds": 90,
                    "notes": "Pausa breve na contração máxima.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 50},
                        {"type": "normal", "reps": 12, "weight_kg": 50},
                        {"type": "normal", "reps": 12, "weight_kg": 50},
                    ]
                },
                {
                    "name": "Calf Raise (Machine)",
                    "rest_seconds": 60,
                    "notes": "Alongar bem na descida.",
                    "sets": [
                        {"type": "normal", "reps": 15, "weight_kg": 60},
                        {"type": "normal", "reps": 15, "weight_kg": 60},
                        {"type": "normal", "reps": 15, "weight_kg": 60},
                        {"type": "normal", "reps": 15, "weight_kg": 60},
                    ]
                },
                {
                    "name": "Hip Thrust (Barbell)",
                    "rest_seconds": 120,
                    "notes": "Contração forte dos glúteos.",
                    "sets": [
                        {"type": "normal", "reps": 12, "weight_kg": 90},
                        {"type": "normal", "reps": 12, "weight_kg": 90},
                        {"type": "normal", "reps": 12, "weight_kg": 90},
                    ]
                }
            ]
        }
    ]
}
