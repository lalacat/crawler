import sys

from twisted.internet.task import react

from twisted.web.client import Agent, ResponseFailed

@react
def main(reactor):
    agent = Agent(reactor)
    requested = agent.request(b"GET", sys.argv[1].encode("ascii"))
    def gotResponse(response):
        print(response.code)
    def noResponse(failure):
        failure.trap(ResponseFailed)
        print(failure.value.reasons[0].getTraceback())
    return requested.addCallbacks(gotResponse, noResponse)