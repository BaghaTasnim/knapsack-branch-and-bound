"""
Script pour créer des instances de test
"""

import os

def create_instances():
    """Crée plusieurs instances de test"""
    
    if not os.path.exists('instances'):
        os.makedirs('instances')
    
    # Instance 1: Petite instance (exemple du cours)
    instance1 = {
        'capacity': 50,
        'items': [
            (10, 60),   # Article 1: poids=10, valeur=60
            (20, 100),  # Article 2: poids=20, valeur=100
            (30, 120),  # Article 3: poids=30, valeur=120
        ]
    }
    
    # Instance 2: Instance moyenne
    instance2 = {
        'capacity': 165,
        'items': [
            (23, 92),
            (31, 57),
            (29, 49),
            (44, 68),
            (53, 60),
            (38, 43),
            (63, 67),
            (85, 84),
            (89, 87),
            (82, 72),
        ]
    }
    
    # Instance 3: Instance plus grande
    instance3 = {
        'capacity': 750,
        'items': [
            (70, 135),
            (73, 139),
            (77, 149),
            (80, 150),
            (82, 156),
            (87, 163),
            (90, 173),
            (94, 184),
            (98, 192),
            (106, 201),
            (110, 210),
            (113, 214),
            (115, 221),
            (118, 229),
            (120, 240),
        ]
    }
    
    # Instance 4: Instance difficile
    instance4 = {
        'capacity': 400,
        'items': [
            (41, 442),
            (50, 525),
            (49, 511),
            (59, 593),
            (55, 546),
            (57, 564),
            (60, 617),
            (45, 463),
            (48, 494),
            (52, 533),
            (43, 442),
            (47, 485),
            (46, 474),
            (44, 455),
            (51, 523),
            (53, 543),
            (56, 574),
            (58, 592),
            (54, 554),
            (42, 432),
        ]
    }
    
    instances = [
        ('instances/instance_1.txt', instance1),
        ('instances/instance_2.txt', instance2),
        ('instances/instance_3.txt', instance3),
        ('instances/instance_4.txt', instance4),
    ]
    
    for filename, instance in instances:
        with open(filename, 'w') as f:
            f.write(f"{instance['capacity']}\n")
            f.write(f"{len(instance['items'])}\n")
            for weight, value in instance['items']:
                f.write(f"{weight} {value}\n")
        print(f"Instance créée: {filename}")
    
    print(f"\n{len(instances)} instances de test créées avec succès!")


if __name__ == "__main__":
    create_instances()