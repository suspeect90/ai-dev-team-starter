# Démarrer et utiliser l'équipe

L'équipe se réutilise dans le dépôt de chaque application. Vous décrivez votre idée et vos contraintes ; Codex coordonne les spécialistes utiles. Les neuf rôles ne doivent pas tous démarrer pour chaque demande.

## 1. Créer votre nouveau projet

1. Sur [le dépôt modèle](https://github.com/suspeect90/ai-dev-team-starter), choisir **Use this template → Create a new repository**, puis nommer votre application. Le dépôt source est déjà marqué Template Repository au 11 octobre 2026. La branche par défaut suffit pour démarrer.
2. Cloner ce nouveau dépôt dans le dossier où vous souhaitez travailler, par exemple `C:\MesProjets\mon-application`. Les fichiers cachés `.codex` et `.agents` doivent aussi être présents.
3. Dans Codex, ouvrir ou ajouter ce dossier comme projet local et le définir comme dossier principal. Démarrer une discussion depuis ce projet. Examiner les instructions et configurations, puis utiliser les contrôles de confiance du client si nécessaire.

Le dossier principal doit être la racine contenant `AGENTS.md`, `.codex/`, `.agents/` et `docs/`. Joindre un dossier ou indiquer son chemin dans une discussion existante peut permettre de lire ses fichiers, mais ne prouve pas la découverte automatique de ses agents et skills. Une ancienne discussion garde son répertoire de travail enregistré ; vérifier celui de la nouvelle discussion. Voir la [documentation officielle des projets](https://learn.chatgpt.com/docs/projects?surface=app).

Si vous utilisez le CLI, lancer `codex` depuis cette racine, ou utiliser `codex --cd "C:\MesProjets\mon-application"`. Vérifier sa version avec `codex --version` ; ne pas remplacer les fichiers par un ancien format sans consulter la [référence des sous-agents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## 2. Vérifier le démarrage une première fois

Vous pouvez copier ce message dans la nouvelle discussion :

> Vérifie le démarrage de notre équipe dans ce projet. Indique le répertoire de travail, la racine Git, la branche et les changements locaux. Lis AGENTS.md et docs/PROJECT_BRIEF.md. Vérifie les rôles et skills réellement disponibles, en distinguant le catalogue du client des fichiers lus explicitement. Exécute le validateur et les tests du modèle. Fais ensuite le test natif isolé décrit dans docs/SMOKE_TEST.md si les outils le permettent, puis nettoie uniquement ses artefacts temporaires. Signale ce qui a réussi et ce qui reste non vérifié.

Les commandes du modèle, à lancer depuis sa racine avec Python 3.11 ou ultérieur et Git disponibles, sont :

```text
python scripts/validate.py
python -m unittest discover -s tests -v
```

Le contrôle des noms de fichiers sensibles examine les chemins suivis dans l'index Git. Il ne lit pas les secrets locaux ignorés et ne remplace pas une recherche de secrets dans le contenu ou l'historique.

Le dépôt contient neuf rôles dans `.codex/agents/` et sept skills dans `.agents/skills/`. Leur présence et les tests structurels ne prouvent pas leur chargement natif. Le [test isolé](SMOKE_TEST.md) vérifie une véritable chaîne de délégation ; il ne certifie pas tous les rôles ni une application future. Ce contrôle est utile au premier démarrage et après un changement important du client ou des contrats.

Si le client ne permet pas de choisir un rôle TOML par nom, le parent peut lire explicitement ses instructions et lancer un véritable sous-agent natif avec ce contrat. Il doit déclarer ce mode, sans prétendre que le TOML ou son sandbox a été appliqué automatiquement. Si la délégation native manque, il doit signaler cette limite.

## 3. Décrire votre idée

Une fois le démarrage vérifié, votre message peut rester simple :

> Voici mon idée d'application. Analyse le besoin, propose l'architecture, prépare le plan de développement et mobilise les spécialistes nécessaires.

Ajoutez juste votre idée, les fonctionnalités prioritaires et vos contraintes. Exemple de complément :

> Mon idée : [description]. Mes technologies choisies : [stack et versions, ou « à proposer »]. Mes contraintes : [budget, délai, plateformes]. Travaille phase par phase et arrête-toi au bilan de chaque phase.

Renseigner le [brief du projet](PROJECT_BRIEF.md), ou demander à Codex de le compléter avec vos réponses. Les informations inconnues restent des questions ouvertes. Les profils dans `templates/stacks/` sont facultatifs : Laravel, Next.js ou une autre technologie ne sont jamais imposés. Python sert aux contrôles du modèle ; il ne détermine pas la stack de l'application.

Le parent agit comme Tech Lead : il analyse, propose le plan, attribue les fichiers, lance les spécialistes selon les dépendances, intègre leurs résultats et vérifie les changements. Les tâches indépendantes peuvent avancer en parallèle dans la limite réelle du client. Le rôle `tech_lead` délégué reste facultatif. Les tests de l'application s'ajoutent aux contrôles du modèle.

## Reprise après interruption

> Reprends cette mission. Vérifie le dépôt, la branche et les changements locaux, les agents encore actifs, la propriété des fichiers et le dernier résultat vérifié. Résume ce qui est terminé, les blocages et le prochain jalon, puis poursuis les tâches déjà autorisées sans démarrer de doublon.

Revenir de préférence dans la discussion du projet. Avant une interruption prévue, demander :

> Prépare un point de reprise : objectif, phase en cours, dépôt et branche, changements locaux, agents actifs et fichiers attribués, dernier commit vérifié, tests réellement exécutés, décisions prises et prochaine tâche. Conserve ce point dans le suivi du projet sans secret.

Si une nouvelle discussion est nécessaire, y fournir ce point et vérifier sa racine. Les agents ne sont pas garantis actifs après un redémarrage : vérifier leurs états avant de relancer une tâche. La reprise ne doit pas écraser les changements locaux.

## Changement de projet

1. Terminer ou suspendre explicitement les tâches du projet courant et conserver un point de reprise.
2. Ouvrir le nouveau projet et démarrer sa propre discussion depuis sa racine ; conserver l'ancienne pour reprendre le premier projet.
3. Vérifier son démarrage, puis décrire sa nouvelle idée. Chaque projet possède son brief, ses instructions et ses décisions ; revérifier les outils et permissions disponibles.

Message pour le nouveau projet :

> Nous travaillons sur [nom du nouveau projet]. Vérifie la racine et la branche, puis lis ses instructions et son brief. Utilise uniquement le contexte pertinent de ce projet. Voici son objectif : [description].

## Mise à jour

Les projets créés depuis le modèle sont des copies indépendantes : les mises à jour ne leur sont pas transmises automatiquement. Suivre le [guide de maintenance](MAINTENANCE.md).

> Compare notre version de l'équipe à la version choisie du modèle. Identifie les changements utiles des agents et skills et nos personnalisations. Prépare leur intégration sur une branche de travail en préservant nos instructions, notre brief et nos fichiers d'application. Vérifie le diff, exécute la validation et les tests, puis présente le résultat et les incompatibilités éventuelles.

Comparer les fichiers ciblés ; ne pas fusionner aveuglément tout l'historique du modèle. Conserver les métadonnées de chaque `SKILL.md` et tester les procédures modifiées. Après un changement significatif de contrat, relancer le test natif isolé. Codex détecte normalement les changements de skills ; redémarrer si la liste n'est pas actualisée. Quand plusieurs skills portent le même nom, sélectionner celui situé dans ce dépôt. Voir la [référence officielle des skills](https://learn.chatgpt.com/docs/build-skills).

## Autorisations et preuves

Le guide prépare et vérifie le travail ; aucune mise en production ni suppression de données réelles n'est autorisée implicitement. Demander l'autorisation humaine au moment de l'action concernée. Distinguer systématiquement « planifié », « exécuté », « réussi », « échoué » et « non vérifié ».
