import json

from Http.Requests.scan import ScanModel, ScanRequestModel
from Providers.Queue.QueueContext import RabbitMQPublisher
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Config.ElasticContext import ElasticsearchContext
from fastapi import Depends
from Middleware.Auth.token import verify_token
from fastapi.encoders import jsonable_encoder




router = APIRouter(prefix="/v1")


@router.post("/scan", tags=["Scan"])
def send_target_queue(target_message: ScanModel, authenticate: str = Depends(verify_token)):
    with RabbitMQPublisher() as publisher:
        data = jsonable_encoder(target_message)
        publisher.publish_message(str(data))
    return "sent"


@router.get("/result", tags=["Scan"])
def get_results(authenticate: str = Depends(verify_token)):
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


@router.post("/scan_new", tags=["Scan"])
def send_target_queue(target_message: ScanRequestModel, authenticate: str = Depends(verify_token)):
    target_message.target = str(target_message.target)
    target_message.request_datetime = str(target_message.request_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    msg = json.dumps(target_message.dict())
    with RabbitMQPublisher() as publisher:
        publisher.publish_message(msg)
    return "sent"

