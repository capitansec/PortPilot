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


@router.get("/result_new", tags=["Scan"])
def get_scan_result(scan_id: str, authenticate: str = Depends(verify_token)):
    with ElasticsearchContext() as es:
        try:
            result = es.search(index="port-scan", body={
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"scan_id": scan_id}}
                        ]
                    }
                }
            })

            scans = []
            for hit in result['hits']['hits']:
                source = hit['_source']
                scan = {
                    "scan_id": source.get("scan_id"),
                    "scan_name": source.get("scan_name"),
                    "scan_owner": source.get("scan_owner"),
                    "scan_datetime": source.get("@timestamp"),
                    "host": list(source['hosts'][0].keys())[0],
                    "open_ports": source['hosts'][0][list(source['hosts'][0].keys())[0]]
                }
                scans.append(scan)

            if not scans:
                raise HTTPException(status_code=404, detail="Scan not found")

            return {"scans": scans}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/result/all")
def get_all_results():
    with ElasticsearchContext() as es:
        try:
            result = es.search(index="port-scan", body={"query": {"match_all": {}}})

            scans = []
            for hit in result['hits']['hits']:
                source = hit['_source']
                host_data = source.get('hosts', [])
                if host_data:
                    host_key = list(host_data[0].keys())[0]
                    scan = {
                        "scan_id": source.get("scan_id"),
                        "scan_name": source.get("scan_name"),
                        "scan_owner": source.get("scan_owner"),
                        "scan_datetime": source.get("@timestamp"),
                        "host": host_key
                    }
                    scans.append(scan)

            return {"scans": scans}

        except Exception as e:
            return {"error": str(e)}
