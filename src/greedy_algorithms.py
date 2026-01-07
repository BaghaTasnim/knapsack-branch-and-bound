"""
Module contenant les algorithmes gloutons pour le problème du sac-à-dos
"""

def sort_items_by_ratio(weights, values):
    """
    Trie les articles par ordre décroissant du ratio valeur/poids
    
    Args:
        weights (list): Liste des poids
        values (list): Liste des valeurs
        
    Returns:
        tuple: (indices triés, ratios triés)
    """
    n = len(weights)
    ratios = [(values[i] / weights[i], i) for i in range(n)]
    ratios.sort(reverse=True)
    
    sorted_indices = [idx for _, idx in ratios]
    sorted_ratios = [ratio for ratio, _ in ratios]
    
    return sorted_indices, sorted_ratios


def greedy_fractional(weights, values, capacity, sorted_indices=None):
    """
    Algorithme glouton fractionnaire (relaxation linéaire)
    Permet de prendre des fractions d'articles
    
    Args:
        weights (list): Liste des poids
        values (list): Liste des valeurs
        capacity (int): Capacité du sac
        sorted_indices (list): Indices triés (optionnel)
        
    Returns:
        tuple: (valeur totale, solution fractionnaire)
    """
    n = len(weights)
    
    # Si pas d'indices triés fournis, on trie
    if sorted_indices is None:
        sorted_indices, _ = sort_items_by_ratio(weights, values)
    
    # Solution fractionnaire
    solution = [0.0] * n
    total_value = 0.0
    remaining_capacity = capacity
    
    for idx in sorted_indices:
        if weights[idx] <= remaining_capacity:
            # Prendre l'article entier
            solution[idx] = 1.0
            total_value += values[idx]
            remaining_capacity -= weights[idx]
        else:
            # Prendre une fraction de l'article
            fraction = remaining_capacity / weights[idx]
            solution[idx] = fraction
            total_value += values[idx] * fraction
            break
    
    return total_value, solution


def greedy_integer(weights, values, capacity, sorted_indices=None):
    """
    Algorithme glouton entier (heuristique)
    Ne prend que des articles entiers
    
    Args:
        weights (list): Liste des poids
        values (list): Liste des valeurs
        capacity (int): Capacité du sac
        sorted_indices (list): Indices triés (optionnel)
        
    Returns:
        tuple: (valeur totale, solution binaire)
    """
    n = len(weights)
    
    # Si pas d'indices triés fournis, on trie
    if sorted_indices is None:
        sorted_indices, _ = sort_items_by_ratio(weights, values)
    
    # Solution binaire
    solution = [0] * n
    total_value = 0
    remaining_capacity = capacity
    
    for idx in sorted_indices:
        if weights[idx] <= remaining_capacity:
            # Prendre l'article entier
            solution[idx] = 1
            total_value += values[idx]
            remaining_capacity -= weights[idx]
    
    return total_value, solution


def compute_upper_bound(weights, values, capacity, level, current_weight, current_value, sorted_indices):
    """
    Calcule la borne supérieure pour un nœud donné
    en utilisant la relaxation fractionnaire sur les articles restants
    
    Args:
        weights (list): Liste des poids
        values (list): Liste des valeurs
        capacity (int): Capacité totale
        level (int): Niveau actuel (articles 0..level-1 déjà traités)
        current_weight (int): Poids courant
        current_value (int): Valeur courante
        sorted_indices (list): Indices triés
        
    Returns:
        float: Borne supérieure
    """
    if current_weight >= capacity:
        return 0
    
    remaining_capacity = capacity - current_weight
    upper_bound = current_value
    
    # Appliquer l'algorithme glouton fractionnaire sur les articles restants
    for i in range(level, len(weights)):
        idx = sorted_indices[i]
        
        if weights[idx] <= remaining_capacity:
            # Prendre l'article entier
            remaining_capacity -= weights[idx]
            upper_bound += values[idx]
        else:
            # Prendre une fraction
            fraction = remaining_capacity / weights[idx]
            upper_bound += values[idx] * fraction
            break
    
    return upper_bound