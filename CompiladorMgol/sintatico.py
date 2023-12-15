import pandas as pd


def parse(self, string):
    log = logging.getLogger("yacv")

    if string[-1] != "$":
        string.append("$")
    stack = [0]
    while True:
        top = stack[-1]
        a = string[0]
        entry = self.parsing_table.at[top, (YACV_ACTION, a)]
        if entry == YACV_ERROR:
            log.error("Parse error")
            raise YACVError("YACV_ERROR entry for top = {}, a = {}".format(top, a))
        if isinstance(entry, list):
            entry = entry[0]
        log.debug("stack top = {}, a = {}, entry = {}".format(top, a, entry))
        if entry[0] == "s":
            stack.append(AbstractSyntaxTree(a))
            stack.append(int(entry[1:]))
            string.pop(0)
        elif entry[0] == "r":
            prod_id = int(entry[1:])
            prod = self.grammar.prods[prod_id]
            new_tree = AbstractSyntaxTree(prod.lhs)
            new_tree.prod_id = prod_id
            popped_list = []
            if prod.rhs[0] != YACV_EPSILON:
                for _ in range(len(prod.rhs)):
                    if not stack:
                        raise YACVError("Stack prematurely empty")
                    stack.pop(-1)  # pops the state number
                    if not stack:
                        raise YACVError("Stack prematurely empty")
                    popped_list.append(stack.pop(-1))  # pops the symbol
            else:
                new_tree.desc.append(AbstractSyntaxTree(YACV_EPSILON))
            for i in range(len(popped_list) - 1, -1, -1):
                new_tree.desc.append(popped_list[i])
            new_top = stack[-1]
            nonterminal = prod.lhs
            new_state = self.parsing_table.at[new_top, (YACV_GOTO, nonterminal)]
            stack.append(new_tree)
            if isinstance(new_state, list):
                new_state = new_state[0]
            stack.append(int(new_state))
        elif entry == YACV_ACCEPT:
            prod = self.grammar.prods[0]
            assert prod.rhs[-1] == "$" and len(prod.rhs) == 2
            if not stack:
                raise ValueError()  # TODO: Convert this to YACVError stating an error has occurred due to stack becoming empty prematurely
            stack.pop(-1)
            if not stack:
                raise ValueError()  # TODO: Convert this to YACVError stating an error has occurred due to stack becoming empty prematurely
            tree = stack.pop(-1)
            log.info("Parse successful")
            log.debug("Final tree = {}".format(tree))
            return tree
            break
        else:
            raise YACVError("Unknown error while parsing")
            break
