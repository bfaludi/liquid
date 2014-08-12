
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

from . import widgets

def flattenAbsData( value_dict ):

    r_dict = {}
    for key, value in ( value_dict or {} ).items():
        if not isinstance( value, dict ):
            r_dict[ key ] = value
            continue

        for ikey, ivalue in flattenAbsData( value ).items():
            r_dict[ u'{}_{}'.format( key, ikey ) ] = ivalue

    return r_dict

class Form( object ):

    _counter = 1

    # void
    def __init__( self, element, value = None, submit = u'Submit', buttons = None, cls = None ):

        self._element = element.clone()
        self._element.setAbsName()
        self._element.setValue( value )

        self._buttons = [ 
            widgets.Button( 
                submit,
                name = 'submit',
                is_primary = True 
            ) 
        ] + ( buttons or [] )
        self._widget = widgets.Form()
        self._cls = cls

    # Field
    def __getattr__( self, attr ):

        return getattr( self.getElement(), attr )

    # void
    def setErrorWidgets( self, widget ):

        """
        Set the element's widget's error widget. Its responsible for
        how show the given error messages in the form.

        @param widget: Error widget object
        @type widget: widgets.Widget
        """

        self.getElement().setErrorWidget( widget )

    # list<Button>
    def getButtons( self ):

        return self._buttons

    # Element
    def getElement( self ):

        return self._element

    # unicode
    def getClass( self ):

        return self._cls

    # tuple<bool,list>
    def isValid( self, return_list = False ):

        if return_list:
            return self.getElement().isValid()

        valid, _ = self.getElement().isValid()
        return valid

    # unicode
    def render( self ):

        return self._widget.render( self )

    # dict
    def getValue( self ):

        return self.getElement().getValue()

    # void
    def setValue( self, value ):

        self.getElement().setValue( value )

    # void
    def delValue( self ):

        self.getElement().delValue()

    value = property( getValue, setValue, delValue )
