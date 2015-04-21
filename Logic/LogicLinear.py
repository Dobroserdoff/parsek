# -*- coding: UTF-8 -*-


def main():
    equation = str(raw_input('Please input an equation '))
    variables = var_count(equation)
    str_var = ''
    result_html = []
    for i in variables[2:]:
        str_var += i + ' '
        result_html.append(i)
    result = str_var + equation + '\n'
    result_html.append(equation)
    result_html.append('$')
    all_values = values_change(variables[2:])
    for values in all_values:
        values = ['0', '1'] + values
        final_value = brackets(equation, variables, values)
        result += out_print(final_value, values)
        for i in out_print(final_value, values).split():
            result_html.append(i)
        result_html.append('$')
    create_html(result_html)
    print result


def create_html(inf):
    out = open('logicLinearOutput.html', 'w')
    output = '<!DOCTYPE html>' + '\n' + '<html>' + '\n' + '<head lang="en">' + '\n'
    output += '\t' + '<meta charset="UTF-8">' + '\n'+ '\t' + '<title>Logix</title>' + '\n' + '</head>' + '\n'
    output += '<body>' + '\n' + '\t' + '<h1 align="center">Table Of Results</h1>' + '\n'
    output += '\t\t' + '<table width="500" cellspacing="5" cellpadding="15" border="3" align="center">' + '\n'
    output += '\t\t\t' + '<tr>' + '\n'
    for i in range(len(inf)):
        if inf[i] != '$':
            output += '\t\t\t\t' + '<td align="center">' + inf[i] + '</td>' + '\n'
        elif i+1 == len(inf):
            output += '\t\t\t' + '</tr>' + '\n'
        else:
            output += '\t\t\t' + '</tr>' + '\n' + '\t\t\t' + '<tr>' + '\n'
    output += '\t\t' + '</table>' + '\n' + '</body>' + '\n' + '</html>'
    out.write(output)


def values_change(variables):
    if len(variables) == 1:
        return [['0'], ['1']]
    else:
        result = []
        short_items = values_change(variables[:-1])
        for short_item in short_items:  # ['1', '0']
            long_item_1 = short_item + ['0']  # ['1', '0'] + ['0'] = ['1', '0', '0']
            long_item_2 = short_item + ['1']  # ['1', '0'] + ['1'] = ['1', '0', '1']
            result.append(long_item_1)
            result.append(long_item_2)
        return result


def out_print(final_value, values):
    str_out = ''
    for j in values[2:]:
        str_out += j + ' '
    result = str_out + final_value + '\n'
    return result


def var_count(equation):
    variables = ['0', '1']
    elements = equation.split()
    for i in elements:
        i = i.replace('(', '')
        i = i.replace(')', '')
        if len(i) == 1 and i not in variables:
            variables.append(i)
        elif len(i) == 2 and i[0] == '(' and i[1] not in variables:
            variables.append(i[1])
        elif len(i) == 2 and i[1] == ')'and i[0] not in variables:
            variables.append(i[0])
    return variables


def brackets(equation, variables, values):
    limit_expression = lowest_brackets(equation, variables, values, counter=0)
    limit = limit_expression[0]
    expression = limit_expression[1]
    while limit > 0:
        result = lowest_brackets(expression, variables, values, 0)
        limit = result[0]
        expression = result[1]
    return expression


def lowest_brackets(equation, variables, values, counter):
    pair_brackets = [0, 0]
    if '(' in equation:
        for i in range(len(equation)):
            if equation[i] == '(':
                pair_brackets[0] = i
                counter += 1
            elif equation[i] == ')':
                pair_brackets[1] = i
                final = lowest_brackets(equation[pair_brackets[0]+1:pair_brackets[1]], variables, values, counter)
                if equation[pair_brackets[0]-4:pair_brackets[0]-1] == 'not':
                    if final[1] == '0':
                        new_eq = equation[:pair_brackets[0]-4] + '1' + equation[pair_brackets[1]+1:]
                    else:
                        new_eq = equation[:pair_brackets[0]-4] + '0' + equation[pair_brackets[1]+1:]
                else:
                    new_eq = equation[:pair_brackets[0]] + final[1] + equation[pair_brackets[1]+1:]
                final[1] = new_eq
                return final
    else:
        result = [counter, all_operators(equation, variables, values)]
        return result


def all_operators(equation, variables, values):
    and_result = and_operator(equation, variables, values)
    or_result = or_operator(and_result, variables, values)
    then_result = then_operator(or_result, variables, values)
    final = equal_operator(then_result, variables, values)
    return final


def and_operator(equation, variables, values):
    if 'and' in equation:
        if equation[equation.find('and')-6:equation.find('and')-3] == 'not':
            exp1 = equation[equation.find('and')-6:equation.find('and')-1]
            start_point = equation.find('and')-6
        else:
            exp1 = equation[equation.find('and')-2:equation.find('and')-1]
            start_point = equation.find('and')-2
        if equation[equation.find('and')+4:equation.find('and')+7] == 'not':
            exp2 = equation[equation.find('and')+4:equation.find('and')+9]
            finish_point = equation.find('and')+9
        else:
            exp2 = equation[equation.find('and')+4:equation.find('and')+5]
            finish_point = equation.find('and')+5
        exp1_position = variables.index(exp1[-1])
        exp2_position = variables.index(exp2[-1])
        if 'not' in exp1:
            if values[exp1_position] == '1':
                first = '0'
            else:
                first = '1'
        else:
            first = values[exp1_position]
        if 'not' in exp2:
            if values[exp2_position] == '1':
                second = '0'
            else:
                second = '1'
        else:
            second = values[exp2_position]
        if first == '1' and second == '1':
            value = '1'
        else:
            value = '0'
        result = equation[:start_point] + value + equation[finish_point:]
        final = and_operator(result, variables, values)
        return final
    else:
        return equation


def or_operator(and_result, variables, values):
    if 'or' in and_result:
        if and_result[and_result.find('or')-6:and_result.find('or')-3] == 'not':
            exp1 = and_result[and_result.find('or')-6:and_result.find('or')-1]
            start_point = and_result.find('or')-6
        else:
            exp1 = and_result[and_result.find('or')-2:and_result.find('or')-1]
            start_point = and_result.find('or')-2
        if and_result[and_result.find('or')+3:and_result.find('or')+6] == 'not':
            exp2 = and_result[and_result.find('or')+3:and_result.find('or')+8]
            finish_point = and_result.find('or')+8
        else:
            exp2 = and_result[and_result.find('or')+3:and_result.find('or')+4]
            finish_point = and_result.find('or')+4
        exp1_position = variables.index(exp1[-1])
        exp2_position = variables.index(exp2[-1])
        if 'not' in exp1:
            if values[exp1_position] == '1':
                first = '0'
            else:
                first = '1'
        else:
            first = values[exp1_position]
        if 'not' in exp2:
            if values[exp2_position] == '1':
                second = '0'
            else:
                second = '1'
        else:
            second = values[exp2_position]
        if first == '0' and second == '0':
            value = '0'
        else:
            value = '1'
        result = and_result[:start_point] + value + and_result[finish_point:]
        final = or_operator(result, variables, values)
        return final
    else:
        return and_result


def then_operator(or_result, variables, values):
    if 'then' in or_result:
        if or_result[or_result.find('then')-6:or_result.find('then')-3] == 'not':
            exp1 = or_result[or_result.find('then')-6:or_result.find('then')-1]
            start_point = or_result.find('then')-6
        else:
            exp1 = or_result[or_result.find('then')-2:or_result.find('then')-1]
            start_point = or_result.find('then')-2
        if or_result[or_result.find('then')+5:or_result.find('then')+8] == 'not':
            exp2 = or_result[or_result.find('then')+5:or_result.find('then')+10]
            finish_point = or_result.find('then')+10
        else:
            exp2 = or_result[or_result.find('then')+5:or_result.find('then')+6]
            finish_point = or_result.find('then')+6
        exp1_position = variables.index(exp1[-1])
        exp2_position = variables.index(exp2[-1])
        if 'not' in exp1:
            if values[exp1_position] == '1':
                first = '0'
            else:
                first = '1'
        else:
            first = values[exp1_position]
        if 'not' in exp2:
            if values[exp2_position] == '1':
                second = '0'
            else:
                second = '1'
        else:
            second = values[exp2_position]
        if first == '1' and second == '0':
            value = '0'
        else:
            value = '1'
        result = or_result[:start_point] + value + or_result[finish_point:]
        final = then_operator(result, variables, values)
        return final
    else:
        return or_result


def equal_operator(then_result, variables, values):
    if 'equal' in then_result:
        if then_result[then_result.find('equal')-6:then_result.find('equal')-3] == 'not':
            exp1 = then_result[then_result.find('equal')-6:then_result.find('equal')-1]
            start_point = then_result.find('equal')-6
        else:
            exp1 = then_result[then_result.find('equal')-2:then_result.find('equal')-1]
            start_point = then_result.find('equal')-2
        if then_result[then_result.find('equal')+6:then_result.find('equal')+9] == 'not':
            exp2 = then_result[then_result.find('equal')+6:then_result.find('equal')+11]
            finish_point = then_result.find('equal')+11
        else:
            exp2 = then_result[then_result.find('equal')+6:then_result.find('equal')+7]
            finish_point = then_result.find('equal')+7
        exp1_position = variables.index(exp1[-1])
        exp2_position = variables.index(exp2[-1])
        if 'not' in exp1:
            if values[exp1_position] == '1':
                first = '0'
            else:
                first = '1'
        else:
            first = values[exp1_position]
        if 'not' in exp2:
            if values[exp2_position] == '1':
                second = '0'
            else:
                second = '1'
        else:
            second = values[exp2_position]
        if first == second:
            value = '1'
        else:
            value = '0'
        result = then_result[:start_point] + value + then_result[finish_point:]
        final = equal_operator(result, variables, values)
        return final
    else:
        return then_result


main()