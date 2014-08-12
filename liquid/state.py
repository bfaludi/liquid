
# -*- coding: utf-8 -*-

"""
Liquid is a form management tool for web frameworks.
Copyright (C) 2014, Bence Faludi (b.faludi@mito.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

class State( object ):

    # void
    def __init__( self, required, hidden, readonly, disabled, focus, error = None ):

        self.setError( error )
        self.setRequired( required )
        self.setHidden( hidden )
        self.setReadonly( readonly )
        self.setDisabled( disabled )
        self.setFocus( focus )

    # dict
    def getState( self ):

        return {
            'required': self.isRequired(),
            'readonly': self.isReadonly(),
            'focus': self.isFocus(),
            'disabled': self.isDisabled(),
            'hidden': self.isHidden(),
            'error': self.getError()
        }

    # void
    def setError( self, error ):

        self.error = error

     # void
    def setRequired( self, required = True ):

        self.required = required

    # void
    def setFocus( self, focus = True ):

        self.focus = focus

    # void
    def setHidden( self, hidden = True ):

        self.hidden = hidden

    # void
    def setReadonly( self, readonly = True ):

        self.readonly = readonly

    # void
    def setDisabled( self, disabled = True ):

        self.disabled = disabled

    # bool
    def isError( self ):

        return self.error is not None

    # bool
    def isRequired( self ):

        return self.required

    # bool
    def isFocus( self ):

        return self.focus

    # bool
    def isHidden( self ):

        return self.hidden

    # bool
    def isReadonly( self ):

        return self.readonly

    # bool
    def isDisabled( self ):

        return self.disabled

    # bool
    def isActive( self ):

        if self.isHidden() or self.isReadonly() or self.isDisabled():
            return False

        return True

    # unicode
    def getError( self ):

        return self.error
