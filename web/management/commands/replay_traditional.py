import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.http import QueryDict

from parameters.catalog import DIGESTS, unique_keys
from simulation.traditional import simulate
from web.traditional_form import TraditionalForm


class Command(BaseCommand):
    help = "Confere localmente a memória JSON copiada da apuração tradicional."

    def add_arguments(self, parser):
        parser.add_argument("file", type=Path)

    def handle(self, file, **options):
        try:
            with file.open("rb") as stream:
                raw = stream.read(131073)
            if len(raw) > 131072:
                raise ValueError
            saved = json.loads(raw, object_pairs_hook=unique_keys)
            revision = saved["catalog_revision"]
            inputs = dict(saved["inputs"])
            if revision not in DIGESTS or inputs["edition"] != revision:
                raise ValueError
            months = inputs.pop("history")
            form_data = QueryDict(mutable=True)
            for key in ("period", "opening"):
                if not inputs[key].endswith("-01"):
                    raise ValueError
                inputs[key] = inputs[key][:7]
            for key in ("accept_history", "accept_period"):
                if type(inputs[key]) is not bool:
                    raise ValueError
                inputs[key] = "yes" if inputs[key] else ""
            inputs.update({"month_" + m: value for m, value in months.items()})
            for key, value in inputs.items():
                form_data[key] = "" if value is None else value
            form = TraditionalForm(form_data)
            # The local replay can explicitly use an archived edition. HTTP accepts only ACTIVE.
            form.fields["edition"].choices = [(revision, revision)]
            if not form.is_valid():
                raise ValueError
            repeated = json.loads(json.dumps(simulate(form.scenario(), revision), default=str))
            for record in (saved, repeated):
                del record["processed_at"]
            if saved != repeated:
                raise CommandError("Divergência na memória. Confira as entradas e restaure as revisões registradas.")
        except (AttributeError, KeyError, TypeError, ValueError, OSError) as exc:
            raise CommandError("Memória inválida ou revisão indisponível para reprodução.") from exc
        self.stdout.write("Memória reproduzida integralmente com a revisão " + revision + ".")
