"""
Programme principal pour résoudre le problème du sac-à-dos avec Branch-and-Bound
"""

import os
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt

from data_reader import read_instance
from branch_and_bound import BranchAndBound
from greedy_algorithms import greedy_integer


def run_single_instance(filename, use_sorting=True):
    """
    Résout une instance unique
    
    Args:
        filename (str): Chemin du fichier d'instance
        use_sorting (bool): Utiliser le tri par ratio
        
    Returns:
        dict: Résultats
    """
    print(f"\n{'='*70}")
    print(f"Traitement de l'instance: {filename}")
    print(f"{'='*70}")
    
    # Lecture de l'instance
    instance = read_instance(filename)
    if instance is None:
        return None
    
    print(f"Capacité: {instance.capacity} kg")
    print(f"Nombre d'articles: {instance.n}")
    
    # Résolution avec Branch-and-Bound
    bb = BranchAndBound(instance.weights, instance.values, instance.capacity, use_sorting)
    result = bb.solve()
    
    # Affichage de la solution
    bb.print_solution()
    
    return result


def compare_with_without_sorting(filename):
    """
    Compare l'efficacité avec et sans tri préalable
    
    Args:
        filename (str): Chemin du fichier d'instance
    """
    print(f"\n{'='*70}")
    print(f"COMPARAISON AVEC/SANS TRI - {filename}")
    print(f"{'='*70}")
    
    instance = read_instance(filename)
    if instance is None:
        return
    
    # Avec tri
    print("\n1. Avec tri par ratio v/w décroissant:")
    bb_sorted = BranchAndBound(instance.weights, instance.values, instance.capacity, use_sorting=True)
    result_sorted = bb_sorted.solve()
    
    # Sans tri
    print("\n2. Sans tri:")
    bb_unsorted = BranchAndBound(instance.weights, instance.values, instance.capacity, use_sorting=False)
    result_unsorted = bb_unsorted.solve()
    
    # Tableau comparatif
    comparison_data = [
        ["Avec tri", result_sorted['value'], result_sorted['nodes_explored'], 
         result_sorted['nodes_pruned'], f"{result_sorted['execution_time']:.4f}"],
        ["Sans tri", result_unsorted['value'], result_unsorted['nodes_explored'], 
         result_unsorted['nodes_pruned'], f"{result_unsorted['execution_time']:.4f}"]
    ]
    
    headers = ["Méthode", "Valeur", "Nœuds explorés", "Nœuds élagués", "Temps (s)"]
    print("\n" + tabulate(comparison_data, headers=headers, tablefmt="grid"))
    
    # Calcul du gain
    if result_unsorted['nodes_explored'] > 0:
        reduction = (1 - result_sorted['nodes_explored'] / result_unsorted['nodes_explored']) * 100
        print(f"\nRéduction du nombre de nœuds explorés: {reduction:.2f}%")


def run_all_instances(instances_dir="instances"):
    """
    Exécute tous les tests sur toutes les instances disponibles
    
    Args:
        instances_dir (str): Répertoire contenant les instances
    """
    if not os.path.exists(instances_dir):
        print(f"Erreur: Le répertoire {instances_dir} n'existe pas")
        return
    
    # Liste des fichiers d'instances
    instance_files = [f for f in os.listdir(instances_dir) if f.endswith('.txt')]
    
    if not instance_files:
        print(f"Aucune instance trouvée dans {instances_dir}")
        return
    
    print(f"\n{'='*70}")
    print(f"EXÉCUTION DE TOUTES LES INSTANCES")
    print(f"{'='*70}")
    print(f"Nombre d'instances trouvées: {len(instance_files)}")
    
    results = []
    
    for filename in sorted(instance_files):
        filepath = os.path.join(instances_dir, filename)
        result = run_single_instance(filepath)
        
        if result:
            results.append({
                'instance': filename,
                'value': result['value'],
                'nodes_explored': result['nodes_explored'],
                'nodes_pruned': result['nodes_pruned'],
                'time': result['execution_time']
            })
    
    # Tableau récapitulatif
    if results:
        print(f"\n{'='*70}")
        print(f"TABLEAU RÉCAPITULATIF")
        print(f"{'='*70}")
        
        table_data = [
            [r['instance'], r['value'], r['nodes_explored'], 
             r['nodes_pruned'], f"{r['time']:.4f}"]
            for r in results
        ]
        
        headers = ["Instance", "Valeur optimale", "Nœuds explorés", "Nœuds élagués", "Temps (s)"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Génération de graphiques
        generate_charts(results)


def generate_charts(results):
    """
    Génère des graphiques à partir des résultats
    
    Args:
        results (list): Liste des résultats
    """
    if not results:
        return
    
    instances = [r['instance'] for r in results]
    nodes_explored = [r['nodes_explored'] for r in results]
    times = [r['time'] for r in results]
    
    # Graphique 1: Nœuds explorés
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.bar(range(len(instances)), nodes_explored, color='steelblue')
    plt.xlabel('Instances')
    plt.ylabel('Nombre de nœuds explorés')
    plt.title('Nombre de nœuds explorés par instance')
    plt.xticks(range(len(instances)), instances, rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Graphique 2: Temps d'exécution
    plt.subplot(1, 2, 2)
    plt.bar(range(len(instances)), times, color='coral')
    plt.xlabel('Instances')
    plt.ylabel('Temps d\'exécution (s)')
    plt.title('Temps d\'exécution par instance')
    plt.xticks(range(len(instances)), instances, rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Sauvegarder le graphique
    if not os.path.exists('results'):
        os.makedirs('results')
    plt.savefig('results/resultats_graphiques.png', dpi=300, bbox_inches='tight')
    print("\nGraphiques sauvegardés dans: results/resultats_graphiques.png")
    plt.show()


def interactive_mode():
    """Mode interactif pour tester différentes configurations"""
    print("\n" + "="*70)
    print("MODE INTERACTIF - Résolution du problème du sac-à-dos")
    print("="*70)
    
    while True:
        print("\nOptions:")
        print("1. Résoudre une instance spécifique")
        print("2. Comparer avec/sans tri")
        print("3. Exécuter toutes les instances")
        print("4. Quitter")
        
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == '1':
            filename = input("Chemin du fichier d'instance: ").strip()
            if os.path.exists(filename):
                run_single_instance(filename)
            else:
                print(f"Erreur: Le fichier {filename} n'existe pas")
        
        elif choice == '2':
            filename = input("Chemin du fichier d'instance: ").strip()
            if os.path.exists(filename):
                compare_with_without_sorting(filename)
            else:
                print(f"Erreur: Le fichier {filename} n'existe pas")
        
        elif choice == '3':
            instances_dir = input("Répertoire des instances [instances]: ").strip() or "instances"
            run_all_instances(instances_dir)
        
        elif choice == '4':
            print("\nAu revoir!")
            break
        
        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Mode ligne de commande
        if sys.argv[1] == "--all":
            run_all_instances()
        elif sys.argv[1] == "--compare":
            if len(sys.argv) > 2:
                compare_with_without_sorting(sys.argv[2])
            else:
                print("Usage: python main.py --compare <fichier_instance>")
        else:
            run_single_instance(sys.argv[1])
    else:
        # Mode interactif
        interactive_mode()