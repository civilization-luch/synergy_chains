import json
from collections import defaultdict

class BarterGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.offers = defaultdict(set)
        self.wants = defaultdict(set)
        self.ratings = {}  

    def add_participant(self, name, offers, wants, rating):
        """Добавляет участника в базу."""
        self.offers[name] = set(offers) if isinstance(offers, list) else {offers}
        self.wants[name] = set(wants) if isinstance(wants, list) else {wants}
        self.ratings[name] = rating  

    def build_graph(self):
        """Создаёт связи после загрузки всех участников."""
        for name, wants in self.wants.items():
            for want in wants:
                for owner, owner_offers in self.offers.items():
                    if want in owner_offers and owner != name:
                        self.graph[name].append((owner, want, self.ratings[owner]))  

    def find_best_cycles(self):
        """Находит циклы и сортирует их по средневзвешенному рейтингу."""
        cycles = []
        visited = set()
        nodes = list(self.graph.keys())

        def dfs(node, start, path, trade_path, ratings):
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            ratings.append(self.ratings[node])

            for neighbor, traded_item, neighbor_rating in self.graph[node]:
                if neighbor == start and len(path) > 2:
                    trade_path.append((node, traded_item, neighbor))
                    ratings.append(self.ratings[neighbor])
                    cycle = self.normalize_cycle(trade_path)
                    avg_weighted_rating = sum(ratings) / len(ratings)  
                    cycles.append((cycle, avg_weighted_rating))
                    trade_path.pop()
                    ratings.pop()
                elif neighbor not in path:
                    trade_path.append((node, traded_item, neighbor))
                    dfs(neighbor, start, path, trade_path, ratings)
                    trade_path.pop()

            path.pop()
            ratings.pop()
            visited.remove(node)

        for node in nodes:
            dfs(node, node, [], [], [])

        # Убираем дубликаты циклов и оставляем с наибольшим средневзвешенным рейтингом
        unique_cycles = {}
        for cycle, rating in cycles:
            key = tuple(sorted([step[0] for step in cycle]))  
            if key not in unique_cycles or unique_cycles[key][1] < rating:
                unique_cycles[key] = (cycle, rating)

        return sorted(unique_cycles.values(), key=lambda x: x[1], reverse=True)

    def normalize_cycle(self, cycle):
        """Приводит цикл к стандартному виду, чтобы избежать дубликатов."""
        names = [step[0] for step in cycle]
        min_index = names.index(min(names))  
        return cycle[min_index:] + cycle[:min_index]  

    def load_from_json(self, json_file):
        """Загружает данные и строит связи."""
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for participant in data:
            self.add_participant(
                participant["name"], participant["offers"], participant["wants"], participant["rating"]
            )

        self.build_graph()



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load barter data from a JSON file.")
    parser.add_argument("json_file", type=str, help="Path to the JSON file containing barter data.")
    args = parser.parse_args()
    


    # === Использование ===
    json_file = args.json_file

    barter = BarterGraph()
    barter.load_from_json(json_file)

    # Найдём циклы с максимальным средневзвешенным рейтингом
    cycles = barter.find_best_cycles()

    # Выводим лучшие цепочки
    for i, (cycle, rating) in enumerate(cycles, 1):
        print(f"🏆 Цепочка {i} (Средневзвешенный рейтинг: {rating:.2f}):")
        for sender, item, receiver in cycle:
            print(f"  {sender} → получает ({item}) → {receiver}")
        print("-" * 30)
