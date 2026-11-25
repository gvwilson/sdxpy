from tracing_decorators import traced


class GenericService:
    async def do_work(self):
        pass


# mccole:service
class Service(GenericService):
    @traced("handle_request")
    async def handle_request(self, request):
        result = await self.do_work()
        return result


# mccole:/service
