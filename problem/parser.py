from .data_models import Variable, Label, Rule, Example, RepresentativeSet

def build_problem(mf_defs, rule_defs, rep_defs):
    variables = {}
    for var_name, labels in mf_defs.items():
        lbl_objs = {name: Label(name, d['type'], d['params']) for name, d in labels.items()}
        variables[var_name] = Variable(var_name, lbl_objs)

    rules = []
    for r in rule_defs:
        rules.append(Rule(r['if'], r['then']))

    examples = []
    for ex in rep_defs['examples']:
        examples.append(Example(ex['id'], ex['inputs'], ex['decision']))

    rep_set = RepresentativeSet(rep_defs['output_values'], examples)

    return (variables, rules, rep_set)