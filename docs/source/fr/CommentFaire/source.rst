
===================
 Sources de données
===================

--------------------------------------------------------------
Injection de données dans un réseau de pompes MetPX-Sarracenia
--------------------------------------------------------------

.. warning::
  **FIXME** : Les sections manquantes sont mises en surbrillance par **FIXME**.
  Pas vraiment prêt à l’emploi, il en manque trop pour l’instant.

.. NOTE::
  **FIXME**: éléments manquants connus: bonne discussion sur le choix de la somme de contrôle.
  Mise en garde sur les stratégies de mise à jour des fichiers. Cas d’utilisation d’un fichier constamment mis à jour,
  plutôt que d’émettre de nouveaux fichiers.)

Enregistrement de révision
--------------------------

:version: |release|
:date: |today|

Une pompe de données Sarracenia est un serveur Web (ou sftp) avec des notifications pour que les
abonnés sachent rapidement quand de nouvelles données sont arrivées. Pour savoir quelles données sont déjà disponibles
sur une pompe, affichez l’arborescence avec un navigateur Web. Pour des besoins immédiats simples, on peut
télécharger des données à l’aide du navigateur lui-même ou d’un outil standard tel que wget.
L’intention habituelle est que sr_subscribe télécharge automatiquement les données
voulu d'un répertoire sur une machine d’abonné où d’autres logiciels
peuvent les traiter. Notez que ce manuel utilise des abonnements pour tester
l'injection de données, de sorte que le guide de l’abonné doit probablement être lu avant
celui-ci.

Quelle que soit la façon dont cela est fait, injecter des données signifie indiquer à la pompe où les données sont
de sorte qu’elles puissent être acheminé vers/par la pompe. Cela peut être fait par l’un ou l’autre
à l’aide de la commande active et explicite sr_post, ou simplement à l’aide de sr_watch sur un répertoire.
Lorsqu’il y a un grand nombre de fichiers et/ou des contraintes de rapidité serrées, l’appel
de sr_post directement par le producteur du dossier est optimale, par ce que sr_watch peut fournir de
performances décevantes. Une autre approche explicite, mais à basse fréquence, est la
commande sr_poll, qui permet d’interroger des systèmes distants pour extraire des données
dans le réseau efficacement.

Alors que sr_watch est écrit comme un système de surveillance de répertoire optimal, il n’y a tout simplement pas de
moyen rapide de regarder des arborescences de répertoires volumineuses (disons, plus de 100 000 fichiers). Sur
dd.weather.gc.ca, par exemple, il y a 60 millions de fichiers dans environ un million de répertoires.
Parcourir cette arborescence de répertoires une fois prend plusieurs heures. Pour rechercher de nouveaux fichiers,
la meilleure résolution temporelle est toutes les quelques heures (disons 3). Donc en moyenne une notification
se produira 1,5 heure après l’affichage du fichier. En utilisant I_NOTIFY (sur Linux), cela
prend plusieurs heures pour démarrer, car il doit effectuer une promenade initiale dans l’arborescence des fichiers jusqu’à
configurer toutes les watches. Après cela, ce sera instantané, mais s’il y a trop de fichiers,
(et 60 millions, c’est très probablement trop) il va simplement planter et refuser de fonctionner.
Ce sont des limites inhérentes à la surveillance des répertoires, quelle que soit la façon dont cela se fait.
S’il est vraiment nécessaire de le faire, il y a de l’espoir.  S’il vous plaît
consultez `Quickly Announcing Very Large Trees On Linux`_

Avec sr_post, le programme qui place le fichier n’importe où dans l’arborescence arbitrairement profond[1]_, cela  indique
à la pompe (qui indiquera aux abonnés) exactement où chercher. Il n’y a pas de limites de
système à craindre. C’est ainsi que fonctionne dd.weather.gc.ca, et les notifications sont inférieures à la seconde, avec
60 millions de fichiers sur le disque. Il est beaucoup plus efficace, en général, de faire des
notifications directe plutôt que de passer par l’indirection du système de fichiers, mais des cas plus
petite et plus simples, cela fait peu de différence pratique.

Dans le cas le plus simple, la pompe prend les données de votre compte, où que vous les ayez,
à condition que vous lui donniez la permission. Nous décrivons d’abord ce cas.

.. note::
   Bien que l’arborescence de fichiers elle-même n’ait pas de limites en profondeur ou en nombre, la possibilité de
   filtrer basé sur *topics* est limité par AMQP à 255 caractères. Donc la configuration de l'item *subtopic*
   est limité à un peu moins que cela. Il n’y a pas delimite fixe
   car les topics sont codées en utf8 qui est de longueur variable. Notez que le
   directive *subtopic* vise à fournir une classification grossière, et
   l’utilisation de *accept/reject* est destinée à un travail plus détaillé. Les clauses *accept/reject*
   ne s’appuient pas sur les en-têtes AMQP, en utilisant des noms de chemin stockés dans le corps du
   message de notifications, et ne sont donc pas affectés par cette limite.

Injection SFTP
--------------

L’utilisation directe de la commande sr_post(1) est le moyen le plus simple d’injecter des données
dans le réseau de pompes. Pour utiliser sr_post, vous devez savoir:

- le nom du courtier local: ( disons: ddsr.cmc.ec.gc.ca )
- vos informations d’authentification pour ce broker ( disons: user=rnd : password=rndpw )
- votre propre nom de serveur (disons: grumpy.cmc.ec.gc.ca )
- votre propre nom d’utilisateur sur votre serveur (disons: peter)

Supposons que l’objectif soit que la pompe accède au compte de Peter via SFTP. Alors vous avez besoin
de prendre la clé publique de la pompe et la placer dans le fichier .ssh/authorized_keys de peter.
Sur le serveur que vous utilisez (*grumpy*), il faut faire quelque chose comme ceci::

  cat pump.pub >>~peter/.ssh/authorized_keys

Cela permettra à la pompe d’accéder au compte de Peter sur grumpy en utilisant sa clé privée.
Donc, en supposant que l’on est connecté au compte de Peter sur grumpy, on peut stocker les
informations d’identification du courtier en toute sécurité ::

  echo 'amqps://rnd:rndpw@ddsr.cmc.ec.gc.ca' >> ~/.config/sarra/credentials.conf:

.. notice::
  Les mots de passe sont toujours stockés dans le fichier credentials.conf.
  pour éviter cela, il est préférable d'utiliser des clés, que Sarracenia peut trouver en
  en regardant les fichiers de configuration ssh. Configurez ssh pour qu'il fonctionne, et Sarracenia
  fonctionnera aussi.

Donc, maintenant, la ligne de commande pour sr_post n’est que l’URL pour que ddsr récupère le
fichier sur grumpy::

  sr_post -post_broker amqp://guest:guest@localhost/ -post_base_dir /var/www/posts/ \
  -post_base_url http://localhost:81/frog.dna

  2016-01-20 14:53:49,014 [INFO] Output AMQP  broker(localhost) user(guest) vhost(/)
  2016-01-20 14:53:49,019 [INFO] message published :
  2016-01-20 14:53:49,019 [INFO] exchange xs_guest topic v02.post.frog.dna
  2016-01-20 14:53:49,019 [INFO] notice   20160120145349.19 http://localhost:81/ frog.dna
  2016-01-20 14:53:49,020 [INFO] headers  parts=1,16,1,0,0 sum=d,d108dcff28200e8d26d15d1b3dfeac1c to_clusters=localhost

Il y a un sr_subscribe qui s’abonne à tous les messages ``*.dna`` indiqués dans le journal d’abonnement.
Voici le fichier de configuration ::

  broker amqp://guest:guest@localhost
  directory /var/www/subscribed
  subtopic #
  accept .*dna*

et voici la sortie associée du fichier journal d’abonnement::

  2016-01-20 14:53:49,418 [INFO] Received notice  20160120145349.19 http://grumpy:80/ 20160120/guest/frog.dna
  2016-01-20 14:53:49,419 [INFO] downloading/copying into /var/www/subscribed/frog.dna
  2016-01-20 14:53:49,420 [INFO] Downloads: http://grumpy:80/20160120/guest/frog.dna  into /var/www/subscribed/frog.dna 0-16
  2016-01-20 14:53:49,424 [INFO] 201 Downloaded : v02.report.20160120.guest.frog.dna 20160120145349.19 http://grumpy:80/ 20160120/guest/frog.dna 201 sarra-server-trusty guest 0.404653 parts=1,16,1,0,0 sum=d,d108dcff28200e8d26d15d1b3dfeac1c from_cluster=test_cluster source=guest to_clusters=test_cluster rename=/var/www/subscribed/frog.dna message=Downloaded

Ou bien, voici le journal d’une instance sr_sarra ::

  2016-01-20 14:53:49,376 [INFO] Received v02.post.frog.dna '20160120145349.19 http://grumpy:81/ frog.dna' parts=1,16,1,0,0 sum=d,d108dcff28200e8d26d15d1b3dfeac1c to_cluster=ddsr.cmc.ec.gc.ca
  2016-01-20 14:53:49,377 [INFO] downloading/copying into /var/www/test/20160120/guest/frog.dna
  2016-01-20 14:53:49,377 [INFO] Downloads: http://grumpy:81/frog.dna  into /var/www/test/20160120/guest/frog.dna 0-16
  2016-01-20 14:53:49,380 [INFO] 201 Downloaded : v02.report.frog.dna 20160120145349.19 http://grumpy:81/ frog.dna 201 sarra-server-trusty guest 0.360282 parts=1,16,1,0,0 sum=d,d108dcff28200e8d26d15d1b3dfeac1c from_cluster=test_cluster source=guest to_clusters=test_cluster message=Downloaded
  2016-01-20 14:53:49,381 [INFO] message published :
  2016-01-20 14:53:49,381 [INFO] exchange xpublic topic v02.post.20160120.guest.frog.dna
  2016-01-20 14:53:49,381 [INFO] notice   20160120145349.19 http://grumpy:80/ 20160120/guest/frog.dna
  @

La commande demande à ddsr de récupérer le fichier treefrog/frog.dna en se connectant
dans grumpy en tant que peter (en utilisant la clé privée de la pompe) pour le récupérer, et le poster
sur la pompe, pour l’acheminement vers les autres destinations de la pompe.

Semblable à sr_subscribe, on peut également placer des fichiers de configuration dans un répertoire spécifique sr_post::

  blacklab% sr_post edit dissem.conf

  post_broker amqps://rnd@ddsr.cmc.ec.gc.ca/
  post_base_url sftp://peter@grumpy

Et puis::

  sr_post -c dissem -url treefrog/frog.dna

S’il existe différentes variétés de publication utilisées, les configurations peuvent être enregistrées pour chacune d’elles.

.. warning::
   **FIXME**: Besoin de faire un exemple réel. ce truc inventé n’est pas suffisamment utile.

   **FIXME**: sr_post n’accepte pas les fichiers de configuration pour le moment, indique la page de manuel.  Vrai/Faux ?

   sr_post lignes de commande peuvent être beaucoup plus simples si c’était le cas.

sr_post revient généralement immédiatement car son seul travail est d’informer la pompe de la disponibilité
de fichiers. Les fichiers ne sont pas transférés lorsque sr_post revient, il ne faut donc pas supprimer les fichiers
après avoir posté sans être sûr que la pompe les a réellement ramassés.

.. NOTE::

  sftp est peut-être le plus simple à implémenter et à comprendre pour l’utilisateur, mais il est aussi
  le plus coûteux en termes de CPU sur le serveur.  Tout le travail de transfert de données est
  fait au niveau de l’application python lorsque l’acquisition sftp est terminée, ce qui n’est pas génial.

  Une version cpu inférieure serait pour le client d’envoyer d’une manière ou d’une autre (sftp?) et puis juste
  indiquer où se trouve le fichier sur la pompe (essentiellement la version sr_sender2).

Notez que cet exemple utilise sftp, mais si le fichier est disponible sur un site Web local,
alors http fonctionnerait, ou si la pompe de données et le serveur source partagent un système de fichiers,
alors même une URL de fichier pourrait fonctionner.


Injection HTTP
--------------
Si nous prenons un cas similaire, mais dans ce cas, il y a un espace accessible http,
les étapes sont les mêmes ou même plus simples si aucune authentification n’est requise pour la pompe
pour acquérir les données. Il faut installer un serveur Web d’une sorte ou d’une autre.

Supposons une configuration qui affiche tous les fichiers sous /var/www sous forme de dossiers, s’exécutant sous
les utilisateurs de www-data. Les données publiées dans ces répertoires doivent être lisibles pour l'utilisateur www-data
pour permettre au serveur Web de le lire. Le serveur exécutant le serveur Web
s’appelle *blacklab*, et l’utilisateur sur le serveur est *peter* s’exécutant comme peter sur blacklab,
un répertoire est créé sous /var/www/project/outgoing, accessible en écriture par peter,
ce qui se traduit par une configuration comme celle-ci ::

  sr_watch edit project.conf

  broker amqp://feeder@localhost/
  url http://blacklab/
  post_base_dir /var/www/project/outgoing


Ensuite, une watch est démarrée::

  sr_watch start project 

.. warning::
  **FIXME** : exemple réel.

  **FIXME** : sr_watch était censé prendre les fichiers de configuration, mais qui cela n'a peut-être pas
   été modifié à cet effet.

Pendant l’exécution de sr_watch, chaque fois qu’un fichier est créé dans le répertoire *document_root*,
il sera annoncé à la pompe (sur localhost, c’est-à-dire le serveur blacklab lui-même).::

 cp frog.dna  /var/www/project/outgoing

.. warning::
  **FIXME** : exemple réel.

Cela déclenche un message à la pompe. Tous les abonnés pourront alors télécharger
le fichier.

.. warning::
   **FIXME**. trop cassé pour l’instant pour vraiment l'éxécuter aussi facilement...
   donc la création d’une vraie démo est différée.

Interrogation de sources externes
---------------------------------

Certaines sources sont intrinsèquement éloignées, et nous sommes incapables de les intéresser ou de les affecter.
On peut configurer sr_poll pour extraire des données de sources externes, généralement des sites Web.
La commande sr_poll s’exécute généralement comme un singleton qui suit les nouveautés dans une arborescence de source
et crée des messages de notification de source à traiter par le réseau de pompes.

Les serveurs externes, en particulier les serveurs Web, ont souvent différentes façons de publier leur
listes de produits, de sorte que le traitement personnalisé de la liste est souvent nécessaire. C’est pourquoi sr_poll
a le paramètre do_poll, ce qui signifie que l’utilisation d’un script de plug-in est pratiquement requise
pour l’utiliser.

.. NOTE::
   voir les poll_script inclus dans le répertoire des plugins de package pour un exemple.
   **FIXME**:

Messages de rapport
-------------------

Si le sr_post a fonctionné, cela signifie que la pompe a accepté de jeter un coup d’œil sur votre dossier.
Pour savoir où vont vos données par la suite, il faut examiner le fichiers de journalisation de la source.
Il est également important de noter que la pompe initiale, ou toute autre pompe
en aval, peut refuser de transmettre vos données pour diverses raisons, qui ne seront que
signalés à la source dans ces messages de rapport.

Pour afficher les messages du rapport source, la commande sr_report n’est qu’une version de sr_subscribe, avec
les mêmes options là où elles ont du sens. Si le fichier de configuration (~/.config/sarra/default.conf)
est configuré, alors tout ce qui est nécessaire est::

  sr_report

Pour afficher les messages de rapport indiquant ce qui est arrivé aux éléments insérés dans le
réseau à partir de la même pompe utilisant ce compte (rnd, dans l’exemple). On peut déclencher
post-traitement arbitraire des messages de rapport à l’aide de plugins on_message.

.. warning::
   **FIXME**: besoin de quelques exemples.

Fichiers volumineux
-------------------

Les fichiers plus volumineux ne sont pas envoyés en tant que bloc unique. Ils sont envoyés en pièces et chaque pièce
a une empreinte digitale, de sorte que lorsque les fichiers sont mis à jour, les parties inchangées
ne pas pas envoyé à nouveau. Il existe un seuil par défaut intégré dans les commandes sr\_,
au-dessus de duquels les messages de notification partitionnés seront effectués par défaut. Ce seuil peut
être ajusté au goût à l’aide de l’option *part_threshold*.

Différentes pompes le long du parcours peuvent avoir des tailles de pièces maximales différentes. Pour
parcourir un chemin donné, la pièce ne doit pas être plus grande que le paramètre de seuil
de toutes les pompes intermédiaires. Une pompe enverra à la source un journal des erreurs
s’il refuse de transférer un fichier.

Comme chaque partie est annoncée, il y a donc un message de rapport correspondant pour
chaque partie.  Cela permet aux expéditeurs de surveiller la progression de la livraison de grands
fichiers.

Fiabilité et sommes de contrôle
-------------------------------

Chaque donnée injectée dans le réseau de pompage doit avoir une empreinte digitale unique (ou somme de contrôle).
Les données circuleront si elles sont nouvelles, et déterminer si les données sont nouvelles est basé sur l’empreinte digitale.
Pour obtenir de la fiabilité dans un réseau sarracenia, plusieurs sources indépendantes sont provisionnées.
Chaque source annonce ses produits, et s’ils ont le même nom et la même empreinte digitale, alors
les produits sont considérés comme identiques.

Le composant sr_winnow de sarracenia examine les messages de notification entrants et note quels produits
sont reçus (par nom de fichier et somme de contrôle). Si un produit est nouveau, il est transmis à d’autres composants
pour le traitement. Si un produit est un doublon, le message de notification n’est plus transféré.
De même, lorsqu'un composant sr_subscribe ou sr_sarra reçoit un message de notification pour un produit qui est déjà
présent sur le système local, ils examineront l’empreinte digitale et ne téléchargeront pas les données à moins qu’elles ne soient différentes.
Les méthodes de somme de contrôle doivent être connues sur un réseau, car les composants en aval les réappliqueront.

Différents algorithmes d’empreintes digitales sont appropriés pour différents types de données, de sorte que
l’algorithme à appliquer doit être choisi par la source de données et non imposé par le réseau.
Normalement, l’algorithme 'd' est utilisé, qui applique le célèbre Message-Digest 5 (md5sum)
aux données du fichier.

Lorsqu’il y a une origine pour les données, cet algorithme fonctionne bien. Pour une haute disponibilité,
les chaînes de production fonctionneront en parallèle, de préférence sans communication entre
eux.  Les articles produits par des chaînes indépendantes peuvent naturellement avoir un temps de traitement différent
et numéros de série différent appliqués, de sorte que les mêmes données traitées par
différentes chaînes ne seront pas identiques au niveau binaire.   Pour les produits fabriqués
par différentes chaînes de production pour être acceptées comme équivalentes, elles doivent avoir
la même empreinte digitale.

Une solution pour ce cas est, si les deux chaînes de traitement produisent des données avec
le même nom, appliquer la somme de contrôle sur le nom du fichier au lieu des données, cela s’appelle 'n'.
Dans de nombreux cas, les noms eux-mêmes dépendent de la chaîne de production, de sorte qu’une
algorithme est nécessaire. Si un algorithme personnalisé est choisi, elle doit être publié sur
le réseau::

 http://dd.cmc.ec.gc.ca/config/msc-radar/sums/

    u.py

Ainsi, les clients en aval peuvent obtenir et appliquer la même algorithme pour comparer les messages de notification
provenant de sources multiples.

.. warning::
   **FIXME**: science-fiction encore: aucun répertoire de configuration de ce type n’existe encore. aucun moyen de les mettre à jour.
   chemin de recherche pour les algos de somme de contrôle?  intégré, à l’échelle du système, par source?

   De plus, si chaque source définit son propre algorithme, elle doit choisir le même
   (avec le même nom) afin d’avoir une correspondance.

   **FIXME** : vérifiez que la vérification des empreintes digitales inclut la correspondance entre l’algorithme et la valeur.

   **FIXME**: pas nécessaire au début, mais probablement à un moment donné.
   en attendant, nous parlons simplement aux gens et incluons leurs algorithmes dans le package.

.. NOTE::

  Méthodes d’empreintes digitales basées sur le nom, plutôt que sur les données réelles,
  entraînera la réexpédition de l’intégralité du fichier lorsqu’ils seront mis à jour.

En-têtes d'utilisateur
----------------------

Que se passe-t-il s’il y a un élément de métadonnées qu’une source de données a choisi pour une raison quelconque de ne pas
inclure dans la hiérarchie des noms de fichiers ? Comment les consommateurs de données peuvent-ils connaître ces informations sans avoir
à télécharger le fichier afin de déterminer qu’il n’est pas intéressant. Un exemple serait les
avertissements météorologiques. Les noms de fichiers peuvent inclure des avertissements météorologiques pour un pays entier.  Si les consommateurs
ne sont intéressés que par le téléchargement d’avertissements qui leur sont locaux, alors, une source de données pourrait
utilisez le hook on_post afin d’ajouter des en-têtes supplémentaires au message de notification.

.. NOTE::
  Une grande flexibilité s’accompagne d’un grand potentiel de préjudice. Les noms de chemin doivent inclure autant d’informations
  que possible car sarracenia est construit pour optimiser le routage en les utilisant.  Des métadonnées supplémentaires doivent être utilisées
  pour compléter, plutôt que remplacer, le routage intégré.

  Pour ajouter des en-têtes aux messages de notification en cours de publication, vous pouvez utiliser l’option d’en-tête.
  Dans une configuration, ajoutez les instructions suivantes ::

    header CAP_province=Ontario
    header CAP_area-desc=Uxbridge%20-%20Beaverton%20-%20Northern%20Durham%20Region
    header CAP_polygon=43.9984,-79.2175 43.9988,-79.219 44.2212,-79.3158 44.4664,-79.2343 44.5121,-79.1451 44.5135,-79.1415 44.5136,-79.1411 44.5137,-79.1407 44.5138,-79.14 44.5169,-79.0917 44.517,-79.0879 44.5169,-79.0823 44.218,-78.7659 44.0832,-78.7047 43.9984,-79.2175

Ainsi, lorsqu’un message de notification de fichier est publié, il inclura les en-têtes avec les valeurs données.
Cet exemple est artificiel parce qu’il affecte statiquement les valeurs d’en-tête appropriées
aux cas simples. Dans ce cas précis, il est probablement plus approprié de mettre en œuvre un
plugin on_post pour les fichiers Common Alerting Protocol pour extraire les informations d’en-tête ci-dessus et
les placer dans les en-têtes de message de notification pour chaque alerte.

Considérations relatives à l’efficacité
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Il n’est pas recommandé de mettre une logique trop complexe dans les scripts du plugin, car ils s’exécutent de manière synchrone avec
les opérations post et receive. Notez que l’utilisation des installations intégrées d’AMQP (en-têtes) est faite pour
être explicitement aussi efficace que possible. À titre d’exemple extrême, inclure du code XML codé dans les messages de notification
n’affectera pas légèrement les performances, cela ralentira le traitement par ordre de grandeur. On ne sera pas
en mesure de compenser avec plusieurs instances, car la pénalité est tout simplement trop importante pour être surmontée.

Considérons, par exemple, les messages du Protocole d’alerte commun (CAP) pour les alertes météorologiques.  Ces alertes
dépassent souvent 100 Ko, alors qu’un message de notification sarracenia est de l’ordre de 200 octets. Les messages de notification sarracenia
vont à beaucoup plus de destinataires que l’alerte : toute personne envisageant de télécharger une alerte, par opposition à ceux qui intéressent réellement l’abonné,
et ces métadonnées seront également incluses dans les messages du rapport,
et donc répliqués dans de nombreux autres endroits où les données elles-mêmes ne seront pas présentes.

Inclure toutes les informations contenues dans la PAC signifierait, juste en termes de transport, 500 fois
plus de capacité utilisée pour un seul message de notification. Lorsqu’il y a plusieurs millions de messages
de notification à transférer, cela s’additionne.
Seules les informations minimales requises par l’abonné pour prendre la décision de télécharger ou non devraient être
ajouter au message de notification.  Il convient également de noter qu’en plus de ce qui précède, il y a généralement
10x à 100x plus de pénalité de processeur de mémoire en analysant une structure de données XML par rapport à la représentation en texte brut, qui
affectera le taux de traitement.

============================================
Quickly Announcing Very Large Trees On Linux
============================================

Pour mettre en miroir de très grands arbres (millions de fichiers) en temps réel, il faut trop de temps pour des outils comme rsync
ou trouvez pour parcourir et générer des listes de fichiers à copier. Sous Linux, on peut intercepter les appels pour des
opérations de fichiers en utilisant la technique bien connue de la bibliothèque de shim. Cette technique fournit virtuellement des
messages de notification en temps réel des fichiers quelle que soit la taille de l’arborescence, avec une surcharge minimale vu que
cette technique impose beaucoup moins de charge que les mécanismes de traversée des arbres et utilise
l'implémentation C de Sarracenia, qui utilise très peu de mémoire ou de ressources de processeur.


Pour utiliser cette technique, il faut avoir l’implémentation C de Sarracenia installée. Les bibliothèque
Libsrshim fait partie de ce package et l’environnement doit être configuré pour intercepter les appels
de la bibliothèque C comme suit::

    export SR_POST_CONFIG=somepost.conf
    export LD_PRELOAD=libsrshim.so.1.0.0

Où *somepost.conf* est une configuration valide qui peut être testée avec sr_post pour publier manuellement un fichier.
Tout processus appelé à partir d’un shell avec ces paramètres aura tous les appels à des routines telles que close(2)
intercepté par libsrshim. Libsrshim vérifiera si le fichier est en cours d’écriture, puis appliquera la configuration
somepost (les clauses accept/reject) et publiera le fichier si cela est approprié.
Exemple::

    blacklab% more pyiotest
    f=open("hoho", "w+" )
    f.write("hello")
    f.close()
    blacklab% 
    
    blacklab% more test2.sh
    
    echo "called with: $* "
    if [ ! "${LD_PRELOAD}" ]; then
       export SR_POST_CONFIG=`pwd`/test_post.conf
       export LD_PRELOAD=`pwd`/libsrshim.so.1.0.0
       exec $0
       #the exec here makes the LD_PRELOAD affect this shell, as well as sub-processes.
    fi
    
    set -x
    
    echo "FIXME: exec above fixes ... builtin i/o like redirection not being posted!"
    bash -c 'echo "hoho" >>~/test/hoho'
    
    /usr/bin/python2.7 pyiotest
    cp libsrshim.c ~/test/hoho_my_darling.txt
    
    blacklab% 
    
    lacklab% ./test2.sh
    called with:  
    called with:  
    +++ echo 'FIXME: exec above fixes ... builtin i/o like redirection not being posted!'
    FIXME: exec above fixes ... builtin i/o like redirection not being posted!
    +++ bash -c 'echo "hoho" >>~/test/hoho'
    2017-10-21 20:20:44,092 [INFO] sr_post settings: action=foreground log_level=1 follow_symlinks=no sleep=0 heartbeat=300 cache=0 cache_file=off
    2017-10-21 20:20:44,092 [DEBUG] setting to_cluster: localhost
    2017-10-21 20:20:44,092 [DEBUG] post_broker: amqp://tsource:<pw>@localhost:5672
    2017-10-21 20:20:44,094 [DEBUG] connected to post broker amqp://tsource@localhost:5672/#xs_tsource_cpost_watch
    2017-10-21 20:20:44,095 [DEBUG] isMatchingPattern: /home/peter/test/hoho matched mask: accept .*
    2017-10-21 20:20:44,096 [DEBUG] connected to post broker amqp://tsource@localhost:5672/#xs_tsource_cpost_watch
    2017-10-21 20:20:44,096 [DEBUG] sr_post file2message called with: /home/peter/test/hoho sb=0x7ffef2aae2f0 islnk=0, isdir=0, isreg=1
    2017-10-21 20:20:44,096 [INFO] published: 20171021202044.096 sftp://peter@localhost /home/peter/test/hoho topic=v02.post.home.peter.test sum=s,a0bcb70b771de1f614c724a86169288ee9dc749a6c0bbb9dd0f863c2b66531d21b65b81bd3d3ec4e345c2fea59032a1b4f3fe52317da3bf075374f7b699b10aa source=tsource to_clusters=localhost from_cluster=localhost mtime=20171021202002.304 atime=20171021202002.308 mode=0644 parts=1,2,1,0,0
    +++ /usr/bin/python2.7 pyiotest
    2017-10-21 20:20:44,105 [INFO] sr_post settings: action=foreground log_level=1 follow_symlinks=no sleep=0 heartbeat=300 cache=0 cache_file=off
    2017-10-21 20:20:44,105 [DEBUG] setting to_cluster: localhost
    2017-10-21 20:20:44,105 [DEBUG] post_broker: amqp://tsource:<pw>@localhost:5672
    2017-10-21 20:20:44,107 [DEBUG] connected to post broker amqp://tsource@localhost:5672/#xs_tsource_cpost_watch
    2017-10-21 20:20:44,107 [DEBUG] isMatchingPattern: /home/peter/src/sarracenia/c/hoho matched mask: accept .*
    2017-10-21 20:20:44,108 [DEBUG] connected to post broker amqp://tsource@localhost:5672/#xs_tsource_cpost_watch
    2017-10-21 20:20:44,108 [DEBUG] sr_post file2message called with: /home/peter/src/sarracenia/c/hoho sb=0x7ffeb02838b0 islnk=0, isdir=0, isreg=1
    2017-10-21 20:20:44,108 [INFO] published: 20171021202044.108 sftp://peter@localhost /c/hoho topic=v02.post.c sum=s,9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043 source=tsource to_clusters=localhost from_cluster=localhost mtime=20171021202044.101 atime=20171021202002.320 mode=0644 parts=1,5,1,0,0
    +++ cp libsrshim.c /home/peter/test/hoho_my_darling.txt
    2017-10-21 20:20:44,112 [INFO] sr_post settings: action=foreground log_level=1 follow_symlinks=no sleep=0 heartbeat=300 cache=0 cache_file=off
    2017-10-21 20:20:44,112 [DEBUG] setting to_cluster: localhost
    2017-10-21 20:20:44,112 [DEBUG] post_broker: amqp://tsource:<pw>@localhost:5672
    2017-10-21 20:20:44,114 [DEBUG] connected to post broker amqp://tsource@localhost:5672/#xs_tsource_cpost_watch
    2017-10-21 20:20:44,114 [DEBUG] isMatchingPattern: /home/peter/test/hoho_my_darling.txt matched mask: accept .*
    2017-10-21 20:20:44,115 [DEBUG] connected to post broker amqp://tsource@localhost:5672/#xs_tsource_cpost_watch
    2017-10-21 20:20:44,115 [DEBUG] sr_post file2message called with: /home/peter/test/hoho_my_darling.txt sb=0x7ffc8250d950 islnk=0, isdir=0, isreg=1
    2017-10-21 20:20:44,116 [INFO] published: 20171021202044.115 sftp://peter@localhost /home/peter/test/hoho_my_darling.txt topic=v02.post.home.peter.test sum=s,f5595a47339197c9e03e7b3c374d4f13e53e819b44f7f47b67bf1112e4bd6e01f2af2122e85eda5da633469dbfb0eaf2367314c32736ae8aa7819743f1772935 source=tsource to_clusters=localhost from_cluster=localhost mtime=20171021202044.109 atime=20171021202002.328 mode=0644 parts=1,15117,1,0,0
    blacklab% 
    


Remarque::
   redirection de fichier du i/o résultant des shell intégrés (pas de processus spawn) dans le shell où
   les variables d’environnement sont d’abord définies NE SERONT PAS PUBLIÉES. seuls les sub-shells sont affectés::

      # ne sera pas publié...
      echo "hoho" > kk.conf

      # sera publié.
      bash -c 'echo "hoho" > kk.conf'
  
   Il s’agit d’une limitation de la technique, car l’ordre de chargement de la bibliothèque dynamique est résolu par le
   processus de démarrage et ne peut pas être modifié par la suite. Une solution de contournement ::

     if [ ! "${LD_PRELOAD}" ]; then
       export SR_POST_CONFIG=`pwd`/test_post.conf
       export LD_PRELOAD=`pwd`/libsrshim.so.1.0.0
       exec $*
     fi

  Ce qui activera la bibliothèque shim pour l’environnement appelant en la redémarrant.
  Ce code particulier peut avoir un impact sur les options de ligne de commande et peut ne pas être directement applicable.

À titre d’exemple, nous avons un arbre de 22 millions de fichiers qui est écrit en continu jour et nuit.
Nous devons copier cette arborescence dans un deuxième système de fichiers le plus rapidement possible,
avec un temps de copie maximal ambitieux d’environ cinq minutes.
