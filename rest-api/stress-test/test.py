from typing import Any, List
import requests
import uuid
import statistics

from cicadad.metrics.console import (
    console_collector,
    console_count,
    console_latest,
    console_stats,
    console_percent,
)
from cicadad.core.decorators import (
    console_metric_displays,
    metrics_collector,
    scenario,
    load_model,
    user_loop,
    result_aggregator,
)
from cicadad.core.types import Result
from cicadad.core.engine import Engine
from cicadad.core.scenario import (
    ramp_users_to_threshold,
    while_alive,
)

# DEMO_API_ENDPOINT = "http://172.17.0.1:8080"
DEMO_API_ENDPOINT = "http://demo-api:8080"

engine = Engine()


def runtime_aggregator(previous_aggregate: Any, latest_results: List[Result]):
    # FEATURE: more built in functions to accomplish this functionality
    return {
        "avg_runtime": 0
        if len(latest_results) < 5
        else statistics.mean(result.time_taken for result in latest_results)
    }


def runtime_ms(latest_results: List[Result]):
    return [result.time_taken * 1000 for result in latest_results]


def pass_or_fail(latest_results: List[Result]):
    return [0 if result.exception is not None else 1 for result in latest_results]


def requests_per_second(latest_results: List[Result]):
    if len(latest_results) < 5:
        return []

    min_timestamp = latest_results[0].timestamp
    max_timestamp = latest_results[0].timestamp

    for result in latest_results:
        if result.timestamp < min_timestamp:
            min_timestamp = result.timestamp

        if result.timestamp > max_timestamp:
            max_timestamp = result.timestamp

    seconds = (max_timestamp - min_timestamp).total_seconds()

    return [len(latest_results) // seconds]


@scenario(engine)
@load_model(
    ramp_users_to_threshold(
        initial_users=10,
        threshold_fn=lambda agg: agg is not None and agg["avg_runtime"] > 0.075,
        next_users_fn=lambda n: n + 5,
    )
)
@user_loop(while_alive())
@result_aggregator(runtime_aggregator)
@metrics_collector(console_collector("ms", runtime_ms))
@metrics_collector(console_collector("pass_or_fail", pass_or_fail))
@metrics_collector(console_collector("rps", requests_per_second))
@console_metric_displays(
    {
        "runtime_stats": console_stats("ms"),
        "rps": console_stats("rps"),
        "latest_rps": console_latest("rps"),
        "success_rate": console_percent("pass_or_fail", 0),
    }
)
def post_user(context):
    requests.post(
        url=f"{DEMO_API_ENDPOINT}/users",
        json={
            "name": "jeremy",
            "age": 23,
            "email": f"{str(uuid.uuid4())[:8]}@gmail.com",
        },
    )


if __name__ == "__main__":
    engine.start()
