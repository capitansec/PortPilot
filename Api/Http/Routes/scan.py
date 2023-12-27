from Http.Requests.scan import ScanModel
from Providers.Queue.QueueContext import RabbitMQPublisher
from fastapi import APIRouter

router = APIRouter(prefix="/v1")


@router.post("/scan", tags=["Scan"])
def send_target_queue(target_message: ScanModel):
    with RabbitMQPublisher() as publisher:
        publisher.publish_message(str(target_message.target))
    return "İletildi"
