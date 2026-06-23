import uuid


class SessionStore:

    _sessions = {}

    @classmethod
    def create(
        cls,
        receipt,
        rules,
        unallocated_items,
    ):
        session_id = str(
            uuid.uuid4()
        )

        cls._sessions[
            session_id
        ] = {
            "receipt": receipt,
            "rules": rules,
            "unallocated_items": unallocated_items,
        }

        return session_id

    @classmethod
    def get(
        cls,
        session_id: str,
    ):
        print(
             "AVAILABLE SESSIONS:",
            cls._sessions.keys()
        )

        return cls._sessions.get(
            session_id
        )

    @classmethod
    def delete(
        cls,
        session_id: str,
    ):
        cls._sessions.pop(
            session_id,
            None,
        )