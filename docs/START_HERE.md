# Démarrer et utiliser l'équipe

## Nouveau projet

1. Sur GitHub, utiliser **Use this template → Create a new repository**. Le dépôt source est déjà marqué Template Repository au 11 octobre 2026.
2. Cloner votre nouveau dépôt et ouvrir sa racine dans Codex. Examiner les instructions/configurations puis accorder la confiance au projet selon les contrôles du client ; ne pas désactiver le sandbox.
3. Vérifier `codex --version` si vous utilisez le CLI. Les formats de référence sont ceux de la [documentation officielle](https://learn.chatgpt.com/docs/agent-configuration/subagents). Une version ancienne peut demander une mise à jour ; ne pas remplacer les fichiers par un ancien format sans vérifier.
4. Renseigner `docs/PROJECT_BRIEF.md` avec le besoin, les contraintes, les technologies choisies et les environnements disponibles. Les profils dans `templates/stacks/` sont facultatifs ; l'équipe accepte d'autres stacks.
5. Avec Python 3.11 ou ultérieur, exécuter :

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

6. Vérifier les agents/skills effectivement proposés par le client, puis réaliser le test isolé de `docs/SMOKE_TEST.md`. Une validation de fichiers ne prouve pas le chargement natif.

## Votre premier message

> Voici mon idée d'application : [décrivez-la]. Analyse le besoin, propose l'architecture, prépare le plan de développement et mobilise les spécialistes nécessaires avec les outils natifs de Codex. Lis AGENTS.md et docs/PROJECT_BRIEF.md. Respecte mes contraintes technologiques et les décisions déjà autorisées. Commence par l'analyse et le plan ; présente les décisions importantes avant leur mise en œuvre. Vérifie les résultats par des tests réellement exécutés et signale les capacités indisponibles.

Le parent agit comme Tech Lead. Il choisit les spécialistes utiles et organise les tâches indépendantes en parallèle, dans la limite du runtime. Le rôle `tech_lead` délégué reste facultatif.

Si le client ne permet pas de choisir un rôle TOML par nom, le parent peut lire explicitement son `developer_instructions` et lancer un véritable sous-agent natif avec ce contrat. Il doit déclarer cette limite et ne pas prétendre que le fichier a été chargé automatiquement.

## Reprise après interruption

> Reprends cette mission. Vérifie le dépôt, la branche et les changements locaux, les agents encore actifs, la propriété des fichiers et le dernier résultat vérifié. Résume ce qui est terminé, les blocages et le prochain jalon, puis poursuis les tâches déjà autorisées sans démarrer de doublon.

Conserver dans le chat ou le suivi du projet le plan, les identifiants d'agents, les chemins attribués, le commit vérifié, les commandes et décisions. Les conversations/templates ne garantissent pas que les agents restent actifs après un redémarrage.

## Changement de projet

Terminer ou suspendre explicitement les tâches du projet courant, conserver leur état, puis ouvrir la racine du nouveau projet dans un chat adapté. Recharger son brief, ses instructions et son contexte ; ne pas réutiliser ses secrets ou ses hypothèses dans un autre projet. Revérifier les outils et permissions disponibles.

## Mise à jour

Suivre `docs/MAINTENANCE.md`. Comparer les nouvelles versions et intégrer par une branche/PR les changements utiles. Préserver les personnalisations. Relancer validation, tests et test natif après un changement significatif de contrat. Codex détecte normalement les changements de skills ; redémarrer le client si la liste n'est pas actualisée.

## Autorisations et preuves

Le guide prépare et vérifie le travail ; aucune mise en production ni suppression de données réelles n'est autorisée implicitement. Demander l'autorisation humaine au moment de l'action concernée. Distinguer systématiquement « planifié », « exécuté », « réussi », « échoué » et « non vérifié ».
