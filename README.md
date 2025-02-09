
```python

#barter_data.json
[
    {"name": "A", "offers": ["design", "water"], "wants": ["marketing"], "rating": 1},
    {"name": "B", "offers": ["marketing"], "wants": ["programming"], "rating": 4},
    {"name": "C", "offers": ["programming"], "wants": ["design", "water"], "rating": 1},
    {"name": "D", "offers": ["copywriting"], "wants": ["marketing", "design"], "rating": 1},
    {"name": "E", "offers": ["water"], "wants": ["copywriting"], "rating": 5},
    {"name": "F", "offers": ["бензин"], "wants": ["зерно"], "rating": 5},
    {"name": "G", "offers": ["зерно"], "wants": ["мясо"], "rating": 5},
    {"name": "H", "offers": ["мясо"], "wants": ["бензин"], "rating": 5}
]


```

```bash
python3 barter_graph.py barter_data.json
```


```
🏆 Цепочка 1 (Средневзвешенный рейтинг: 5.00):
  F → получает (зерно) → G
  G → получает (мясо) → H
  H → получает (бензин) → F
------------------------------
🏆 Цепочка 2 (Средневзвешенный рейтинг: 3.20):
  B → получает (programming) → C
  C → получает (water) → E
  E → получает (copywriting) → D
  D → получает (marketing) → B
------------------------------
🏆 Цепочка 3 (Средневзвешенный рейтинг: 2.83):
  A → получает (marketing) → B
  B → получает (programming) → C
  C → получает (water) → E
  E → получает (copywriting) → D
  D → получает (design) → A
------------------------------
🏆 Цепочка 4 (Средневзвешенный рейтинг: 2.50):
  A → получает (marketing) → B
  B → получает (programming) → C
  C → получает (design) → A
```