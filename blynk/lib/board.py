
idfunc = lambda *args: args

class Board:
    def analogRead(self, pin, wrapfunc=idfunc):
        """ Read an analog (ADC) pin """
        pass
        # return wrapfunc(result)

    def analogWrite(self, pin, value):
        """ Write value to analog (ADC) pin """
        pass

    def digitalRead(self, pin):
        """ Read a HIGH/LOW state of a pin """
        pass

    def digitalWrite(self, pin, value):
        """ Set a pin to a HIGH/LOW state """
        pass
