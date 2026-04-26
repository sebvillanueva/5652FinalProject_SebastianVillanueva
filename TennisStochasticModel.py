import random


# ---------------------------
# Player Class
# ---------------------------
class Player:
    def __init__(self, name, p_serve, p_return):
        self.name = name
        self.p_serve = p_serve
        self.p_return = p_return


# ---------------------------
# Tennis Match Class
# ---------------------------
class TennisMatch:
    def __init__(self, playerA, playerB, best_of=3):
        self.A = playerA
        self.B = playerB
        self.best_of = best_of
        self.sets_to_win = best_of // 2 + 1

    # Symmetric point simulation
    def simulate_point(self, server):
        if server == self.A:
            # A serves, B returns
            p_A = (self.A.p_serve + (1 - self.B.p_return)) / 2
        else:
            # B serves, A returns
            p_A = ((1 - self.B.p_serve) + self.A.p_return) / 2

        return self.A if random.random() < p_A else self.B

    # Game simulation
    def simulate_game(self, server):
        score_A = 0
        score_B = 0

        while True:
            winner = self.simulate_point(server)

            if winner == self.A:
                score_A += 1
            else:
                score_B += 1

            if score_A >= 4 and score_A - score_B >= 2:
                return self.A
            if score_B >= 4 and score_B - score_A >= 2:
                return self.B

    # Tiebreak (alternating serve every 2 points)
    def simulate_tiebreak(self, starting_server):
        points_A = 0
        points_B = 0
        server = starting_server
        point_count = 0

        while True:
            winner = self.simulate_point(server)

            if winner == self.A:
                points_A += 1
            else:
                points_B += 1

            point_count += 1

            # Switch serve: first after 1 point, then every 2
            if point_count == 1 or point_count % 2 == 1:
                server = self.B if server == self.A else self.A

            if points_A >= 7 and points_A - points_B >= 2:
                return self.A
            if points_B >= 7 and points_B - points_A >= 2:
                return self.B

    # Set simulation 
    def simulate_set(self, starting_server):
        games_A = 0
        games_B = 0
        server = starting_server

        while True:
            winner = self.simulate_game(server)

            if winner == self.A:
                games_A += 1
            else:
                games_B += 1

            # Check win
            if games_A >= 6 and games_A - games_B >= 2:
                return self.A, (games_A, games_B), server

            if games_B >= 6 and games_B - games_A >= 2:
                return self.B, (games_A, games_B), server

            # Tiebreak
            if games_A == 6 and games_B == 6:
                tb_winner = self.simulate_tiebreak(server)
                if tb_winner == self.A:
                    return self.A, (7, 6), server
                else:
                    return self.B, (6, 7), server

            # Alternate serve
            server = self.B if server == self.A else self.A

    # Match with score tracking
    def simulate_match_with_score(self):
        sets_A = 0
        sets_B = 0
        set_scores = []

        # Only randomize ONCE
        server = random.choice([self.A, self.B])

        while sets_A < self.sets_to_win and sets_B < self.sets_to_win:
            winner, score, server = self.simulate_set(server)
            set_scores.append(score)

            if winner == self.A:
                sets_A += 1
            else:
                sets_B += 1

        match_winner = self.A if sets_A > sets_B else self.B
        return match_winner, set_scores

    # Monte Carlo
    def monte_carlo(self, n=10000):
        wins_A = 0

        for _ in range(n):
            winner, _ = self.simulate_match_with_score()
            if winner == self.A:
                wins_A += 1

        return wins_A / n

    def format_score(self, set_scores):
        return ", ".join([f"{a}-{b}" for a, b in set_scores])

def runSimulation(player1, player2, best_of = 3,number_of_simulations = 10000):
    match = TennisMatch(player1, player2, best_of=5)

    # Single match
    winner, scores = match.simulate_match_with_score()
    print(f"!!! {player1.name} vs. {player2.name} !!!")
    print(f"\nWinner: {winner.name}")
    print("Match Score:", match.format_score(scores))
    print("______________________")
    
    # Monte Carlo
    n = number_of_simulations
    pA = match.monte_carlo(n)

    print(f"After {n} simulations:")
    print(f"\n{player1.name} win probability: {pA:.4f}")
    print(f"{player2.name} win probability: {1 - pA:.4f}")
    print("___________________________________")
        
# ---------------------------
# Main Function
# ---------------------------
def main():
    CarlosAlcaraz = Player("Carlos Alcaraz", 0.67, 0.42)
    NovakDjokovic = Player("Novak Djokovic", 0.68, 0.42)
    BenShelton = Player("Ben Shelton", 0.68, 0.33)
    ReillyOpelka = Player("Reilly Opelka", 0.70, 0.28)
    AlexDeMinaur = Player("Alex De Minaur", 0.64, 0.40)
    
    runSimulation(CarlosAlcaraz, NovakDjokovic, 5)
    runSimulation(ReillyOpelka, AlexDeMinaur, 5)
    
    runSimulation(BenShelton, CarlosAlcaraz, 5)
    runSimulation(BenShelton, NovakDjokovic, 5)

if __name__ == "__main__":
    main()