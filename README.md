
Sinewave
========

Learn PUB/SUB with fun.

Redis PUB/SUB example, adapted from [Redis on Windows: Getting Started](https://channel9.msdn.com/Blogs/Interoperability/Redis-on-Windows-Getting-Started)

video:

[![PubSubWithRedisAndPython](https://i.vimeocdn.com/video/738556705_640.webp)](https://player.vimeo.com/video/300250331 "PubSubWithRedisAndPython")

screenshot:

![screenshot](screenshot.png)



## Introduzione

L'esempio proposto ha lo scopo di esaminare alcuni possibili paradigmi di comunicazione fra dispositivi periferici e un server centrale, con particolare riferimento al protocollo PUB/SUB reso disponibile da `Redis`.

L'invio di informazioni da parte del dispositivo può essere concretizzato sia utilizzando una delle tante librerie client disponibili (Python o altri linguaggi), sia mediante una funzione "publish" minimale (per es. scritta in C); questa seconda opzione può essere convenientemente utilizzata in contesti limitati quali Arduino o altre schede embedded.

Le informazioni ricevute sul server possono essere ulteriormente propagate ad eventuali clients web che avessero manifestato il proprio interesse, predisponendo sul server un processo "listener" incaricato di raccogliere i dati come subscriber, per poi eseguirne il broadcast via WebSocket; l'esempio proposto illustra una semplice implementazione basata su `django-channels`.


## Alcuni schemi tradizionali di comunicazione

Esaminiamo alcuni metodi di comunicazione utilizzati tradizionalmente per trasferire
informazioni da un dispositivo periferico ad un server remoto,
per la successiva archiviazione ed elaborazione.

### Trasmissione spontanea

- il dispositivo invia l'informazione non appena disponibile
- se è richiesta la certezza della consegna del messaggio,
  dispositivo e server devono concordare qualche meccanismo di handshake:

    + ACK/NAK + ristrasmissione (per evitare perdita)
    + identificazione dei messaggi con n.ro progressivo (per evitare duplicazione)

- il processo si ripete nel tempo quando nuove informazioni sono disponibili

>TODO: inserire immagine

### Dialogo Master / Slave

- il dispositivo (Slave) contatta il server e stabilisce un canale di comunicazione
  bi-direzionale (tipicamente TCP)
- successivamente, si mette in attesa di comandi da parte del Master
- l'invio del dato al Master avviene solo in seguito ad una sua sollecitazione

>TODO: inserire immagine

## Publish/Subscribe (PUB/SUB)

`Pub/sub` è un pattern di comunicazione che propone di sostituire la connessione
punto-punto fra dispositivo e server, introducendo la mediazione di un agente
intermedio, detto "broker", al fine di disaccoppiare i due interlocutori.

Tipicamente il workflow di comunicazione sarà:

- il server manifesta al broker il proprio interesse a ricevere informazioni
  mediante una sorta di registrazione denominata SUBSCRIBE, e si mette in ascolto
- il dispositivo comunica l'informazione al broker utilizzando il comando PUBLISH
- il broker si incarica di inoltrare l'informazione così ricevuta a tutti i subscribers

Questo schema consente sia al publisher che al subscriber di ignorare
l'esistenza e la posizione dell'interlocutore.

Il dialogo avviene esclusivamente con il broker, e solo indirettamente con il
mittente o destinatario dell'informazione, tramite l'intermediazione del broker.


## Esempio di comunicazione PUB/SUB con Python e Redis

Abbiamo un script che produce una stringhe di lunghezza variabile, modulate con andamento sinusoidale.

Le stringhe prodotte vengono pubblicate su un canale di comunicazione, senza curarsi del fatto che ci siano o meno subscribers in ascolto.

Un secondo script esegue il subscribe sullo stesso canale, e visualizza quanto ricevuto.

Il meccanismo è intrinsecamente scalabile, e numerosi subscribers possono ricevere la stessa informazione senza modificare la strategia di pubblicazione.

Viceversa, più dispositivi possono contribuire alla comunicazione pubblicando informazioni allo stesso canale.


## Web

### Polling

Volendo visualizzare le informazioni ricevute in una pagina web, rimanendo nell'ambito HTTP, possiamo procedere come segue:

- lato server, un processo listener esegue il subscribe
  e memorizza le informazioni ricevute
- la pagina web richiede periodicamente eventuali aggiornamenti

Gli svantaggi di questo approccio sono quelli tipici di un sistema di polling:

- richieste troppo frequenti comportano un inutile consumo di risorse
- riducento la frequenza di polling si introduce una latenza indesiderata
- molto traffico inutile: la pagina web deve "scomodare" il server anche quando
  nessuna nuova informazione è disponibile

### Push

In alternativa, possiamo utilizzare il protocollo WebSocket per sostituire il
polling con una trasmissione "push"

- la pagina web apre un WebSocket, manifestando il proprio interesse a ricevere
  l'informazione
- il server inoltra le informazioni ai client in ascolto quando disponibili

È evidente l'analogia con il pattern precedentemente descritto:

| Web Sockets     | PUB/SUB   |
|-----------------|-----------|
| open            | subscribe |
| write           | publish   |


Sfortunatamente la pagina web non ha modo di fare direttamente il subscribe di un canale PUB/SUB, ma possiamo facilmente realizzare un "bridge" fra i due mondi realizzando lato server un processo che si incarica del subscribe e distribuisce
i messaggi ricevuti ai web sockets attivi.

Allo scopo, riutilizziamo il listener precedente, confezionandolo come Django management command, e sfruttano django-channels per l'interazione con Websocket.

>TODO: scrivere il codice

Il broker diventa il componente critico della comunicazione, e pertanto è importante gestire correttamente eventuali problemi di connessione con redis e garantire un meccanismo robusto di ripristino della connessione.


## Arduino as a Publisher

Il protocollo previsto da Redis è sufficientemente semplice da consentirne l'utilizzo anche in contesti in cui non siano disponibili librerie "redis-client"; parliamo di Arduino o altri sistemi embedded, che non dispongono di un sistema operativo e/o rendono poco agevole la ricompilazione delle librerie esistenti.

Il seguente script Python ripropone il precedente publisher, formattando direttamente i comandi che vengono inviati a Redis; può essere facilmente riscritto in C - serve solo la funzione printf() e un supporto minimale per la comunicazione TCP.


    #!/usr/bin/env python3
    import socket

    ip = "127.0.0.1"
    port = 6379

    s = socket.socket()
    s.connect((ip, port))

    # > PUBLISH mychannel mymessage
    channel = "mychannel"
    message = "mymessage"
    print('> publish %s %s' % (channel, message))
    s.send(
        ("*3\r\n$7\r\nPUBLISH\r\n$%d\r\n%s\r\n$%d\r\n%s\r\n" % (
            len(channel),
            channel,
            len(message),
            message
        )).encode('utf-8')
    )
    print(s.recv(256))

    s.close()

>TODO: inserire nell'esempio

