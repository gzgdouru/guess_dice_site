from django.utils.deprecation import MiddlewareMixin

from analysis.models import ClientIp


class MarkVisitIpMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            realIp = request.META["HTTP_X_FORWARDED_FOR"]
            print(request.META)
            realIp = realIp.split(",")[0]
        except:
            realIp = request.META["REMOTE_ADDR"]
        url = request.path
        if realIp != "127.0.0.1":
            ClientIp(ip=realIp, url=url).save()
