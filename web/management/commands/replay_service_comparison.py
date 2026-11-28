import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from parameters.catalog import unique_keys
from simulation.service_comparison import compare_services
from web.service_comparison import ServiceComparisonForm, replay_post


class Command(BaseCommand):
    help = "Reproduz as duas trajetórias do C08 com os históricos e parâmetros registrados."
    form_class = ServiceComparisonForm
    restore = staticmethod(replay_post)
    simulate = staticmethod(compare_services)
    case = "C08"
    success = "Comparação de serviços reproduzida integralmente."
    max_bytes = 131072

    def add_arguments(self, parser):
        parser.add_argument("file", type=Path)

    def handle(self, file, **options):
        try:
            with file.open("rb") as stream:
                raw = stream.read(self.max_bytes + 1)
            if len(raw) > self.max_bytes:
                raise ValueError
            saved = json.loads(raw, object_pairs_hook=unique_keys)
            form = self.form_class(self.restore(saved["inputs"]))
            if not form.is_valid():
                raise ValueError
            repeated = json.loads(json.dumps(self.simulate(form.scenario()), default=str))
            if repeated != saved:
                raise CommandError(f"Divergência na memória comparativa do {self.case}.")
        except (ValueError, OSError, TypeError, KeyError, AttributeError) as exc:
            raise CommandError("Memória comparativa inválida.") from exc
        self.stdout.write(self.success)
