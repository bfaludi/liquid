
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

from .. import widgets

# list<Option>
def generate( iterable ):

    """
    Iterate over the given list and generate a list of Option.

    @param iterable: Iterable object
    @type iterable: list

    @return: List of Options
    @rtype: list<Option>
    """

    rlist = []
    for item in iterable:
        if ( isinstance( item, list ) or isinstance( item, tuple ) ) and len( item ) >= 2:
            rlist.append( Option( item[0], item[1] ) )

        elif isinstance( item, dict ):
            rlist.append( Option( item.get('value'), item.get('label') ) )

    return rlist

class Options( object ):

    """
    Options class which handle multiple Option values. Its a Setter and Getter
    with levelling purposes.
    """

    # void
    def __init__( self, options = None ):

        """
        Options class which handle multiple Option values. Its a Setter and 
        Getter with levelling purposes.
        
        @param options: List of Options
        @type options: list<Option>
        """

        self.setOptions( options )

    # void
    def setOptions( self, options ):

        """
        Set a list of Option. It could get a function, a generator, or a static
        list.

        @param options: List of Options
        @type: list<Option> | generator | func
        """

        if options is None:
            self._options, self._fn = [], None

        if isinstance( options, list ):
            self._options, self._fn = options, None

        elif type( options ).__name__ == 'generator':
            self._options, self._fn = [ x for x in options ], None

        else:
            self._options, self._fn = [], options 

    # list<Option>
    def getOptions( self, level = 0 ):

        """
        Returns the list of options. It will automaticly set the given level
        for the options and call the options functions and generators.

        @param level: Current option level
        @type level: int

        @return: List of Options
        @rtype: list<Option>
        """

        return ( option.setLevel( level ) \
            for option in ( self._options if self._fn is None else self._fn() ) \
            if isinstance( option, Option ) )

class OptionsInterface( object ):

    """
    Interface for any object which collects Options.
    """

    # void
    def setOptions( self, options ):

        """
        Set a list of Option with the help of Options object.

        @param options: List of Options
        @type: list<Option> | generator | func
        """

        self._options.setOptions( options )

    # list<Option>
    def getOptions( self, level = 0 ):

        """
        Returns the list of options with the help of Options object.

        @param level: Current option level
        @type level: int

        @return: List of Options
        @rtype: list<Option>
        """

        return self._options.getOptions( level )

class Option( object ):

    """
    Basic Option class.
    """

    # void
    def __init__( self, value, label, disabled = False ):

        """
        Basic Option class.

        @param value: Option's value
        @type value: type

        @param label: Option's label
        @type label: unicode

        @param disabled: Option is not selectable
        @type disabled: bool
        """

        self._value = value
        self._label = label
        self._disabled = disabled
        self._level = 0

    # void
    def setLevel( self, level ):

        """
        Set the level of the Option.

        @param level: Current level
        @type level: int
        """

        self._level = level
        return self

    # int
    def getLevel( self ):

        """
        Returns the level of the Option.

        @return: Current level
        @rtype: int
        """

        return self._level

    # unicode
    def getName( self ):

        """
        Returns the class name.

        @return: Class name
        @rtype: unicode
        """

        return self.__class__.__name__.lower()

    # bool
    def isDisabled( self ):

        """
        Returns the Options is selectable or not.

        @return: Is disabled?
        @rtype: bool
        """

        return self._disabled

    # type
    def getValue( self, element ):

        """
        Returns the converted value of the Option.

        @param element: Checked object (Field, FieldSet, etc.)
        @type element: elements.Element

        @return: Converted option's value
        @rtype: type
        """

        return element.getTypeValue( self._value )

    # unicode
    def getLabel( self, levelled = False ):

        """
        Returns the Label of the Option.

        @param levelled: Returns the current level Option's label
        @type label: bool

        @return: Label
        @rtype: unicode
        """

        return u'-'*5*self.getLevel() + u' ' + self._label \
            if levelled and hasattr( self, 'getLevel') \
            else self._label

class OptionGroup( Option, OptionsInterface ):

    """
    OptionGroup class.
    """

    # void
    def __init__( self, label, options, disabled = False ):
        
        """
        OptionGroup class.

        @param label: Option's label
        @type label: unicode

        @param options: List of Options
        @type: list<Option> | generator | func

        @param disabled: Option is not selectable
        @type disabled: bool
        """

        self._options = Options( options )
        super( OptionGroup, self ).__init__( None, label, disabled )

class MultiDimensionalOption( Option, OptionsInterface ):

    """
    Multi Dimensional Option class.
    """
    
    # void
    def __init__( self, value, label, options, disabled = False ):

        """
        Multi Dimensional Option class.

        @param value: Option's value
        @type value: type

        @param label: Option's label
        @type label: unicode

        @param options: List of Options
        @type: list<Option> | generator | func

        @param disabled: Option is not selectable
        @type disabled: bool
        """

        self._options = Options( options )
        super( MultiDimensionalOption, self ).__init__( value, label, disabled )

class Empty( Option ):

    """
    Empty Option.
    """

    # void
    def __init__( self, label = '-- Select --' ):

        """
        Empty Option.

        @param label: Option's label
        @type label: unicode
        """

        super( Empty, self ).__init__( None, label, False )
