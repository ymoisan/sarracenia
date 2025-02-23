
----------------------
GUIDE DE MISE A NIVEAU
----------------------

Ce dossier documente les changements de comportement afin de fournir des conseils aux personnes qui effectuent la mise à niveau
à partir d’une version précédente. Les sections sont intitulées pour indiquer les changements nécessaires lorsqu'il y a
une mise à niveau vers cette version. Pour effectuer une mise à niveau sur plusieurs versions, il faut démarrer
à la version après celle installée, et tenir compte de toutes les notifications pour la version intérim.
Bien que la stabilité du langage de configuration soit importante, à l’occasion, les changements ne peuvent
être évités. Ce fichier ne documente pas les nouveaux, mais uniquement les modifications qui posent problème lors des
mises à niveau. Les avis prennent la forme :

**CHANGEMENT**
   Indique où les fichiers de configuration doivent être modifiés pour obtenir le même comportement qu’avant la publication.

**ACTION**
   Indique une activité de maintenance requise dans le cadre d’un processus de mise à niveau.

**BUG**
   Indique un bug grave pour indiquer que le déploiement de cette version n’est pas recommandé.

*NOTICE*
   Un changement de comportement qui sera perceptible lors de la mise à niveau, mais qui n’est pas préoccupant.

*SHOULD*
   Indique les interventions recommandées qui sont recommandées, mais pas obligatoires. Si l’activité prescrite n’est pas effectuée,
   la conséquence est soit une ligne de configuration qui n’a aucun effet (gaspillage), soit l’application
   qui peut générer des messages.

Les sections sont intitulées par les changements intervenus au niveau en question.

Instructions d’installation
---------------------------

`Installation Guide <../Tutorials/Install.rst>`_

git
---

3.0.22
------

*CHANGEMENTMENT*: option *destination* dans une configuration de poll est remplacé par *pollUrl*

*CHANGEMENTMENT*: option *destination* dans une configuration de sender est remplacé par *remoteUrl*

*ACTION*: remplacer les *destination* dans les configurations affectés (traité automatiquement
dans le cas de conversion à partir de v2.)

3.0.17
------

*CHANGEMENT*: La chaine de charactères "Vendor" est changé de "science.gc.ca" à "MetPX". 
     Ce changement modifie le placement des fichiers sur la platteforme *Windows*.

*CHANGEMENT*: l´encodage des messages d´annonce v03 est changé: *Integrity* est rendu optionnel.

*CHANGEMENT*: l'encodage des messages d'annonce v03 est changé: le champs *fileOp* est rajouté
     pour séparer les operations sur des fichiers qui ne comprennent pas des transmissions
     de données: créations de liens symboliques, renommage de fichier, suppression de fichiers.
     Le champs *Integrity* est maintenant dédié au sommes de contrôle pour les données.



3.0.15
------

*NOTICE*: rétablir les paquets Debian et Windows en supprimant les exigences matérielles pour les modules python
    qui sont difficiles à satisfaire. À partir de la version 3.0.15, les dépendances sont modulaires.


*CHANGEMENT*: il y a maintenant quatre "extras" configurés pour les paquets pip pour metpx-sr3.

  * amqp - capacité de communiquer avec les courtiers AMQP (rabbitmq)

  * mqtt - capacité à communiquer avec les courtiers MQTT

  * ftppoll - possibilité d’interroger les serveurs FTP

  * vip - activez les paramètres vip (Virtual IP) pour implémenter le traitement singleton pour la prise en charge de la haute disponibilité.

  avec l’installation de pip, on peut inclure tous les extras via::

      pip install metpx-sr3[amqp,mqtt,ftppoll,vip]

  avec les paquets Linux, installez les paquets natifs correspondants pour activer les fonctionnalités correspondantes

  sur Ubuntu, respectivement::

      apt install python3-amqp
      apt install python3-paho-mqtt
      apt install python3-dateparser python3-tz
      apt install python3-netifaces

  sr3 recherche les modules pertinents au démarrage et active automatiquement la prise en charge des fonctionnalités pertinentes.

**CHANGEMENT**: le placement des fichiers pour indiquer des configurations désactivées.
     Avant, l’action *disable* ajoutait un *.off* au nom de fichier de configuration.
     Maintenant, on crée à la place un fichier *disabled* dans le répertoire d’état.
     Les fichiers de configuration ne sont plus modifié par la gestion routinière
     d’activités.

3.0.14
------

bêta initiale.

*NOTICE* : seuls les paquets pip fonctionnent actuellement. Pas de paquets Debian sur launchpad.net
          ni aucun package Windows.


V2 to Sr3
---------

*NOTICE*: Sr3 est un refacteur très profond de Sarracenia. Pour plus de détails sur la nature
          des changements, `allez ici <../Contribution/v03.html>`_ Brièvement, où v2
          est une application écrite en python qui avait une petite installation d’extension,
          Sr3 est une boîte à outils qui fournit naturellement une API et est beaucoup plus
          pythonique. Sr3 est construit avec moins de code, plus de code maintenable, et
          prend en charge plus de fonctionnalités, et plus naturellement.

**CHANGEMENT** : les messages de journal sont complètement différents. Toute analyse des journaux devra être examinée.
          Le nouveau format de journal inclut un préfixe avec un process-id et la routine générant le message.

*NOTICE* : Lors de la migration de la v2 vers la sr3, les configurations simples "fonctionneront simplement".
          Cependant, les cas reposant sur des plugins construits par l’utilisateur nécessiteront des efforts de portage.
          Les plugins intégrés fournis avec Sarracenia ont été portés comme des exemples.

**CHANGEMENT**: placement du fichier. Sous Linux : ~/.cache/sarra -> ~/.cache/sr3
          ~/.config/sarra -> ~/.config/sr3
          Changement similaire sur d’autres plateformes. Les différents placements
          permettent d’exécuter v2 et sr3 en même temps sur le même serveur.

**CHANGEMENT**: L’interface de ligne de commande (CLI) est différente. Il n’y a qu’un seul entry_point principal : sr3.
          donc la plupart des invocations sont différentes dans un modèle comme ci-dessous::

             sr_subscribe start config -> sr3 start subscribe/config

          dans sr3, on peut spécifier une série de configurations sur lesquelles fonctionner avec une seule commande::

             sr3 start poll/airnow subscribe/airnow sender/cmqb

**CHANGEMENT**: dans sr3, utilisez -- pour les options de mots complets, comme --config ou --broker.  Dans la v2, vous
           pouvez utiliser -config et -broker, mais un tiret unique est réservé aux options à caractère unique.
           Ceci est le résultat de sr3 utilisant la classe ArgParse standard python::

                -config hoho.conf  -> in v2 refers to loading the hoho.conf file as a configuration.

           Dans sr3, il sera interprété comme -c (config) charger le fichier config.conf, et hoho.conf
           fait partie d’une option ultérieure. dans sr3::

                --config hoho.conf

           le fait comme prévu.

**CHANGEMENT**: En général, les traits de soulignement dans les options sont remplacés par camelCase. p. ex. :

          v2 loglevel -> sr3 logLevel

          Les options v2 qui sont renommées seront comprises, mais un message d’information sera produit au
          démarrage. Le trait de soulignement est toujours utilisé à des fins de regroupement. Options qui ont changé :

          ========================= ==================
          **Option v2**             **Option v3**
          ------------------------- ------------------
          accel_scp_threshold       accelThreshold
          accel_wget_threshold      accelThreshold
          accept_unmatch            acceptUnmatched
          accept_unmatched          acceptUnmatched
          base_dir                  baseDir
          basedir                   baseDir
          baseurl                   baseUrl
          bind_queue                queueBind
          cache                     nodupe_ttl
          cache_basis               nodupe_basis
          caching                   nodupe_ttl
          chmod                     permDefault
          chmod_dir                 permDirDefault
          chmod_log                 permLog
          declare_exchange          exchangeDeclare
          declare_queue             queueDeclare
          default_dir_mode          permDirDefault
          default_log_mode          permLog
          default_mode              permDefault
          document_root             documentRoot
          e                         fileEvents
          events                    fileEvents
          exchange_split            exchangeSplit
          file_time_limit           nodupe_fileAgeMax
          hb_memory_baseline_file   MemoryBaseLineFile
          hb_memory_max             MemoryMax
          hb_memory_multiplier      MemoryMultiplier
          heartbeat                 housekeeping
          instance                  instances
          ll                        logLevel
          logRotate                 logRotateCount
          logRotate_interval        logRotateInterval
          log_format                logFormat
          log_reject                logReject
          logdays                   logRotateCount
          loglevel                  logLevel
          no_duplicates             nodupe_ttl
          post_base_dir             post_baseDir
          post_base_url             post_baseUrl
          post_basedir              post_baseDir
          post_baseurl              post_baseUrl
          post_document_root        post_documentRoot
          post_exchange_split       post_exchangeSplit
          post_rate_limit           messageRateMax
          post_topic_prefix         post_topicPrefix
          preserve_mode             permCopy
          preserve_time             timeCopy
          queue_name                queueName
          report_back               report
          source_from_exchange      sourceFromExchange
          sum                       integrity
          suppress_duplicates       nodupe_ttl
          suppress_duplicates_basis nodupe_basis
          topic_prefix              topicPrefix
          ========================= ==================

**CHANGEMENT** : topic_prefix v02.post par défaut -> topicPrefix v03
          peut avoir besoin de modifier les configurations pour remplacer la valeur par défaut pour obtenir des
          configurations compatibles.

**CHANGEMENT**: v2 : *mirror* a la valeur false sur tous les composants à l’exception de sarra.
          sr3 : la valeur par défaut de *mirror* est True sur tous les composants, à l’exception de subscribe.

*NOTICE* : Les plugins v2 les plus courants sont on_message, et on_file
          (selon les directives *plugin* et *on\_* dans les fichiers de configuration v2) qui peuvent
          être honoré via la classe de plugin `v2wrapper sr3 plugin class <../Reference/flowcb.html#module-sarracenia.flowcb.v2wrapper>`_
          De nombreux autres plugins ont été portés, et le module de configuration
          reconnaît les anciens paramètres de configuration et ils sont interprétés
          dans le nouveau style. les conversions connues peuvent être visualisées en démarrant
          un interpréteur python ::


            Python 3.8.10 (default, Nov 26 2021, 20:14:08)
            [GCC 9.3.0] on linux
            Type "help", "copyright", "credits" or "license" for more information.
            >>> import sarracenia.config,pprint
            >>> pp=pprint.PrettyPrinter()
            >>> pp.pprint(sarracenia.config.convert_to_v3)
            {
             'do_send':   {
                            'file_email':           ['flowCallback',
                                                     'sarracenia.flowcb.send.email.Email']
                          },
             'ls_file_index':                       ['continue'],
             'no_download':                         ['download',
                                                     'False'],
             'notify_only':                         ['download',
                                                     'False'],

             'on_message':{
                            'msg_2http':            ['flow_callback',
                                                     'sarracenia.flowcb.accept.tohttp.ToHttp'],
                            'msg_2local':           ['flow_callback',
                                                     'sarracenia.flowcb.accept.tolocal.ToLocal'],
                            'msg_2localfile':       ['flow_callback',
                                                     'sarracenia.flowcb.accept.tolocalfile.ToLocalFile'],
                            'msg_WMO_type_suffix':  ['flow_callback',
                                                     'sarracenia.flowcb.accept.wmotypesuffix.WmoTypeSuffix'],
                            'msg_by_source':        ['continue'],
                            'msg_by_user':          ['continue'],
                            'msg_delay':            ['flow_callback',
                                                     'sarracenia.flowcb.accept.messagedelay.MessageDelay'],
                            'msg_delete':           ['flow_callback',
                                                     'sarracenia.flowcb.filter.deleteflowfiles.DeleteFlowFiles'],
                            'msg_download':         ['continue'],
                            'msg_download_baseurl': ['flow_callback',
                                                     'sarracenia.flowcb.accept.downloadbaseurl.DownloadBaseUrl'],
                            'msg_dump':             ['continue'],
                            'msg_fdelay':           ['continue'],
                            'msg_from_cluster':     ['continue'],
                            'msg_gts2wistopic':     ['continue'],
                            'msg_hour_tree':        ['flow_callback',
                                                     'sarracenia.flowcb.accept.hourtree.HourTree'],
                            'msg_http_to_https':    ['flow_callback',
                                                     'sarracenia.flowcb.accept.httptohttps.HttpToHttps'],
                            'msg_log':              ['logEvents',
                                                     'after_accept'],
                            'msg_overwrite_sum':    ['continue'],
                            'msg_print_lag':        ['flow_callback',
                                                     'sarracenia.flowcb.accept.printlag.PrintLag'],
                            'msg_rawlog':           ['logEvents', 'after_accept'],
                            'msg_rename4jicc':      ['flow_callback',
                                                     'sarracenia.flowcb.accept.rename4jicc.Rename4Jicc'],
                            'msg_rename_dmf':       ['flow_callback',
                                                     'sarracenia.flowcb.accept.renamedmf.RenameDMF'],
                            'msg_rename_whatfn':    ['flow_callback',
                                                     'sarracenia.flowcb.accept.renamewhatfn.RenameWhatFn'],
                            'msg_renamer':          ['flow_callback',
                                                     'sarracenia.flowcb.accept.renamer.Renamer'],
                            'msg_save':             ['flow_callback',
                                                     'sarracenia.flowcb.accept.save.Save'],
                            'msg_skip_old':         ['flow_callback',
                                                     'sarracenia.flowcb.accept.skipold.SkipOld'],
                            'msg_speedo':           ['flow_callback',
                                                     'sarracenia.flowcb.accept.speedo.Speedo'],
                            'msg_stdfiles':         ['continue'],
                            'msg_stopper':          ['continue'],
                            'msg_sundew_pxroute':   ['flow_callback',
                                                     'sarracenia.flowcb.accept.sundewpxroute.SundewPxRoute'],
                            'msg_test_retry':       ['flow_callback',
                                                     'sarracenia.flowcb.accept.testretry.TestRetry'],
                            'msg_to_clusters':      ['flow_callback',
                                                     'sarracenia.flowcb.accept.toclusters.ToClusters'],
                            'msg_total':            ['continue'],
                            'msg_total_save':       ['continue'],
                            'post_hour_tree':       ['flow_callback',
                                                     'sarracenia.flowcb.accept.posthourtree.PostHourTree'],
                            'post_long_flow':       ['flow_callback',
                                                     'sarracenia.flowcb.accept.longflow.LongFLow'],
                            'post_override':        ['flow_callback',
                                                     'sarracenia.flowcb.accept.postoverride.PostOverride'],
                            'post_total':           ['continue'],
                            'post_total_save':      ['continue'],
                            'wmo2msc':              ['flow_callback',
                                                     'sarracenia.flowcb.filter.wmo2msc.Wmo2Msc']
                           },
             'on_post':    {
                            'post_log':             ['logEvents', 'after_work']
                           },
             'plugin':     {
                            'accel_scp':            ['continue'],
                            'accel_wget':           ['continue'],
                            'msg_fdelay':           ['flowCallback',
                                                     'sarracenia.flowcb.filter.fdelay.FDelay'],
                            'msg_pclean_f90':       ['flowCallback',
                                                     'sarracenia.flowcb.filter.pclean_f90.PClean_F90'],
                            'msg_pclean_f92':       ['flowCallback',
                                                     'sarracenia.flowcb.filter.pclean_f92.PClean_F92']
                           },
             'windows_run':                         ['continue'],
             'xattr_disable':                       ['continue']
            }
            >>>

          Les options répertoriées comme "continuer" sont obsolètes, remplacées par le traitement par défaut ou rendues
          inutile par des changements dans la mise en œuvre.

*NOTICE* : pour les utilisateurs d’API et les rédacteurs de plugins, le format de plugin v2 est entièrement remplacé par
          la classe `Flow Callback <FlowCallbacks.html>`_. La nouvelle fonctionnalité de plugin
          peut principalement être implémenté sous forme de plugins.

**CHANGEMENT**: les plugins do_poll v2 doivent être remplacés par une sous-classification pour `poll <../Reference/flowcb.html#module-sarracenia.flowcb.poll>`_
          Exemple dans  `plugin porting <v2ToSr3.html>`_

**CHANGEMENT**: Les plugins on_html_page v2 sont également remplacés par la sous-classification `poll <.. /Reference/flowcb.html#module-sarracenia.flowcb.poll>`_

**CHANGEMENT**: v2 do_send remplacé par send entrypoint dans un plugin Flowcb `plugin portage <v2ToSr3.html>`_

*NOTICE* : les plugins d’accélérateur v2 sont remplacés par l’accélérateur intégré.
          accel_wget_command, accel_scp_command, accel_ftpget_command, accel_ftpput_command,
          accel_scp_command, sont maintenant des options intégrées utilisées par la classe
          `Transfer <../Reference/flowcb.html#module-sarracenia.transfer>`_.
          L’ajout de nouveaux protocoles de transfert se fait en sous-classant Transfer.

*SHOULD*: v2 on_message -> after_accept doit être réécrit `portage de plugin <v2ToSr3.html>`_

*SHOULD*: v2 on_file -> after_work devrait être réécrit `portage de plugin <v2ToSr3.html>`_

*SHOULD* : les plugins v2 doivent être réécrits. `portage de plugin <v2ToSr3.html>`_
          il existe de nombreux plugins intégrés qui sont portés et automatiquement
          convertis, mais les externes doivent être réécrits.

          Cependant, cette compatibilité a des conséquences sur les performances, de sorte qu’un trafic élevé
          de flux s’exécuteront avec moins de charge cpu et mémoire si les plugins sont portés sur sr3.
          Pour créer des plugins sr3 natifs, il faut étudier la classe flowCallback (flowcb).

**CHANGEMENT**: on_watch plugins devient entry_point un point d’entrée after_accept sr3 dans un flowcb dans un watch.

*ACTION* : Le composant **sr_audit a disparu**. Remplacé par l’exécution de *sr sanity* en tant que cron
          (ou tâche planifiée sous Windows) pour s’assurer que les processus nécessaires continuent de s’exécuter.

**CHANGEMENT** : paramètres obsolètes : use_amqplib, use_pika. Le nouveau `sarracenia.moth.amqp <../Reference/code.html#module-sarracenia.moth.amqp>`_
          utilise la bibliothèque amqp.  Pour utiliser d’autres bibliothèques, il faut créer de nouvelles sous-classes de sarracenia.moth.

**CHANGEMENT**: statehost est maintenant un indicateur booléen, l’option fqdn n’est plus implémentée.
          s’il s’agit d’un problème, soumettez un problème. Ce n’est tout simplement pas considéré comme intéressant pour l’instant.

**CHANGEMENTMENT**: sr_retry est devenu `retry.py <../Reference/flowcb.html#module-sarracenia.flowcb.retry>`_.
          Tous les plugins accédant aux structures internes de sr_retry.py doivent être réécrits.
          Cet accès n’est plus nécessaire, car l’API définit comment mettre des messages sur
          la fil d’attente de nouvelle tentative (déplacer les messages vers worklist.failed. )

*CHANGEMENT* : le watch sr3, avec l’option *force_polling*, est beaucoup moins efficace
          sur sr3 que v2 pour les grandes arborescences de répertoires (voir numéro #403 )
          Idéalement, on n’utilise pas du tout *force_polling*.
