import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from parameters.catalog import unique_keys
from simulation.service_comparison import compare_services
from web.service_comparison import ServiceComparisonForm, replay_post


class Command(BaseCommand):
    help = "Reproduz as duas trajetórias do C08 com os históricos e parâmetros registrados."

    def add_arguments(self, parser):
        parser.add_argument("file", type=Path)

    def handle(self, file, **options):
        try:
            with file.open("rb") as stream:
                raw = stream.read(131073)
            if len(raw) > 131072:
                raise ValueError
            saved = json.loads(raw, object_pairs_hook=unique_keys)
            form = ServiceComparisonForm(replay_post(saved["inputs"]))
            if not form.is_valid():
                raise ValueError
            repeated = json.loads(json.dumps(compare_services(form.scenario()), default=str))
            if repeated != saved:
                raise CommandError("Divergência na memória comparativa do C08.")
        except (ValueError, OSError, TypeError, KeyError, AttributeError) as exc:
            raise CommandError("Memória comparativa inválida.") from exc
        self.stdout.write("Comparação de serviços reproduzida integralmente.")
