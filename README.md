# soundsForThymio

Ce dépôt résumes les informations à connaître pour jouer des sons avec Thymio depuis une carte micro-SD, et propose 2 scripts pour aider à la conversion de fichier et/ou corriger certains fichiers wav mal formatés.

## Setup Thymio & Carte

### Instructions officielles
- Comment enregistrer un son avec le logiciel Audacity: https://www.thymio.org/fr/faq/comment-enregistrer-et-utiliser-un-effet-sonore-pour-thymio/
- Quelle carte micro SD utiliser: http://aseba.wikidot.com/fr:thymiomicrosd

### Vérifier sa carte SD

La première chose à faire est de vérifier la compatibilité et le bon fonctionnement de sa carte SD. La carte SD doit être formatée en **FAT32** et les fichiers `.wav` disposés à la racine de la carte en suivant la numérotation `P0, P1, P2, Px.wav`

Pour vérifier votre carte, copiez le fichier `sounds/P0.wav` sur votre carte SD et essayer de jouer le son. 
Vous devriez entendre "nihao", ce qui signifie "bonjour" en chinois. Ce son de référence est également disponible sur le [forum de thymio](http://aseba.wdfiles.com/local--files/fr:thymioapi/s0.wav)
Si vous n'entendez pas de son, n'essayez pas d'aller plus loin et essayer une autre carte SD.

### Format wav

Pour pouvoir être jouer par Thymio, un son doit avoir les caratéristiques suivantes:
* mono channel
* 8000Hz sample rate
* unsigned 8 bits PCM
* **aucune** méta-données en entête du fichier

## Conversion de sons

### Convertir un son dans le bon format pour Thymio

Bien que vous puissiez utiliser n'importe quel logiciel de conversion audio pour cette tâche, le script `soundsForThymio` permet de convertir un son (peu importe le format d'entrée) dans le format attendu par Thymio sans rien n'avoir à configurer. Il s'utilise en ligne de commande et nécessite [ffmpeg](https://ffmpeg.org/) pour fonctionner:
`soundsForThymio.py -i <inputfile.ext> -o <outputfile.wav>`
Exemple:
`soundsForThymio.py -i son-de-voiture.wav -o P1.wav`

### Vérifier (et corriger) un fichier son

Il se peut que même bien configuré, le convertisseur audio peut malgré tout sortir un son mal formaté si ce dernier se basse sur ffmpeg. La cause est dûe à ce bug https://trac.ffmpeg.org/ticket/10229 qui n'est actuellement pas encore corrigé. 
Le script `patchThymioWav` permet de vérifier si un son présente des problèmes, et de corriger le bug énoncé ci-dessus. /!\ Attention le script ne corrige QUE le bug de ffmpeg et non pas d'autres potentiels problèmes. Si vous voulez un fichier qui marche à coup sûr, utilisez `soundsForThymio`

#### Vérification d'un son
`patchThymioWav.py -c -i P0.wav`

### Correction d'un son
`patchThymioWav.py -i Pko.wav -o P1.wav`

