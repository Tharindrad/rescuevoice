import json, logging, uuid
log = logging.getLogger("rescuevoice")

def new_trace_id(): return str(uuid.uuid4())

def event(event_type: str, trace_id: str, **fields):
    payload={"trace_id":trace_id,"event":event_type,**fields}
    log.info(json.dumps(payload, separators=(",",":")))
    return payload
