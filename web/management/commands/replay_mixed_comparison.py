from simulation.mixed_comparison import compare_mixed
from web.management.commands.replay_service_comparison import Command as ComparisonReplay
from web.mixed_comparison import MixedComparisonForm, replay_post


class Command(ComparisonReplay):
    help = "Reproduz a comparação empresarial C09 de março de 2027."
    form_class = MixedComparisonForm
    restore = staticmethod(replay_post)
    simulate = staticmethod(compare_mixed)
    case = "C09"
    max_bytes = 2 * 1024 * 1024
    success = "Comparação de atividades mistas reproduzida integralmente."
