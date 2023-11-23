import random

from django.http import HttpRequest


def get_interesting_fact(request: HttpRequest) -> dict:
    with open("crewing/data_for_footer.json", "r") as f:
        history_data = f.read().split("\n")

    history = random.choice(history_data)
    return {"history": history}
