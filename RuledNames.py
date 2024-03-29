import random
from typing import Union
from dataclasses import dataclass

OPTIONAL_REJECT_PROB = 0.5


class RuleSeq:
    """
    Sequence of `Rule`/`RuleSeq`, concatenated

    `list` is treated as `Rule`(Necessary) by default, use RuleSeq() to indicate a `RuleSeq`.
    """

    def __init__(self, *seq):
        self.seq = []
        for rule in seq:
            if type(rule) in [str, list]:
                self.seq.append(N(rule))
            elif type(rule) in [RuleSeq, Rule]:
                self.seq.append(rule)
            else:
                raise TypeError(
                    f"Elements of `seq` in RuleSeq should be str, list, RuleSeq or Rule, but got {type(rule)}")

    def __str__(self):
        res = ""
        for rule in self.seq:
            res += str(rule)
        return res

    def __add__(self, rseq):
        if type(rseq) in [str, list]:
            return RuleSeq(*self.seq, N(rseq))
        elif isinstance(rseq, Rule):
            return RuleSeq(*self.seq, rseq)
        elif isinstance(rseq, RuleSeq):
            return RuleSeq(*self.seq, *rseq)
        else:
            raise TypeError(f"Cannot add RuleSeq to {type(rseq)}")


@dataclass
class Rule:
    rule: Union[str, list]
    optional: bool = False

    def __str__(self):
        if self.optional:
            if random.random() < OPTIONAL_REJECT_PROB:
                return ""

        if isinstance(self.rule, str):
            return self.rule

        selections = []
        for sub_rule in self.rule:
            selections.append(str(sub_rule))
        return random.choice(selections)

    def __add__(self, r):
        return RuleSeq(self, r)


def O(selection):
    """
    Optional rule
    """
    return Rule(selection, True)    


def N(selection):
    """
    Necessary rule
    """
    return Rule(selection, False)


class NameGen:
    def __init__(self, rules, dict_):
        self.rules = rules
        self.dict_ = dict_

    def gen(self):
        return str(random.choice(self.rules)).format(**self.dict_)
