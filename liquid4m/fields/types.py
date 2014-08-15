
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

import datetime, re
from dateutil import parser
from ..exceptions import TypeConversionError

class Type( object ):

    """
    Basic type class for mapping puroses.
    """

    # List of expected types
    _default_types = []

    # bool
    def isInherited( self, value ):
        
        """
        Checks the value is inherited from the list of expected types.

        @param value: Value
        @type value: type

        @return: Value is interited from the list of expected types.
        @rtype: bool
        """

        for checked_type in self._default_types:
            if isinstance( value, checked_type ):
                return True

        return False

    # type
    def convert( self, value ):

        """
        Converts a value into the expected type.

        @param value: Value
        @type value: type

        @return: Converted value
        @type: type
        """

        raise RuntimeError( '%(cls)s.convert( value ) is not implemented!' % {
            'cls': self.__class__.__name__
        } )

    # type
    def modify( self, value ):

        """
        Modify the converted value if it neccesary.

        @param value: Converted value
        @type value: type

        @return: Modified value
        @type: type
        """

        return value

    # bool
    def isEmpty( self, value ):

        """
        Checks the value is empty or not. It will empty string as empty
        value as well.

        @param value: Value
        @type value: type

        @return: Is empty?
        @rtype: bool
        """

        return ( value is None or len( unicode( value ).strip() ) == 0 )

    # type
    def getValue( self, value ):
        
        """
        Returns a converted value into the expected types.

        @param value: Value
        @type value: type

        @return: Converted value
        @rtype: type
        """

        # If the value is empty then returns None
        if self.isEmpty( value ):
            return None

        # If the value is inherited from the expected value then modify
        if self.isInherited( value ):
            return self.modify( value )
        
        # Otherwise, try to convert and modify the value
        try:
            return self.modify( self.convert( value ) )

        except:
            raise TypeConversionError()

class String( Type ):

    """
    String type.
    """

    # List of expected types
    _default_types = [ unicode, str ]

    # unicode
    def convert( self, value ):

        """
        Converts a value into string.

        @param value: Value
        @type value: type

        @return: Converted value
        @type: unicode
        """

        return unicode( value )

    # unicode
    def modify( self, value ):

        """
        Strips the converted value.

        @param value: Converted value
        @type value: type

        @return: Modified value
        @type: type
        """

        return value.strip()

class Integer( Type ):
    
    """
    Integer type.
    """

    # List of expected types
    _default_types = [ int ]

    # int
    def convert( self, value ):

        """
        Converts a value into integer.

        @param value: Value
        @type value: type

        @return: Converted value
        @type: int
        """

        try:
            return int( value )

        except:
            return int( float( re.sub( r',', '.', value ) ) )

class Float( Type ):
    
    """
    Float type.
    """

    # List of expected types
    _default_types = [ float ]

    # float
    def _convert( self, value ):

        """
        Converts a value into float.

        @param value: Value
        @type value: type

        @return: Converted value
        @type: unicode
        """

        try:
            return float( value )

        except:
            return float( re.sub( r',', '.', value ) )

class Boolean( Type ):

    """
    Boolean type.
    """

    # List of expected types
    _default_types = [ bool ]

    # bool
    def convert( self, value ):

        """
        Converts a value into boolean.

        @param value: Value
        @type value: type

        @return: Converted value
        @type: bool
        """

        if str( value ).lower() in ("yes", "y", "true",  "t", "1"): 
            return True

        if str( value ).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): 
            return False

        raise TypeError()

class Date( Type ):
    
    """
    Date type.
    """

    # List of expected types
    _default_types = [ datetime.date ]

    # datetime.date
    def parseString( self, value ):

        """
        Parse the string and return a date object.

        @param value: Value
        @type value: unicode

        @return: Date object
        @rtype: datetime.date
        """

        try:
            return parser.parse( value ).date()

        except:
            return parser.parse( value.split(' ')[0] ).date()

    # datetime.date
    def convert( self, value ):

        """
        Converts a value into date object.

        @param value: Value
        @type value: type

        @return: Converted value
        @type: datetime.date
        """

        if isinstance( value, tuple ) or isinstance( value, list ):
            return datetime.date( value[0], value[1], value[2] )

        if isinstance( value, str ) or isinstance( value, unicode ):
            return self.parseString( value )

        if isinstance( value, datetime.datetime ):
            return value.date()

        raise TypeError()

class DateTime( Type ):
    
    """
    DateTime type.
    """

    # List of expected types
    _default_types = [ datetime.datetime ]

    # datetime.datetime
    def convert( self, value ):

        """
        Converts a value into datetme object.

        @param value: Value
        @type value: type

        @return: Converted value
        @type: datetime.datetime
        """

        if isinstance( value, tuple ) or isinstance( value, list ):
            return datetime.datetime( value[0], value[1], value[2], value[3], value[4], value[5] )

        if isinstance( value, str ) or isinstance( value, unicode ):
            return parser.parse( value )

        if isinstance( value, datetime.date ):
            return datetime.datetime( value.year, value.month, value.day )

        raise TypeError()
