from uuid import uuid4

from starlette.types import ASGIApp, Receive, Scope, Send

from src.core.database import session


class SQLAlchemyMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        context = session.set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as exception:
            raise exception
        finally:
            await session.session.remove()
            session.reset_session_context(context=context)
