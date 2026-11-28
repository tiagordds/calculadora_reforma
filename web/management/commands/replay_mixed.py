from simulation.mixed import simulate_mixed
from web.management.commands.replay_services import Command as ServicesReplay
from web.mixed import MixedForm


class Command(ServicesReplay):
    help = "Reproduz a memória do DAS tradicional de comércio e serviços no mesmo CNPJ."
    form_class = MixedForm
    simulate = staticmethod(simulate_mixed)
    description = "de atividades mistas"
