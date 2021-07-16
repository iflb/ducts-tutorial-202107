from ducts.spi import EventHandler, webapi

from datetime import datetime

from aiohttp import web

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    LEN_COMMAND = {'string':'STRLEN', 'hash':'HLEN', 'list':'LLEN', 'stream':'XLEN', 'set':'SCARD', 'zset':'ZCARD'}
    
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('Get the type and length for a given key')
        return handler_spec

    async def handle(self, event):
        redis_key = event.data
        typ = await event.session.redis.execute_str('TYPE', redis_key)
        length = await event.session.redis.execute(LEN_COMMAND[typ], redis_key)
        return {'key': redis_key, 'type': typ, 'length': length}
    
    @webapi.add_route(path='/', method='GET')
    async def service(self, request):
        return web.json_response({'hello':'world'})
