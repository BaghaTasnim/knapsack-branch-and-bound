
class KnapsackInstance:
    """Classe représentant une instance du problème du sac-à-dos"""
    
    def __init__(self, capacity, weights, values):
        """
        Initialise une instance du problème
        
        Args:
            capacity (int): Capacité maximale du conteneur
            weights (list): Liste des poids des articles
            values (list): Liste des valeurs des articles
        """
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.n = len(weights)
        
    def __str__(self):
        return f"Sac-à-dos: capacité={self.capacity}, n={self.n} articles"


def read_instance(filename):
    """
    Lit une instance depuis un fichier
    
    Format du fichier:
    - Ligne 1: Capacité W
    - Ligne 2: Nombre d'articles n
    - Lignes suivantes: poids valeur (une paire par ligne)
    
    Args:
        filename (str): Chemin du fichier
        
    Returns:
        KnapsackInstance: Instance du problème
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        # Lecture de la capacité
        capacity = int(lines[0].strip())
        
        # Lecture du nombre d'articles
        n = int(lines[1].strip())
        
        # Lecture des poids et valeurs
        weights = []
        values = []
        
        for i in range(2, 2 + n):
            parts = lines[i].strip().split()
            weights.append(int(parts[0]))
            values.append(int(parts[1]))
            
        return KnapsackInstance(capacity, weights, values)
        
    except FileNotFoundError:
        print(f"Erreur: Le fichier {filename} n'existe pas")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return None


def create_test_instance(filename, capacity, items):
    """
    Crée un fichier d'instance de test
    
    Args:
        filename (str): Nom du fichier à créer
        capacity (int): Capacité du sac
        items (list): Liste de tuples (poids, valeur)
    """
    with open(filename, 'w') as f:
        f.write(f"{capacity}\n")
        f.write(f"{len(items)}\n")
        for weight, value in items:
            f.write(f"{weight} {value}\n")
    print(f"Instance de test créée: {filename}")