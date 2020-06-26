from redis import Redis
from rq import Queue

redis_queue = Queue(connection=Redis())
