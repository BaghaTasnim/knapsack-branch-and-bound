
import time
from greedy_algorithms import sort_items_by_ratio, greedy_integer, compute_upper_bound


class Node:
    """Classe représentant un nœud dans l'arbre Branch-and-Bound"""
    
    def __init__(self, level, value, weight, bound, solution):
        """
        Initialise un nœud
        
        Args:
            level (int): Niveau dans l'arbre (nombre de décisions prises)
            value (int): Valeur courante
            weight (int): Poids courant
            bound (float): Borne supérieure
            solution (list): Solution partielle (0, 1, ou -1 pour non décidé)
        """
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = bound
        self.solution = solution.copy()
    
    def __str__(self):
        return f"Node(level={self.level}, value={self.value}, weight={self.weight}, bound={self.bound:.2f})"


class BranchAndBound:
    """Classe implémentant l'algorithme Branch-and-Bound"""
    
    def __init__(self, weights, values, capacity, use_sorting=True):
        """
        Initialise l'algorithme Branch-and-Bound
        
        Args:
            weights (list): Liste des poids
            values (list): Liste des valeurs
            capacity (int): Capacité du sac
            use_sorting (bool): Si True, trie les articles par ratio décroissant
        """
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.n = len(weights)
        self.use_sorting = use_sorting
        
        # Statistiques
        self.nodes_explored = 0
        self.nodes_pruned = 0
        self.execution_time = 0
        
        # Solution
        self.best_value = 0
        self.best_solution = [0] * self.n
        
        # Tri des articles
        if use_sorting:
            self.sorted_indices, _ = sort_items_by_ratio(weights, values)
        else:
            self.sorted_indices = list(range(self.n))
    
    def solve(self):
        """
        Résout le problème du sac-à-dos avec Branch-and-Bound
        
        Returns:
            dict: Dictionnaire contenant la solution et les statistiques
        """
        start_time = time.time()
        
        # Initialisation avec l'heuristique gloutonne (borne inférieure)
        lb_value, lb_solution = greedy_integer(
            self.weights, self.values, self.capacity, self.sorted_indices
        )
        self.best_value = lb_value
        self.best_solution = lb_solution.copy()
        
        # Calcul de la borne supérieure initiale
        ub = compute_upper_bound(
            self.weights, self.values, self.capacity, 
            0, 0, 0, self.sorted_indices
        )
        
        # Nœud racine
        root = Node(0, 0, 0, ub, [-1] * self.n)
        
        # Exploration en profondeur d'abord (DFS)
        self._branch_and_bound_dfs(root)
        
        self.execution_time = time.time() - start_time
        
        return {
            'value': self.best_value,
            'solution': self.best_solution,
            'nodes_explored': self.nodes_explored,
            'nodes_pruned': self.nodes_pruned,
            'execution_time': self.execution_time
        }
    
    def _branch_and_bound_dfs(self, node):
        """
        Exploration en profondeur d'abord de l'arbre Branch-and-Bound
        
        Args:
            node (Node): Nœud courant
        """
        self.nodes_explored += 1
        
        # Cas terminal : tous les articles ont été considérés
        if node.level == self.n:
            if node.value > self.best_value:
                self.best_value = node.value
                self.best_solution = node.solution.copy()
            return
        
        # Élagage par borne
        if node.bound <= self.best_value:
            self.nodes_pruned += 1
            return
        
        # Article courant (dans l'ordre trié)
        idx = self.sorted_indices[node.level]
        
        # Branche gauche : prendre l'article (x_idx = 1)
        if node.weight + self.weights[idx] <= self.capacity:
            # Solution mise à jour
            left_solution = node.solution.copy()
            left_solution[idx] = 1
            
            # Nouveau poids et valeur
            left_weight = node.weight + self.weights[idx]
            left_value = node.value + self.values[idx]
            
            # Borne supérieure
            left_bound = compute_upper_bound(
                self.weights, self.values, self.capacity,
                node.level + 1, left_weight, left_value, self.sorted_indices
            )
            
            # Créer le nœud fils gauche
            left_node = Node(node.level + 1, left_value, left_weight, left_bound, left_solution)
            
            # Mise à jour de la meilleure solution si on a une solution entière
            if left_value > self.best_value:
                self.best_value = left_value
                self.best_solution = left_solution.copy()
            
            # Explorer récursivement
            self._branch_and_bound_dfs(left_node)
        
        # Branche droite : ne pas prendre l'article (x_idx = 0)
        right_solution = node.solution.copy()
        right_solution[idx] = 0
        
        # Borne supérieure
        right_bound = compute_upper_bound(
            self.weights, self.values, self.capacity,
            node.level + 1, node.weight, node.value, self.sorted_indices
        )
        
        # Vérifier si la branche droite est prometteuse
        if right_bound > self.best_value:
            # Créer le nœud fils droit
            right_node = Node(node.level + 1, node.value, node.weight, right_bound, right_solution)
            
            # Explorer récursivement
            self._branch_and_bound_dfs(right_node)
        else:
            self.nodes_pruned += 1
    
    def get_statistics(self):
        """
        Retourne les statistiques d'exécution
        
        Returns:
            dict: Statistiques
        """
        return {
            'best_value': self.best_value,
            'nodes_explored': self.nodes_explored,
            'nodes_pruned': self.nodes_pruned,
            'execution_time': self.execution_time
        }
    
    def print_solution(self):
        """Affiche la solution détaillée"""
        print(f"\n{'='*60}")
        print(f"SOLUTION OPTIMALE")
        print(f"{'='*60}")
        print(f"Valeur totale: {self.best_value}")
        
        total_weight = sum(self.best_solution[i] * self.weights[i] for i in range(self.n))
        print(f"Poids total: {total_weight} / {self.capacity}")
        
        print(f"\nArticles sélectionnés:")
        for i in range(self.n):
            if self.best_solution[i] == 1:
                print(f"  Article {i}: poids={self.weights[i]}, valeur={self.values[i]}")
        
        print(f"\nStatistiques:")
        print(f"  Nœuds explorés: {self.nodes_explored}")
        print(f"  Nœuds élagués: {self.nodes_pruned}")
        print(f"  Temps d'exécution: {self.execution_time:.4f} secondes")
        print(f"{'='*60}\n")