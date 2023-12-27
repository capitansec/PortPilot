# Port Pilot
Port pilot is a tool for basic port scanning from different zones(WLANs, ZONEs, REGIONs). It's provide to validate firewall or binding rules. It might be very usefully for concurrent internal and external tests.
<center><img src="./Docs/view.png" alt="drawing" width="550"/></center>

## Reason To Use
### Network/OS/Operation Teams
Time by time network policies could be updated. It may cause side effects like intended accessibility. PortPilot could be used to test services by attempting access from multiple points.
### Security Teams
You can perform internal and external tests simultaneously and even perform inter-wlan tests simultaneously.

## Utilized Services
 * RabbitMQ
 * ElasticSearch
 * Grafana
 * ... Will be updated after API integration

## Sequence Diagram
<img src="Docs/Sequence.png">

## Application Topology
<img src="Docs/topo-new.png" width="60%">
