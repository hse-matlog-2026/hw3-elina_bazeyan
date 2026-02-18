# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/operators.py

"""Syntactic conversion of propositional formulas to use only specific sets of
operators."""

from propositions.syntax import *
from propositions.semantics import *

def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'``, ``'&'``, and ``'|'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'``, ``'&'``, and
        ``'|'``.
    """

    return formula.substitute_operators({
        'T':Formula.parse('(p|~p)'),
        'F':Formula.parse('(p&~p)'),
        '->':Formula.parse('(~p|q)'),
        '+':Formula.parse('((p&~q)|(~p&q))'),
        '<->':Formula.parse('((p&q)|(~p&~q))'),
        '-&':Formula.parse('~(p&q)'),
        '-|':Formula.parse('~(p|q)')
        })

    # Task 3.5

def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'`` and ``'&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'`` and ``'&'``.
    """

    f = to_not_and_or(formula)
    return f.substitute_operators({
        '|':Formula.parse('~(~p&~q)')
        })

    # Task 3.6a

def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'-&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'-&'``.
    """

    f = to_not_and(formula)
    
    def recurse(g:Formula) -> Formula:
        if is_variable(g.root):
            return g
        if is_unary(g.root):
            a = recurse(g.first)
            return Formula('-&', a, a)
        assert g.root == '&'
        a = recurse(g.first)
        b = recurse(g.second)
        nand_ab = Formula('-&', a, b)
        return Formula('-&', nand_ab, nand_ab)

    return recurse(f)

    # Task 3.6b

def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'~'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'~'``.
    """

    f = to_not_and_or(formula)
    return f.substitute_operators({
        '|':Formula.parse('(~p->q)'),
        '&':Formula.parse('~(p->~q)'),
        'T':Formula.parse('(p->p)'),
        'F':Formula.parse('~(p->p)')
        })

    # Task 3.6c

def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'F'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'F'``.
    """

    f = to_implies_not(formula)

    def recurse(g:Formula) -> Formula:
        if is_variable(g.root):
            return g
        if is_constant(g.root):
            if g.root == 'F':
                return g
            return Formula('->', Formula('F'), Formula('F'))
        if is_unary(g.root):
            return Formula('->', recurse(g.first), Formula('F'))
        assert g.root == '->'
        return Formula('->', recurse(g.first), recurse(g.second))

    return recurse(f)

    # Task 3.6d
