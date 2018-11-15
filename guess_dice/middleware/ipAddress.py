from django.utils.deprecation import MiddlewareMixin

from analysis.models import ClientIp


class MarkVisitIpMiddleware(MiddlewareMixin):
    def process_request(self, request):
        remote_ip = request.META["REMOTE_ADDR"]
        url = request.path
        if remote_ip != "127.0.0.1":
            ClientIp(ip=remote_ip, url=url).save()
