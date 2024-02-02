class Expression:
    def __str__(self):
        string = ''
        if type(self) == Symbol:
            return self.string
        elif type(self) == Number:
            return str(self.number)
        else:
            for i in range(len(self.expressions)-1):
                string += str(self.expressions[i])+self.operator_string
            string += str(self.expressions[-1])
            return string

    def __add__(self, obj):
        if type(obj) == int or type(obj) == float:
            obj = Number(obj)
        return Addition(self, obj)

    def __mul__(self, obj):
        if type(obj) == int or type(obj) == float:
            obj = Number(obj)
        return Multiplication(self, obj)

    def __pow__(self, obj):
        if type(obj) == int or type(obj) == float:
            obj = Number(obj)
        return Power(self, obj)

    def simplify(self):
        return self

    def print_structure(self):
        print(type(self))
        print()
        [(print(type(expr)),print(expr)) for expr in self.expressions]

    __rmul__ = __mul__
    __radd__ = __add__
    __rpow__ = __pow__


class Number(Expression):
    def __init__(self, number):
        self.number = number

class Operator(Expression):
    commutative = False

    def commutative_simplify(self):
        if self.commutative:

            #Combine nested expressions into self
            found_exressions = []
            for expression in self.expressions:

                if type(expression) == type(self):
                    if hasattr(expression,"commutative_simplify"):
                        expression.commutative_simplify()
                    found_exressions += expression.expressions
                else:
                    found_exressions.append(expression)
            self.expressions = found_exressions
        
            #Seperate all numbers and other expressions
            numbers = []
            non_numbers = []
            for expression in self.expressions:
                if type(expression) == Number:
                    numbers.append(expression.number)
                else:
                    non_numbers.append(expression)

            #Perform the object operation on all ints and combine
            if len(numbers) == 0:
                self.expressions = non_numbers
            elif len(numbers) == 1:
                self.expressions = [Number(numbers[0])]+non_numbers
            else:
                value = numbers[0]
                for i in range(1,len(numbers)):
                    value = self.real_operation(value,numbers[i])
                self.expressions = [Number(value)]+non_numbers
                

                    





class Addition(Operator):
    commutative = True
    def __init__(self, *args):

        for i in range(len(args)):
            if type(args[i]) == int or type(args[i]) == float:
                args[i] = Number(args[i])

        self.expressions = list(args)
        self.operator_string = "+"
        self.commutative_simplify()

    def real_operation(self,a,b):
        return a+b


class Multiplication(Operator):
    commutative = True
    def __init__(self, *args):
        self.expressions = list(args)
        self.operator_string = "*"
        self.commutative_simplify()

    def real_operation(self,a,b):
        return a*b


class Power(Operator):
    def __init__(self, expression1, expression2):
        self.expressions = expression1, expression2
        self.operator_string = "^"


class Symbol(Operator):
    def __init__(self, string):
        self.string = string


if __name__ == "__main__":

    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")

    expr = 2 + 2*a*2+2*b*2 + 2.2

    expr.commutative_simplify()

    expr.print_structure()

    print(expr)
