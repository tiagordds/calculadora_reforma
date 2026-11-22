import re
from datetime import date
from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from parameters.comparison import REVISION
from .traditional_form import AmountField, TraditionalForm, choice


def flag(label):
    return forms.BooleanField(required=False, label=label, widget=forms.CheckboxInput())


class RateField(forms.CharField):
    def clean(self, value):
        raw = super().clean(value)
        if not raw:
            return None
        if not re.fullmatch(r"[0-9]{1,3}(?:[.,][0-9]{1,6})?", raw):
            raise ValidationError("Informe um percentual entre 0 e 100, com até seis casas.")
        rate = Decimal(raw.replace(",", "."))
        if rate > 100:
            raise ValidationError("O percentual deve ficar entre 0 e 100.")
        return rate


def day(label, **kwargs):
    return forms.DateField(label=label, required=False, input_formats=["%Y-%m-%d"],
                           widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}), **kwargs)


class ComparisonForm(TraditionalForm):
    accept_period = None
    edition = forms.ChoiceField(choices=[(REVISION, REVISION)], initial=REVISION, widget=forms.HiddenInput)
    standing = choice("Situação da empresa no Simples", [
        ("unknown", "Não sei confirmar"), ("member", "Optante, segundo a empresa"),
        ("impediment", "Impedimento vigente")], "unknown")
    revenue = AmountField(label="Preço final de todas as vendas de março (R$)")
    quantity = forms.IntegerField(label="Quantidade de canetas nas mesmas vendas, se conhecida",
                                  min_value=0, max_value=10**12, required=False)
    history_basis = choice("Histórico fiscal do híbrido", [
        ("unknown", "Ainda não sei"), ("shared", "Aceito as mesmas doze receitas fiscais iniciais"),
        ("estimated", "Estimar por outra média mensal"), ("real", "Informar os doze meses próprios")], "unknown")
    hybrid_income = AmountField(label="Média mensal fiscal do híbrido (R$)")
    hybrid_prior_year = AmountField(label="Receita fiscal em 2026 no híbrido (R$)")
    hybrid_year_to_date = AmountField(label="Receita fiscal de janeiro a março de 2027 no híbrido (R$)")
    cbs_rate = RateField(label="CBS escolhida para simular as vendas (%)", required=False, max_length=10)
    accept_cbs = flag("Aceito esta taxa como hipótese da simulação.")
    exclusions = AmountField(label="Outras exclusões legais incluídas no preço (R$)")
    exclusion_origin = choice("Origem das exclusões", [("unknown", "Não conheço a composição"),
        ("document", "Total identificado nos documentos"), ("assumed", "Aceito o total como hipótese")], "unknown")
    purchases = AmountField(label="Total pago pelas compras (R$)")
    purchase_base = AmountField(label="Base tributável identificada nas compras (R$)")
    eligible_base = AmountField(label="Parte da base com requisitos atendidos (R$)")
    supplier = choice("Origem das aquisições", [("unknown", "Não sei ou há tratamentos mistos"),
        ("regular", "Fornecedor no regime regular"), ("simples", "Fornecedor do Simples tradicional"),
        ("exempt", "Operação desonerada sem crédito presumido")], "unknown")
    credit_rule = choice("Fundamento para os créditos informados", [
        ("unknown", "Não sei confirmar"), ("extinction", "Extinção do débito conforme art. 47"),
        ("exception", "Art. 48: nenhuma das duas modalidades implantada e destaque correto"),
        ("declared", "Apropriação já conferida e declarada para o período")], "unknown")
    credit_evidence = flag("Confirmo documento idôneo, destinação empresarial e valor elegível por tributo, ou aceito essas condições como hipótese indicada abaixo.")
    credit_origin = choice("Origem dos valores de crédito", [("unknown", "Não informada"),
        ("declared", "Documentos ou apuração declarada"), ("assumed", "Aceito como hipótese")], "unknown")
    event_month = forms.RegexField(label="Mês em que se completaram os requisitos de apropriação",
        regex=r"^(19|20)[0-9]{2}-(0[1-9]|1[0-2])$", required=False,
        widget=forms.TextInput(attrs={"type": "month"}))
    account_scope = flag("Confirmo que estes dados abrangem a conta do mês, sem débitos prioritários, ajustes de débito, transferências ou pedidos de ressarcimento.")
    zero_movements = flag("Assumir saldo anterior, ajustes, estornos e outras extinções iguais a zero nas duas contas.")
    option_status = choice("Situação da opção conjunta de IBS e CBS",
        [("unknown", "Não sei confirmar"), ("absent", "Sem opção"), ("requested", "Pedido realizado"),
         ("active", "Vigente conforme recibo e situação declarados"),
         ("assumed", "Explorar hipótese de opção tempestiva, sem recibo")], "unknown")
    option_date = day("Data do pedido original")
    cancel_date = day("Data de cancelamento, se houve")
    decision_date = day("Data em que se avalia uma nova opção", initial="2027-03-01")
    refund = choice("Recebeu ressarcimento de IBS/CBS no ano corrente ou anterior?",
                    [("unknown", "Não sei"), ("yes", "Sim"), ("no", "Não")], "unknown")
    buyer = choice("Perfil dos clientes dessas vendas", [("unknown", "Desconhecido ou misto"),
        ("consumer", "Consumidor final"), ("regular", "Adquirente no regime regular"),
        ("simples", "Adquirente no Simples tradicional")], "unknown")
    buyer_document = flag("Valores transferíveis individualizados nos documentos de venda, para aquisição empresarial elegível.")
    example_origin = forms.ChoiceField(required=False, choices=[(x, x) for x in ("zero", "middle", "high")],
                                       widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["period"].widget = forms.HiddenInput()
        self.fields["period"].initial = "2027-03"
        self.fields["revenue"].required = True
        self.fields["mode"].initial = "estimated"
        self.fields["mode"].label = "Origem do histórico tradicional"
        self.fields["decision_date"].required = True
        self.fields["accept_history"] = flag("Aceito estimar os doze meses do tradicional pela média.")
        for month in self.months:
            self.fields["hybrid_" + month] = AmountField(label=f"{month[5:]}/{month[:4]} no híbrido (R$)")
        for tax in ("cbs", "ibs"):
            for key, label in (("potential", "Crédito potencial identificado no conjunto das compras"),
                               ("credit", "Valor elegível do destaque do fornecedor regular"),
                               ("transfer", "Crédito transferível no documento de fornecedor do Simples"),
                               ("opening", "Saldo credor anterior"), ("adjustment", "Ajustes credores"),
                               ("reversal", "Estornos"), ("extinguished", "Outras extinções já realizadas")):
                self.fields[tax + "_" + key] = AmountField(label=f"{label} de {tax.upper()} (R$)")
            for seller, label in (("traditional", "tradicional"), ("hybrid", "híbrido")):
                self.fields[f"buyer_{seller}_{tax}"] = AmountField(label=f"{tax.upper()} transferível ao cliente pelo {label} (R$)")

    def clean(self):
        data = super().clean()
        if data.get("quantity") == 0 and data.get("revenue"):
            self.add_error("quantity", "As vendas com preço positivo exigem quantidade positiva ou desconhecida.")
        for key, field in self.fields.items():
            if isinstance(field, forms.BooleanField) and self.data.get(key) not in (None, "", "on"):
                self.add_error(key, "Confirmação inválida.")
        for part, total in (("exclusions", "revenue"), ("eligible_base", "purchase_base"),
                            ("purchase_base", "purchases")):
            if None not in (data.get(part), data.get(total)) and data[part] > data[total]:
                self.add_error(part, "A parcela informada supera o total correspondente.")
        if data.get("option_date") and data.get("cancel_date") and data["cancel_date"] < data["option_date"]:
            self.add_error("cancel_date", "O cancelamento antecede o pedido.")
        if data.get("event_month") and data.get("period") and data["event_month"] < data["period"].strftime("%Y-%m"):
            self.add_error("event_month", "A apropriação não pode anteceder as compras do mês.")
        if data.get("option_status") == "absent" and data.get("option_date") and not data.get("cancel_date"):
            self.add_error("option_status", "Informe o estado do pedido ou seu cancelamento.")
        if data.get("cancel_date") and not data.get("option_date"):
            self.add_error("option_date", "Informe o pedido correspondente ao cancelamento.")
        if data.get("zero_movements") and any(data.get(t + "_" + k) for t in ("ibs", "cbs")
                for k in ("opening", "adjustment", "reversal", "extinguished")):
            self.add_error("zero_movements", "Há movimentos diferentes de zero. Desmarque esta hipótese.")
        if data.get("history_basis") != "real" and any(data.get("hybrid_"+m) is not None for m in self.months):
            self.add_error("history_basis", "Selecione os doze meses próprios para usar o histórico preenchido.")
        if data.get("history_basis") != "estimated" and data.get("hybrid_income") is not None:
            self.add_error("hybrid_income", "Selecione a estimativa por outra média.")
        if data.get("supplier") == "exempt" and any(data.get(t+"_"+k) for t in ("ibs", "cbs")
                                                    for k in ("potential", "credit", "transfer")):
            self.add_error("supplier", "Há crédito positivo em operação declarada desonerada sem exceção.")
        for tax in ("ibs", "cbs"):
            key = tax + ("_transfer" if data.get("supplier") == "simples" else "_credit")
            amount, potential = data.get(key), data.get(tax+"_potential")
            if None not in (amount, potential) and amount > potential:
                self.add_error(key, "O crédito elegível supera o potencial informado para estas compras.")
        if any(data.get(k) == 0 for k in ("purchases", "purchase_base", "eligible_base")) and any(
                data.get(t+"_"+k) for t in ("ibs", "cbs") for k in ("credit", "transfer")):
            self.add_error("eligible_base", "Confira o crédito positivo diante das compras ou da base informadas como zero.")
        return data

    def scenario(self):
        data = self.cleaned_data.copy()
        data["history"] = {m: data.pop("month_" + m) for m in self.months}
        data["hybrid_history"] = {m: data.pop("hybrid_" + m) for m in self.months}
        month = data["event_month"]
        data["event_month"] = date.fromisoformat(month + "-01") if month else None
        return data
