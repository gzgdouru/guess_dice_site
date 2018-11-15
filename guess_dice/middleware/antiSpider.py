from django.utils.deprecation import MiddlewareMixin
from django.http import Http404


class CheckUserAgentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META["HTTP_USER_AGENT"]
        if -1 != user_agent.find("python") or -1 != user_agent.find("scrapy"):
            raise Http404("找不到页面")
