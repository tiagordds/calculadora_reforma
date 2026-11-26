import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.http import QueryDict

from parameters.catalog import unique_keys
from simulation.services import simulate_services
from web.services import ServicesForm, flatten_history


class Command(BaseCommand):
    help = "Reproduz a memória JSON da simulação de serviços, inclusive resultados parciais."

    def add_arguments(self, parser):
        parser.add_argument("file", type=Path)

    def handle(self, file, **options):
        try:
            with file.open("rb") as source:
                raw = source.read(131073)
            if len(raw) > 131072:
                raise ValueError
            saved = json.loads(raw, object_pairs_hook=unique_keys)
            fields = flatten_history(saved["inputs"])
            for key in ("period", "opening"):
                if not fields[key].endswith("-01"):
                    raise ValueError
                fields[key] = fields[key][:7]
            post = QueryDict(mutable=True)
            for key, value in fields.items():
                post[key] = "" if value is None else value
            form = ServicesForm(post)
            if not form.is_valid():
                raise ValueError
            replay = json.loads(json.dumps(simulate_services(form.scenario()), default=str))
            if saved != replay:
                raise CommandError("A memória divergiu. Confira os dados e a revisão do cálculo.")
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
            raise CommandError("Memória de serviços inválida ou incompatível.") from exc
        self.stdout.write("Memória de serviços reproduzida integralmente.")
