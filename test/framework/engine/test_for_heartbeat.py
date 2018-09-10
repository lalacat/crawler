from test.framework.engine.engine import ExecutionEngine
from twisted.internet import reactor

try:
    ee = ExecutionEngine(None,None)
    opens = ee.open_spider(1,"aaa")
except Exception as e :
    print(e)

reactor.run()