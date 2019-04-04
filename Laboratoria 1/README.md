### Węzły (ang. nodes)  
Działające współbieżnie i w dużej mierze niezależnych od siebie programy:  
-węzeł nadrzędny - ROS Master - polecenie **roscore**  
-powinien działać cały czas w trakcie pracy w systemie ROS  
-zatrzymanie: wysłanie sygnału SIGINT (Ctrl + C)  

### Wiadomości (ang. messanges)  
Komunikacja między węzłami.  

### Temat (ang. topic)  
Tematy wiadomości.  

### Publishers   
Węzły, które chcą dzielić informacje. Publikują one informacje w obrębie odpowiedniego tematu.  

### Subscribers  
Węzły odbierające wiadomości.  

## Pakiety  

### Polecenia:  
- **rospack list** - lista wszystkich pakietów w ROS
- **rospack find _package-name_** - znajdowanie katalogu zawierającego dany pakiet  
- **rosls _package-name_** - znajdowanie katalogu zawierającego dany pakiet  
- **roscd _package-name_** - przejście z bieżącego katalogu do katalogu danego pakietu  

## Węzły (ang. nodes)  
Wykonywalne instancje programów systemu ROS.  

### Polecenia:  
- **rostopic list** - lista aktywnych pakietów  
- **rostopic echo _topic-name_** - wyświetlanie wiadomości przesłanych aktualnie w obrębie danego tematu  
- **rostopic hz _topic-name_** - mierzenie częstotliwości publikowania wiadomości  
- **rostopic bw _topic-name_** - mierzenie przepustowości wiadomości  
- **rostopic info _topic-name_** - uzyskiwanie informacji na temat danego tematu  
- **rosmsg show _message-type-name_** - uzyskiwanie informacji na temat przesłanych wiadomości  
- **rostopic pub -r _rate-in-hz_ _topic-name_ _message-type_ _message_content_** - publikowanie wiadomości  

## Usługi (ang. services)  

Usługi oferują komunikację dwukierunkową - węzeł przesyła informację do innego węzła i oczekuje na odpowiedź (klient-serwer).

### Polecenia  
- **rosservice list** - lista aktywnych uslug  
- **rosnode info _node-name_** - lista usług oferowanych przez dane węzeł  
- **rosservice node _service-node_** - odnajdywanie węzła oferującego daną usługę  
- **rosservice type _service-node_** - odczytywanie typu danych konkretnej usługi  
- **rossrv show _service-name_ _request-content_** - szczegółowe informacje na temat typu danych usługi  
- **rosservice call _service-name_ _request-content_** - wywołanie usługi  
