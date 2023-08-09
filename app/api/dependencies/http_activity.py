from pydantic import BaseModel
from starlette.requests import Request


class HttpActivity(BaseModel):
    host: str
    ip: str
    ua: str
    url: str


async def get_http_activity(request: Request) -> HttpActivity:
    client_ip = request.headers.get('X-Real-IP')
    if client_ip is None:
        client_ip = request.headers.get('X-Forwarded-For')
    if client_ip is None:
        client_ip = request.client.host  # type: ignore

    host = request.url.hostname
    url = str(request.url)

    return HttpActivity(host=host,
                        ip=client_ip,
                        ua=request.headers.get('user-agent'),
                        url=url)
