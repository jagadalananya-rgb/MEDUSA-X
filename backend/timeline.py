from datetime import datetime


def build_timeline(records):

    timeline = []

    for record in records:

        try:
            date = datetime.strptime(
                record["date"], "%Y-%m-%d"
            )

            timeline.append({
                "date": date,
                "event": record["event"],
                "document": record["document"]
            })

        except (ValueError, KeyError):
            continue

    timeline.sort(key=lambda item: item["date"])

    return timeline