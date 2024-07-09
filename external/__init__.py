from ..base import protoExe, exeClass


class exeAST(protoExe):
    def dispatchAST(self, node, **kwd):
        # print(node)
        # if 'kind' not in node:
        #     print(node)
        #     breakOn()
        #     # pass

        # todo: will have to that base exeAST doesn't do node.ast.kind but only the immediate...
        try: kind = node.ast.kind
        except AttributeError:
            kind = node.kind

        try:
            return getattr \
                (self, kind,
                 *self.default) \
                    (node, **kwd)

        except TypeError as e:
            breakOn()

        # return getattr \
        #     (self, kind,
        #      *self.default) \
        #         (node, **kwd)


    class namespace(dict):
        def __init__(self, *args, **kwd):
            super().__init__(*args, **kwd)
            self.__dict__ = self

            # (data, *args) = args if args else (dict(), ())
            # self.__dict__ = data
            # data.update(kwd)

    namespaceOf = namespace


    def dispatch(self, node, **kwd):
        return self.dispatchAST \
            (self.namespaceOf \
                (node), **kwd)


class delegationOperations:
    def __init__(self):
        self.delegation = dict()


    def delegationOf(self, node):
        return self.delegation \
            [node.name]

    def Delegation(self, node, **kwd):
        return self(self.delegationOf
            (node), **kwd)


class delegateAst(exeAST, delegationOperations):
    def __init__(self, *args, **kwd):
        super().__init__(*args, **kwd)
        delegationOperations.__init__(self)


from .immediate import *
