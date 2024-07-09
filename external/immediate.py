from ..external import exeAST, exeClass


class externalizationOperations:
    def __init__(self, externalizations):
        self.externalizations = externalizations

    def Externalization(self, node, **kwd):
        return self.externalizations \
            [node.service] \
                (self, node, **kwd)


class compileOperations:
    @classmethod
    def externalOf(self, **kwd):
        # breakOn()
        return self.defaultExternalOf(**kwd)


    @classmethod
    def externalSuiteOf(self, suite):
        return self.externalOf \
            (suite = list
                (map(self, suite)))


    def externalNodeOf(self, node):
        if isinstance(node, list):
            return list(map(self.externalNodeOf, node))

        if not isinstance(node, AST):
            return node

        # if isinstance(node, str):
        #     breakOn()

        # if not isinstance(node, BinOp):
        # if node.__class__.__name__ == 'BinOp':
        #     breakOn()

        return self.externalOf \
            (ast = exeAST \
                .namespaceOf(kind = node.__class__.__name__),
             **{name: self(getattr(node, name))
                for name in node._fields})


from json import loads as loadJsonString

class httpOperations:
    @classmethod
    def defaultExternalizations(self):
        return dict(default = self.httpService,
                    http = self.httpService)


    @classmethod
    def httpExternalizationOf(self, location, **kwd):
        ns = dict(kind = 'Externalization',
                  service = 'http',
                  location = location)


        try: ns['headers'] = kwd['headers']
        except KeyError: pass

        try: ns['post'] = kwd['post']
        except KeyError:
            try: ns['method'] = kwd['method']
            except KeyError: pass
        else:
            try: ns['method'] = kwd['method']
            except KeyError: ns['method'] = 'post'


        return exeAST.namespaceOf \
            (ns)


    @classmethod
    def httpService(self, exe, node, **kwd):
        # Todo: how to generalize incorporation of kwd into url method?
        u = URL(node.location,
            headers = node.get
                ('headers', dict()))


        method = u.get('method', 'get')
        if method == 'get':
            r = u.get()

        elif method == 'post':
            r = u.post(data = node.get
                ('post', None))

        else:
            raise ValueError(f'Unknown method: {method}')


        o = r.headers.get('Content-Type')
        if o == 'text/json':
            # XXX pass kwd here?
            return exe(loadJsonString(r.content), **kwd)

        else:
            raise ValueError(f'Unknown content-type: {o}')


    @classmethod
    def defaultExternalOf(self, **kwd):
        return self.httpExternalizationOf \
            ('https://network/execute',
             post = kwd)


class immediateOperations:
    @classmethod
    def defaultExternalizations(self):
        return dict(default = self.immediateService,
                    immediate = self.immediateService)


    @classmethod
    def immediateExternalizationOf(self, data):
        return exeAST.namespaceOf \
            (data = data,
             kind = 'Externalization',
             service = 'immediate')


    @classmethod
    def immediateService(self, exe, node, **kwd):
        # breakOn()
        # XXX WHy doing exe: arg?!?

        # exe = exe # .exe

        # Using dispatch instead of ReturnOperation-catching __call__:
        return exe.dispatch(node.data, **kwd)


    @classmethod
    def defaultExternalOf(self, **kwd):
        return self.immediateExternalizationOf \
            (kwd)


    def opArgOf(self, node, **kwd):
        # XXX Note: this is rebuilding the AST instance
        # such that arithmeticOperations.BinOp can succeed
        # the 'isinstance' check.
        return getattr \
            (pyAstModule,
             node.ast.kind) \
                () # ['ast']['kind'])

    And = Or = Add = Sub = Mult = MatMult = \
    Div = Mod = Pow = LShift = RShift = BitOr = \
    BitXor = BitAnd = FloorDiv = Invert = Not = UAdd = \
    USub = Eq = NotEq = Lt = LtE = Gt = \
    GtE = Is = IsNot = In = NotIn = \
        opArgOf


class immediateCompiler:
    def dispatch(self, node, **kwd):
        return self \
            .externalNodeOf \
                (node)


class baseImmediate(exeAST, exeClass):
    pass

class exeImmediateCompiler(immediateCompiler, immediateOperations, compileOperations, baseImmediate):
    pass


class immediateClass(baseImmediate, immediateOperations, externalizationOperations):
    opArgOf = immediateOperations.opArgOf

    And = Or = Add = Sub = Mult = MatMult = \
    Div = Mod = Pow = LShift = RShift = BitOr = \
    BitXor = BitAnd = FloorDiv = Invert = Not = UAdd = \
    USub = Eq = NotEq = Lt = LtE = Gt = \
    GtE = Is = IsNot = In = NotIn = \
        opArgOf


    Load = Store = Del = opArgOf


    # definitionOperations
    class definitionObject(baseImmediate.definitionObject):
        @property
        def executionClass(self):
            return self.exe.__class__


    class CallableFunction(definitionObject, baseImmediate.CallableFunction):
        pass


    class Method(CallableFunction, baseImmediate.Method):
        pass

    class UnboundMethod(Method, baseImmediate.UnboundMethod):
        pass
    class BoundMethod(Method, baseImmediate.BoundMethod):
        pass


    class LambdaCallableFunction(CallableFunction, baseImmediate.LambdaCallableFunction):
        pass


    class ClassDefinition(definitionObject, baseImmediate.ClassDefinition):
        pass

        # def declare(self):
        #     breakOn()
        #     return super() \
        #         .declare()


    def arguments(self, node):
        # XXX Yes, this doesn't make sense, except that
        # the implementation of immediate relies on
        # astOperations.arguments which just doesn't
        # do the walking...
        c = self.compilerClass()

        return c.externalNodeOf \
            (exeAST.namespaceOf
                (node, args = list
                    (map(self, node.args))))

            # (posonlyargs = node.posonlyargs,
            #  args = list(map(self, node.args)),
            #  vararg = node.vararg,
            #  kwonlyargs = node.kwonlyargs,
            #  kw_defaults = node.kw_defaults,
            #  kwarg = node.kwarg,
            #  defaults = node.defaults)

    def arg(self, node):
        return node

        # node.arg
        # node.annotation
        # node.type_comment

    def keyword(self, node):
        return node

        # node.arg
        # node.value

    # def alias(self, node):
    #     return node

    #     # node.name
    #     # node.asname


    # def Load(self, node):
    #     return node
    # def Store(self, node):
    #     return node
    # def Del(self, node):
    #     return node


    def __init__(self, *args, **kwd):
        super().__init__(*args, **kwd)
        externalizationOperations.__init__ \
            (self, self.defaultExternalizations())


class exeImmediate(immediateClass):
    compilerClass = exeImmediateCompiler

    @classmethod
    def compile(self, *args):
        return self \
            .compilerClass() \
                (self.parseAstIf
                    (*args))


    @classmethod
    def run(self, *args, **kwd):
        try: (initArgs, initKwd) = kwd.pop('init')
        except KeyError:
            initArgs = ()
            initKwd = dict()

        return self \
            (*initArgs, **initKwd) \
                (self.compile
                    (*args),
                 **kwd)


    # def __init__(self, *args, **kwd):
    #     super().__init__(*args, **kwd)

    #     # XXX execute shall not be compatible with the externalized node
    #     self.exe = self # .__class__() # immediateClass() # execute()


    @property
    def default(self):
        return (self.dispatchNode,)

    def dispatchNode(self, node, **kwd):
        # XXX Yes this duplicates,
        # but don't yet have impl
        # and also relying on exeClass.
        return getattr \
            (exeClass, node.ast.kind) \
                (node, **kwd)


    def importAliasAssignment(self, a, o = None):
        # breakOn()
        return super() \
            .importAliasAssignment \
                (exeAST.namespaceOf
                    (self(a)),
                 o = o)

    def importFromAlias(self, o, a):
        # breakOn()
        return super() \
            .importFromAlias \
                (o, exeAST
                    .namespaceOf
                        (self(a)))


class externalizationCompiler:
    def Module(self, node):
        return self.externalSuiteOf(self.body)
    def Interactive(self, node):
        return self.externalSuiteOf(self.body)
    def Expression(self, node):
        return self.externalSuiteOf(self.value)


    def FunctionType(self, node):
        pass
    def FunctionDef(self, node):
        pass
    def Lambda(self, node):
        pass
    def AsyncFunctionDef(self, node):
        pass
    def ClassDef(self, node):
        pass


    # Module
    # Interactive
    # Expression

    # FunctionType
    # FunctionDef
    # Lambda
    # AsyncFunctionDef
    # ClassDef


    # def (self, *args, **kwd):
    #     return self.externalNodeOf \
    #         (*args, **kwd)


    Constant = \
    Name = \
    Attribute = \
    Subscript = \
        compileOperations \
            .externalNodeOf


    # Return
    # Pass
    # Break
    # Continue

    # For
    # AsyncFor
    # While
    # If
    # With
    # AsyncWith
    # Raise

    # Try
    # ExceptHandler
    # Assert
    # Await
    # Yield
    # YieldFrom

    # Import
    # ImportFrom

    # Expr
    # Call

    # BoolOp
    # BinOp
    # UnaryOp
    # Compare
    # IfExp
    # NamedExpr

    # ListComp
    # SetComp
    # DictComp
    # GeneratorExp

    # FormattedValue
    # JoinedStr
    # Starred

    # List
    # Tuple
    # Dict
    # Set
    # Slice

    # Num
    # Str
    # Bytes

    # Global
    # Nonlocal
    # Delete

    # Assign
    # AugAssign
    # AnnAssign

    # Load
    # Store
    # Del

    # And
    # Or
    # Add
    # Sub
    # Mult

    # MatMult

    # Div
    # Mod
    # Pow

    # LShift
    # RShift
    # BitOr
    # BitXor
    # BitAnd
    # FloorDiv

    # Invert
    # Not
    # UAdd
    # USub
    # Eq
    # NotEq
    # Lt
    # LtE
    # Gt
    # GtE
    # Is
    # IsNot
    # In
    # NotIn

    # TypeIgnore
    # NameConstant

    # Ellipsis

    # Index
    # ExtSlice
    # Suite
    # AugLoad
    # AugStore
    # Param


    def Constant(self, node):
        pass
    def Name(self, node, **kwd):
        pass
    def Attribute(self, node, **kwd):
        pass
    def Subscript(self, node):
        pass

    def Return(self, node):
        pass
    def Pass(self, node):
        pass
    def Break(self, node):
        pass
    def Continue(self, node):
        pass

    def For(self, node):
        pass
    def AsyncFor(self, node):
        pass
    def While(self, node):
        pass
    def If(self, node):
        pass
    def With(self, node):
        pass
    def AsyncWith(self, node):
        pass
    def Raise(self, node):
        pass

    def Try(self, node):
        pass
    def ExceptHandler(self, node):
        pass
    def Assert(self, node):
        pass
    def Await(self, node):
        pass
    def Yield(self, node):
        pass
    def YieldFrom(self, node):
        pass

    def Import(self, node):
        pass
    def ImportFrom(self, node):
        pass

    def Expr(self, node):
        pass
    def Call(self, node):
        pass

    def BoolOp(self, node):
        pass
    def BinOp(self, node):
        pass
    def UnaryOp(self, node):
        pass
    def Compare(self, node):
        pass
    def IfExp(self, node):
        pass
    def NamedExpr(self, node):
        pass

    def ListComp(self, node):
        pass
    def SetComp(self, node):
        pass
    def DictComp(self, node):
        pass
    def GeneratorExp(self, node):
        pass

    def FormattedValue(self, node):
        pass
    def JoinedStr(self, node):
        pass
    def Starred(self, node):
        pass

    def List(self, node):
        pass
    def Tuple(self, node):
        pass
    def Dict(self, node):
        pass
    def Set(self, node):
        pass
    def Slice(self, node):
        pass

    def Num(self, node):
        pass
    def Str(self, node):
        pass
    def Bytes(self, node):
        pass

    def Global(self, node):
        pass
    def Nonlocal(self, node):
        pass
    def Delete(self, node):
        pass

    def Assign(self, node):
        pass
    def AugAssign(self, node):
        pass
    def AnnAssign(self, node):
        pass

    def Load(self, node):
        pass
    def Store(self, node):
        pass
    def Del(self, node):
        pass

    def And(self, node):
        pass
    def Or(self, node):
        pass
    def Add(self, node):
        pass
    def Sub(self, node):
        pass
    def Mult(self, node):
        pass

    def MatMult(self, node):
        pass

    def Div(self, node):
        pass
    def Mod(self, node):
        pass
    def Pow(self, node):
        pass

    def LShift(self, node):
        pass
    def RShift(self, node):
        pass
    def BitOr(self, node):
        pass
    def BitXor(self, node):
        pass
    def BitAnd(self, node):
        pass
    def FloorDiv(self, node):
        pass

    def Invert(self, node):
        pass
    def Not(self, node):
        pass
    def UAdd(self, node):
        pass
    def USub(self, node):
        pass
    def Eq(self, node):
        pass
    def NotEq(self, node):
        pass
    def Lt(self, node):
        pass
    def LtE(self, node):
        pass
    def Gt(self, node):
        pass
    def GtE(self, node):
        pass
    def Is(self, node):
        pass
    def IsNot(self, node):
        pass
    def In(self, node):
        pass
    def NotIn(self, node):
        pass

    def TypeIgnore(self, node):
        pass
    def NameConstant(self, node):
        pass

    def Ellipsis(self, node):
        pass

    def Index(self, node):
        pass
    def ExtSlice(self, node):
        pass
    def Suite(self, node):
        pass
    def AugLoad(self, node):
        pass
    def AugStore(self, node):
        pass
    def Param(self, node):
        pass
