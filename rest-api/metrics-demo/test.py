from typing import List
from cicadad.core.engine import Engine
from cicadad.core.types import Result
from cicadad.core.decorators import (
    scenario,
    metrics_collector,
    console_metric_displays,
    load_model,
    user_loop,
)
from cicadad.core.scenario import n_seconds, while_alive
from cicadad.metrics.console import (
    console_collector,
    console_stats,
    console_percent,
)
import requests
import uuid

engine = Engine()


def runtime_ms(latest_results: List[Result]):
    return [result.output * 1000 for result in latest_results]


@scenario(engine)
@load_model(n_seconds(180, 30))
@user_loop(while_alive())
@metrics_collector(console_collector("ms", runtime_ms))
@console_metric_displays(
    {
        "latency_stats": console_stats("ms"),
        "latency_above_30ms": console_percent("ms", 30),
    }
)
def post_user(context):
    response = requests.post(
        # url="http://demo-api:8080/users",
        url="http://localhost:8080/users",
        json={
            "name": "jeremy",
            "age": 23,
            "email": f"{str(uuid.uuid4())[:8]}@gmail.com",
        },
    )

    return response.elapsed.total_seconds()


if __name__ == "__main__":
    engine.start()
