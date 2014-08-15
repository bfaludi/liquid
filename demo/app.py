
import pycountry, inspect, os, datetime, requests, json, codecs
from flask import *
from liquid4m import *
from functools import wraps
from pygments import highlight
from pygments.lexers import PythonLexer, HtmlLexer
from pygments.formatters import HtmlFormatter
app = Flask( __name__ )

def printSourceCode( fn = None, code = None, lexer = PythonLexer ):

    source_code = unicode( code ) \
        if code is not None \
        else inspect.getsource( fn )

    return highlight( source_code, lexer(), HtmlFormatter() )

class demo( object ):
    
    def __init__( self, header ):
        
        self.header = header

    def __call__( self, func ):

        outer = self

        @wraps( func )
        def decorated():
            
            f = func()

            return render_template(
                'form.jinja2',
                header = outer.header,
                valid = f.valid,
                renderer = f.render,
                results = {} if not request.form.get('submit') else f.value,
                current_function = func,
                printer = printSourceCode
            )

        return decorated

@app.route( '/' )
def index():

    return render_template(
        'index.html',
        scripts = printSourceCode( code = """<link href='http://fonts.googleapis.com/css?family=Roboto:700,300,400&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
<link rel="stylesheet" href="static/liquid4m/bower_components/normalize.css/normalize.css">
<link rel="stylesheet" href="static/liquid4m/css/style.css">
<script src="static/liquid4m/bower_components/modernizr/modernizr.js"></script>
<script src="static/liquid4m/bower_components/jquery/dist/jquery.js"></script>
<script src="static/liquid4m/bower_components/jquery-ui/ui/core.js"></script>
<script src="static/liquid4m/bower_components/jquery-ui/ui/widget.js"></script>
<script src="static/liquid4m/bower_components/jquery-ui/ui/mouse.js"></script>
<script src="static/liquid4m/bower_components/jquery-ui/ui/draggable.js"></script>
<script src="static/liquid4m/js/vendor/dropkick.js"></script>
<script src="static/liquid4m/js/vendor/dropkick.jquery.js"></script>
<script src="static/liquid4m/js/liquid.js"></script>""", lexer = HtmlLexer )
    )

@app.route( '/login_with_button', methods = ['GET','POST'] )
@demo('Login with Button')
def login_with_button():

    class UserPasswordExists( validators.FieldSetValidator ):

        msg = 'Given username or password is invalid.'

        # bool
        def isValid( self, fs ):

            # Hint: Determine this information by your models
            if fs.username.value == 'admin' and fs.password.value == 'Test123':
                return True

            return False

    class SchemaFieldSet( fieldsets.FieldSet ):

        _default_validators = UserPasswordExists(
            position = 'username'
        )

        username = fields.Text( 
            label = 'Username', 
            required = True,
            focus = True
        )

        password = fields.Password( 
            label = 'Password', 
            required = True
        )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values ),
        buttons = [ widgets.Button( 
            'Registration', 
            url = url_for('.registration') 
        ) ]
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/registration', methods = ['GET','POST'] )
@demo('Registration')
def registration():

    class UserNotExists( fields.validators.Validator ):

        msg = 'Please choose a different username.'

        # bool
        def isValid( self, f ):

            # Hint: Determine this information by your models
            if f.value != 'admin':
                return True

            return False

    class SchemaFieldSet( fieldsets.FieldSet ):

        _default_validators = fieldsets.validators.Same(
            position = 'password_again',
            field_names = [ 'password', 'password_again' ]
        )

        username = fields.Text( 
            label = 'Username', 
            required = True,
            validators = validators.And(
                fields.validators.Length( 5, 18 ),
                fields.validators.Pattern( '^[a-z0-9]+$' ),
                UserNotExists()
            )
        )

        password = fields.Password( 
            label = 'Password', 
            required = True,
            validators = validators.And(
                fields.validators.Length( 6, 32 ),
                fields.validators.Pattern( '.*[a-z].*', ignorecase = False ),
                fields.validators.Pattern( '.*[A-Z].*', ignorecase = False ),
                fields.validators.Pattern( '.*[0-9].*' )
            ) 
        )

        password_again = fields.Password( 
            label = 'Password again', 
            required = True,
            validators = validators.And(
                fields.validators.Length( 6, 32 ),
                fields.validators.Pattern( '.*[a-z].*', ignorecase = False ),
                fields.validators.Pattern( '.*[A-Z].*', ignorecase = False ),
                fields.validators.Pattern( '.*[0-9].*' )
            ) 
        )

        accept_tc = fields.SwitchCheckbox(
            option = fields.options.Option( True, 'I Agree To The Terms & Conditions'),
            validators = fields.validators.Equal( 
                True,
                msg = 'You have to accept the Terms & Conditions.' 
            )
        )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/match_validator_with_hint', methods = ['GET','POST'] )
@demo('Match Validator with Hint')
def match_validator_with_hint():

    class SchemaFieldSet( fieldsets.FieldSet ):

        country_code = fields.Text(
            label = 'Country Code',
            required = True,
            validators = fields.validators.Pattern( ur'^[A-Z]{2}$', ignorecase = False ),
            hint = 'Two letter long ISO format is expected (e.g.: HU, UK)'
        )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f


@app.route( '/length_validator', methods = ['GET','POST'] )
@demo('Length Validator')
def length_validator():

    class SchemaFieldSet( fieldsets.FieldSet ):

        short_text = fields.Text(
            label = 'Short text',
            validators = fields.validators.Length( max_length = 5 )
        )

        long_text = fields.Text(
            label = 'Long text',
            validators = fields.validators.Length( min_length = 10 )
        )

        ranged_text = fields.Text(
            label = 'Ranged text',
            validators = fields.validators.Length( 5, 10 )
        )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/range_validator', methods = ['GET','POST'] )
@demo('Range Validator')
def range_validator():

    class SchemaFieldSet( fieldsets.FieldSet ):

        age = fields.Number(
            label = 'Age',
            validators = fields.validators.Range( 18, 100 )
        )

        date_of_graduation = fields.Date(
            label = 'Date of graduation',
            validators = fields.validators.Range( min_value = '2000/01/01' )
        )

        birth_date = fields.Date(
            label = 'Birth date',
            validators = fields.validators.Range( max_value = datetime.date.today() )
        )


    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/input_fields', methods = ['GET','POST'] )
@demo('Input Fields')
def input_fields():

    class SchemaFieldSet( fieldsets.FieldSet ):

        user_id = fields.Hidden( type = fields.types.Integer() )
        full_name = fields.Text( label = 'Full name', 
            placeholder = 'John Doe' )
        password = fields.Password( label = 'Password' )
        number_of_children = fields.Number( label = 'Number of children' )
        birth_date = fields.Date( label = 'Birth date' )
        email = fields.Email( label = 'Email address', 
            hint = """Please do not use your work email address. Your boss 
            wont be happy.""" )
        telephone = fields.Telephone( label = 'Telephone number' )
        website = fields.URL( label = 'Website' )
        search = fields.Search( label = 'Search terms' )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values ) or { 'user_id': '1' }
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/select_fields', methods = ['GET','POST'] )
@demo('Select and Multiple Select Fields')
def select_fields():

    class SchemaFieldSet( fieldsets.FieldSet ):

        # list<fields.options.Option>
        def getMusicGenres():

            return fields.options.generate([
                ( 1, 'Avant-Garde' ),
                ( 2, 'Blues' ),
                ( 3, 'Children\'s' ),
                ( 4, 'Classical' ),
                ( 5, 'Comedy/Spoken' ),
                ( 6, 'Country' ),
                ( 7, 'Easy Listening' ),
                ( 8, 'Electronic' ),
                ( 9, 'Folk' ),
                ( 10, 'Holiday' ),
                ( 11, 'International' ),
                ( 12, 'Jazz' ),
                ( 13, 'Latin' ),
                ( 14, 'New Age' ),
                ( 15, 'Pop/Rock' ),
                ( 16, 'R&B' ),
                ( 17, 'Rap' ),
                ( 18, 'Reggae' ),
                ( 19, 'Religious' ),
                ( 20, 'Stage & Screen' ),
                ( 21, 'Vocal' ),
            ])

        # list<fields.options.MultiDimensionalOption>
        def getFoursquareCategories():

            def getCategory( categories ):

                for category in categories:
                    # Hint: Use MultiDimensionalOption for multiple level
                    # option lists.
                    yield fields.options.MultiDimensionalOption(
                        category['id'],
                        category['name'],
                        options = getCategory( category.get('categories', []) )
                    )

            data = json.load( codecs.open('static/4sq.json','r','utf-8') )
            return getCategory( data.get('response',{}).get('categories',[]) )

        active = fields.Select(
            label = 'Active',
            type = fields.types.Boolean(),
            # Hint: convert tuple/list items into list of Option
            options = fields.options.generate([
                ( True, 'Yes' ),
                ( False, 'No' )
            ])
        )

        gender = fields.Select(
            label = 'Gender',
            options = [
                # Hint: empty element is acceptable
                fields.options.Empty(),
                fields.options.Option( 'M', 'Male' ),
                fields.options.Option( 'F', 'Female' )
            ]
        )

        favourite_genre_ids = fields.Select(
            label = 'Favourite Genres',
            type = fields.types.Integer(),
            # Hint: If you want to allow multiple selection
            multiple = True,
            # Hint: define just the function name and it will be evaluated when
            # the form is created.
            options = getMusicGenres 
        )

        favourite_sub_genres = fields.Select(
            label = 'Age group',
            options = [
                fields.options.Option( '-9', 'Children, under 9 year' ),
                # Hint: Use OptionGroup for two-level grouping
                fields.options.OptionGroup(
                    'Adolescents',
                    options = [
                        fields.options.Option( '10-14', '10-14', disabled = True ),
                        fields.options.Option( '15-18', '15-18' ),
                    ]
                ),
                fields.options.OptionGroup(
                    'Adults',
                    options = [
                        fields.options.Option( '19-25', '19-25' ),
                        fields.options.Option( '26-35', '26-35' ),
                        fields.options.Option( '36-45', '36-45' ),
                    ]
                ),
                fields.options.OptionGroup(
                    'Middle and Older age',
                    # Hint: You can disable the whole group
                    disabled = True,
                    options = [
                        fields.options.Option( '46-60', '46-60' ),
                        fields.options.Option( '60-', 'older then 60 year' ),
                    ]
                ),
            ]
        )

        interests_4sq_ids = fields.Select(
            label = 'Interests in 4sq',
            multiple = True,
            options = getFoursquareCategories
        )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/checkbox_fields', methods = ['GET','POST'] )
@demo('Checkbox Fields')
def checkbox_fields():

    class SchemaFieldSet( fieldsets.FieldSet ):

        # list<fields.options.Option>
        def getMusicGenres():

            # Hint: convert tuple/list items into list of Option
            return fields.options.generate([
                ( 1, 'Avant-Garde' ),
                ( 2, 'Blues' ),
                ( 3, 'Children\'s' ),
                ( 4, 'Classical' ),
                ( 5, 'Comedy/Spoken' ),
                ( 6, 'Country' ),
                ( 7, 'Easy Listening' ),
                ( 8, 'Electronic' ),
                ( 9, 'Folk' ),
                ( 10, 'Holiday' ),
                ( 11, 'International' ),
                ( 12, 'Jazz' ),
                ( 13, 'Latin' ),
                ( 14, 'New Age' ),
                ( 15, 'Pop/Rock' ),
                ( 16, 'R&B' ),
                ( 17, 'Rap' ),
                ( 18, 'Reggae' ),
                ( 19, 'Religious' ),
                ( 20, 'Stage & Screen' ),
                ( 21, 'Vocal' ),
            ])

        favourite_genre_ids = fields.Checkbox(
            label = 'Favourite Genres',
            type = fields.types.Integer(),
            # Hint: define just the function name and it will be evaluated when
            # the form is created.
            options = getMusicGenres
        )

        accept_tc = fields.SwitchCheckbox(
            # Hint: You cant define the type attribute, its Boolean and it
            # can't be multiple or required field.
            label = 'Subscription',
            # Hint: Be aware, the paramter's name is 'option', not 'options'
            option = fields.options.Option( True, 'Subscribe to newsletter' )
        )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/radio_field', methods = ['GET','POST'] )
@demo('Radio Field')
def radio_field():

    class SchemaFieldSet( fieldsets.FieldSet ):

        gender = fields.Radio(
            label = 'Gender',
            options = fields.options.generate( [ ('M','Male'), ('F','Female') ] )
        )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/selected_validator', methods = ['GET','POST'] )
@demo('Selected Validator')
def selected_validator():

    class SchemaFieldSet( fieldsets.FieldSet ):

        # list<fields.options.Option>
        def getMusicGenres():

            # Hint: convert tuple/list items into list of Option
            return fields.options.generate([
                ( 1, 'Avant-Garde' ),
                ( 2, 'Blues' ),
                ( 3, 'Children\'s' ),
                ( 4, 'Classical' ),
                ( 5, 'Comedy/Spoken' ),
                ( 6, 'Country' ),
                ( 7, 'Easy Listening' ),
                ( 8, 'Electronic' ),
                ( 9, 'Folk' ),
                ( 10, 'Holiday' ),
                ( 11, 'International' ),
                ( 12, 'Jazz' ),
                ( 13, 'Latin' ),
                ( 14, 'New Age' ),
                ( 15, 'Pop/Rock' ),
                ( 16, 'R&B' ),
                ( 17, 'Rap' ),
                ( 18, 'Reggae' ),
                ( 19, 'Religious' ),
                ( 20, 'Stage & Screen' ),
                ( 21, 'Vocal' ),
            ])

        selected_genre_ids = fields.Select(
            label = 'Selected Genres',
            type = fields.types.Integer(),
            multiple = True,
            options = getMusicGenres,
            validators = fields.validators.Selected( max_selected = 3 )
        )

        checked_genre_ids = fields.Checkbox(
            label = 'Checked Genres',
            type = fields.types.Integer(),
            options = getMusicGenres,
            # Hint: You have to define required if you dont want to 
            # accept empty value.
            required = True,
            validators = fields.validators.Selected( 3, 6 )
        )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/same_validator', methods = ['GET','POST'] )
@demo('Same Validator')
def same_validator():

    class SchemaFieldSet( fieldsets.FieldSet ):

        _default_validators = fieldsets.validators.Same(
            position = 'number',
            field_names = ['number','number_again']
        )

        number = fields.Number( label = 'Number' )
        number_again = fields.Number( label = 'Number again' )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/different_validator', methods = ['GET','POST'] )
@demo('Different Validator')
def different_validator():

    class SchemaFieldSet( fieldsets.FieldSet ):

        _default_validators = fieldsets.validators.Different(
            position = 'number',
            field_names = ['number','number_again']
        )

        number = fields.Number( label = 'Number' )
        number_again = fields.Number( label = 'Other number' )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/greater_validator', methods = ['GET','POST'] )
@demo('Greater Validator')
def greater_validator():

    class SchemaFieldSet( fieldsets.FieldSet ):

        # Hint: Use list instead of validators.And, if you want to
        # evaluate in one time. It will generate two error message instad of
        # one. And will stop when the first validation fails.
        _default_validators = [
            fieldsets.validators.Greater(
                position = 'date_of_end',
                field_name = 'date_of_end',
                other_field_name = 'date_of_start'
            ),
            fieldsets.validators.GreaterAndEqual(
                position = 'salary_to',
                field_name = 'salary_to',
                other_field_name = 'salary_from'
            )
        ]

        date_of_start = fields.Date( label = 'Start work' )
        date_of_end = fields.Date( label = 'End work' )

        salary_from = fields.Number( 
            label = 'Salary starts', placeholder = 'Required minimum' )
        salary_to = fields.Number( 
            label = 'Salary ends', placeholder = 'Expected maximum' )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/less_validator', methods = ['GET','POST'] )
@demo('Less Validator')
def less_validator():

    class SchemaFieldSet( fieldsets.FieldSet ):

        # Hint: Use list instead of validators.And, if you want to
        # evaluate in one time. It will generate two error message instad of
        # one. And will stop when the first validation fails.
        _default_validators = [
            fieldsets.validators.Less(
                position = 'date_of_start',
                field_name = 'date_of_start',
                other_field_name = 'date_of_end'
            ),
            fieldsets.validators.LessAndEqual(
                position = 'salary_from',
                field_name = 'salary_from',
                other_field_name = 'salary_to'
            )
        ]

        date_of_start = fields.Date( label = 'Start work' )
        date_of_end = fields.Date( label = 'End work' )

        salary_from = fields.Number( 
            label = 'Salary starts', placeholder = 'Required minimum' )
        salary_to = fields.Number( 
            label = 'Salary ends', placeholder = 'Expected maximum' )

    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

@app.route( '/contact_information', methods = ['GET','POST'] )
@demo('Contact Information')
def contact_information():

    class AddressFieldSet( fieldsets.FieldSet ):

        _default_validators = validators.Or(
            fieldsets.validators.NoneOf(),
            fieldsets.validators.AllOf()
        )

        country_code = fields.Select( 
            label = 'Country Code',
            options = [ fields.options.Empty() ] + fields.options.generate( ( c.alpha2, c.name ) \
                for c in pycountry.countries ) 
        )
        street = fields.Text( 
            label = 'Street',
            validators = fields.validators.Length( max_length = 255 ) 
        )
        city = fields.Text( 
            label = 'City',
            validators = fields.validators.Length( max_length = 32 ) 
        )
        postal_code = fields.Number( label = 'Postal Code' )

    class SchemaFieldSet( fieldsets.FieldSet ):

        delivery_address = AddressFieldSet( legend = 'Delivery Address')
        invoice_address = AddressFieldSet( legend = 'Invoice Address' )


    f = form.Form( 
        SchemaFieldSet(), 
        dialects.flask( request.values )
    )
    if request.form.get('submit') and f.isValid():
        # Do the magic and redirect
        data = f.value

        pass

    # Use f.render to return the renderer function
    return f

if __name__ == '__main__':
    app.run(
        debug = True
    )

