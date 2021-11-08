from datetime import datetime
import requests
import uuid
import statistics

from cicadad.metrics.console import (
    console_collector,
    console_count,
    console_latest,
    console_stats,
)
from cicadad.core.decorators import (
    console_metric_displays,
    metrics_collector,
    scenario,
    load_model,
    user_loop,
    result_aggregator,
)
from cicadad.core.engine import Engine
from cicadad.core.scenario import (
    ramp_users_to_threshold,
    while_alive,
)

# DEMO_API_ENDPOINT = "http://172.17.0.1:8080"
DEMO_API_ENDPOINT = "http://demo-api:8080"

engine = Engine()


def runtime_aggregator(previous_aggregate, latest_results):
    if previous_aggregate is None:
        num_results = 0
        mean_ms = 0
    else:
        num_results = previous_aggregate["num_results"]
        mean_ms = previous_aggregate["mean_ms"]

    # FEATURE: more built in functions to accomplish this functionality
    runtimes = []

    for result in latest_results:
        if result.exception is None:
            runtimes.append(result.output)

    if runtimes != []:
        latest_num_results = len(runtimes)
        latest_mean_ms = statistics.mean(runtimes)

        new_num_results = num_results + latest_num_results
        new_mean = ((mean_ms * num_results) + (latest_mean_ms * latest_num_results)) / (
            num_results + latest_num_results
        )
    else:
        new_num_results = num_results
        new_mean = mean_ms

    return {
        "num_results": new_num_results,
        "mean_ms": new_mean,
    }


def extract_ms(latest_results):
    return [
        float(result.output) for result in latest_results if result.exception is None
    ]


@scenario(engine)
@load_model(
    ramp_users_to_threshold(
        initial_users=10,
        threshold_fn=lambda agg: agg is not None and agg["mean_ms"] > 75,
        next_users_fn=lambda n: n + 5,
    )
)
@user_loop(while_alive())
@result_aggregator(runtime_aggregator)
@metrics_collector(console_collector("stats", extract_ms))
@metrics_collector(console_collector("latest", extract_ms))
@metrics_collector(console_collector("count", extract_ms))
@console_metric_displays(
    {
        "stats": console_stats(),
        "latest": console_latest(),
        "count": console_count(),
    }
)
def post_user(context):
    start = datetime.now()

    requests.post(
        url=f"{DEMO_API_ENDPOINT}/users",
        json={
            "name": "jeremy",
            "age": 23,
            "email": f"{str(uuid.uuid4())[:8]}@gmail.com",
        },
    )

    end = datetime.now()

    return ((end - start).seconds + (end - start).microseconds / 1000000) * 1000


if __name__ == "__main__":
    engine.start()
