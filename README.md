# Simplon Toolbox – Projet 1 MLOP

![CI Status](https://github.com/nicolastchenio/simplon_projet1_mlop/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-0%25-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 1. Présentation

Ce projet constitue la "Toolbox" de référence du cursus **Développeur IA** chez Simplon.  
Il sert de template pour tous les futurs projets, incluant :

- Code Python structuré et modulaire
- Tests unitaires avec **pytest**
- Documentation automatique avec **Sphinx + Furo**
- Linting avec **Ruff**
- Conteneurisation via **Docker**

---

## 2. Structure du projet

```plaintext
.
├── app/                    
│   ├── modules/           
│   │   ├── __init__.py
│   │   └── mon_module.py
│   ├── main.py            
│   └── moncsv.csv         
├── tests/                 
│   └── test_math_csv.py   
├── docs/                      
├── pyproject.toml         
├── uv.lock                    
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE

```

## 3. Guide d'installation

Cloner le dépôt :

```
git clone https://github.com/nicolastchenio/simplon_projet1_mlop.git
cd simplon_projet1_mlop
```

Installer les dépendances via uv :

```
uv sync
```

Lancer l'application :

```
uv run python app/main.py
```

Exécuter les tests :

```
uv run pytest
```

## 4. Contributeurs

Nicolas T.

[Autres membres de l'équipe]

## 5. Code de conduite

Merci de respecter les règles suivantes :

- Respect et courtoisie entre tous les contributeurs
- Aucun partage de données sensibles
- Suivi du guide de style Python (PEP8 / Ruff)


## 6. Contributing

Pour contribuer :

- Fork le projet
- Créer une branche : feat/ma-nouvelle-fonctionnalite
- Ajouter les tests et la documentation
- Ouvrir une Pull Request


## 7. Licence

Ce projet est sous licence MIT.

<!-- ceci est un commentaire pourb tetster le workflow -->