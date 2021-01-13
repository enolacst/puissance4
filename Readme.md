Le répertoire du projet est organisé en 2 sous-répertoires
Code: tous les codes qui seront développés sont dans cette partie
Fiches: toutes les fiches relatives au projet sont dans ce répertoire

Code est subdivisé en une partie principale (là où se font les
développements et là où sont lancés les tests)
tests: sous-répertoire contenant les codes de tests que je vous fournis
tools: sous-répertoire contenant des codes utiles pour le bon
       déroulement du projet


Les fichiers NE DOIVENT PAS être déplacés.

Exploration du répertoire Code:
> Le fichier connect4.py contient la classe Board qui permet de jouer
au puissance 4. La méthode win sera l'objet du travail du premier jalon
(voir fiche_jalon01.pdf)
> Le fichier main_tests.py permet de lancer l'ensemble des tests ou une partie
seulement.
Au lancement du fichier (run dans IDLE)
on vous demande de saisir le fichier sur lequel les tests doivent être effectués
on vous demande ensuite de répondre par une lettre
    Oui en utilisant au choix 0, o, O, y, Y
    toute autre lettre est considérée comme une réponse négative
si vous voulez passer *tous* les tests
  dans le cas d'une réponse négative on vous demandera si vous voulez passer
  les tests associés à une étape particulière (un jalon), pour chaque sous-test
  vous devrez dire si vous souhaitez que le test soit ou non effectué
> Sample.txt:
Un exemple de session utilisant le fichier connect4.py
> Tests_sample.txt
Un exemple de session utilisant le fichier main_tests.py

Exploration du répertoire tests:
> test_board: correspond aux tests de fonctionnalités du jeu hors les tests
  relatif à la méthode 'win'
> test_win: correspond aux tests relatifs à la fonction win, ce fichier n'est
pas terminé et sera modifié durant les jours à venir

Exploration du répertoire tools:
> ezCLI.py: une ancienne version du fichier fourni par C. Schlick pour le
module "Prog 2" du premier semestre de L3
> checkTools.py: fichier python contenant des petits outils pour faciliter la
mise en place de tests
> outils.py: contient pour le moment 2 utilitaires permettant de passer
de coordonnée en 2D à un index en 1D (c2p "coordinate to position") et de
passer d'un index en 1D à une coordonnée 2D (p2c "position to coordinate")

