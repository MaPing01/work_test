class person:
    def __init__( self, name ):
        self.name = name

    def say( self ):
        print('%s say hi' % self.name)

    def eat( self ):
        if hasattr(self, 'say'):
            func = getattr(self, 'say')
            func()

b = person('willing')
b.eat()