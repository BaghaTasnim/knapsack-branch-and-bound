"""
Script pour créer des instances plus grandes pour mieux voir l'impact du tri
"""

import random
import os

def create_large_instances():
    """Crée des instances plus grandes pour les tests"""
    
    if not os.path.exists('instances'):
        os.makedirs('instances')
    
    # Instance 5: 25 articles (pour voir clairement l'impact du tri)
    random.seed(42)  # Pour la reproductibilité
    n5 = 25
    capacity5 = 500
    items5 = [(random.randint(20, 80), random.randint(50, 200)) for _ in range(n5)]
    
    with open('instances/instance_5.txt', 'w') as f:
        f.write(f"{capacity5}\n")
        f.write(f"{n5}\n")
        for w, v in items5:
            f.write(f"{w} {v}\n")
    print("Instance 5 créée: 25 articles")
    
    # Instance 6: 30 articles (instance difficile)
    random.seed(123)
    n6 = 30
    capacity6 = 600
    items6 = [(random.randint(15, 70), random.randint(40, 180)) for _ in range(n6)]
    
    with open('instances/instance_6.txt', 'w') as f:
        f.write(f"{capacity6}\n")
        f.write(f"{n6}\n")
        for w, v in items6:
            f.write(f"{w} {v}\n")
    print("Instance 6 créée: 30 articles")
    
    # Instance 7: Instance avec ratios similaires (pire cas)
    n7 = 22
    capacity7 = 450
    items7 = [(random.randint(40, 50), random.randint(80, 100)) for _ in range(n7)]
    
    with open('instances/instance_7.txt', 'w') as f:
        f.write(f"{capacity7}\n")
        f.write(f"{n7}\n")
        for w, v in items7:
            f.write(f"{w} {v}\n")
    print("Instance 7 créée: 22 articles (ratios similaires)")
    
    print("\n✅ 3 nouvelles instances créées!")
    print("Utilisez instance_5, instance_6 ou instance_7 pour la comparaison avec/sans tri")

if __name__ == "__main__":
    create_large_instances()