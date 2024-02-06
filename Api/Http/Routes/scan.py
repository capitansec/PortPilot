from Http.Requests.scan import ScanModel
from Providers.Queue.QueueContext import RabbitMQPublisher
from fastapi import APIRouter
from Config.ElasticContext import ElasticsearchContext


router = APIRouter(prefix="/v1")


@router.post("/scan", tags=["Scan"])
def send_target_queue(target_message: ScanModel):
    with RabbitMQPublisher() as publisher:
        publisher.publish_message(str(target_message.target))
    return "İletildi"


@router.get("/result", tags=["Scan"])
def get_results():
    with ElasticsearchContext() as es:
        index_name = "port-scan"

        query = {
            "query": {
                "match_all": {}  # Retrieve all documents
            }
        }

        result = es.search(index=index_name, body=query)

        hits = result.get("hits", {}).get("hits", [])

        results = []
        for hit in hits:
            source = hit.get("_source", {})
            ip = source.get("ip")
            port = source.get("port")
            state = source.get("state")
            timestamp = source.get("@timestamp")

            results.append({
                "ip": ip,
                "port": port,
                "state": state,
                "@timestamp": timestamp
            })

        return {"results": results}