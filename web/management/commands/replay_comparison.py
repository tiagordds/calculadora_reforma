import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.http import QueryDict

from parameters.catalog import unique_keys
from parameters.comparison import REVISION
from simulation.comparison import compare
from web.comparison_form import ComparisonForm


class Command(BaseCommand):
    help = "Reproduz uma memória comparativa local com a edição registrada."

    def add_arguments(self, parser):
        parser.add_argument("file", type=Path)

    def handle(self, file, **options):
        try:
            with file.open("rb") as stream:
                raw = stream.read(131073)
            if len(raw) > 131072:
                raise ValueError
            saved = json.loads(raw, object_pairs_hook=unique_keys)
            if saved["revision"] != REVISION:
                raise CommandError("Restaure a edição do software registrada na memória.")
            inputs = dict(saved["inputs"])
            post = QueryDict(mutable=True)
            for group, prefix in (("history", "month_"), ("hybrid_history", "hybrid_")):
                for month, value in inputs.pop(group).items():
                    post[prefix+month] = "" if value is None else value
            for key, value in inputs.items():
                if value is not None and key in ("opening", "period", "event_month"):
                    if not value.endswith("-01"):
                        raise ValueError
                    value = value[:7]
                if isinstance(value, bool):
                    value = "on" if value else ""
                post[key] = "" if value is None else value
            form = ComparisonForm(post)
            if not form.is_valid():
                raise ValueError
            repeated = json.loads(json.dumps(compare(form.scenario()), default=str))
            for record in (repeated, saved):
                del record["processed_at"]
            if repeated != saved:
                raise CommandError("Divergência na memória. Confira as revisões e os valores.")
        except (OSError, ValueError, KeyError, AttributeError, TypeError) as exc:
            raise CommandError("Memória inválida ou edição incompatível.") from exc
        self.stdout.write(f"Memória comparativa reproduzida integralmente com {REVISION}.")
