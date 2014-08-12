
import pycountry, inspect, os, datetime
from flask import *
from liquid import *
from functools import wraps
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
app = Flask( __name__ )

def printSourceCode( fn = None, code = None ):

    source_code = unicode( code ) \
        if code is not None \
        else inspect.getsource( fn )

    return highlight( source_code, PythonLexer(), HtmlFormatter() )

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
                renderer = f.render,
                results = {} if not request.form.get('submit') else f.value,
                current_function = func,
                printer = printSourceCode
            )

        return decorated

@app.route( '/' )
def index():

    return render_template(
        'base.html'
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
            required = True
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

    class UserNotExists( validators.Validator ):

        msg = 'Please choose a different username.'

        # bool
        def isValid( self, f ):

            # Hint: Determine this information by your models
            if f.value != 'admin':
                return True

            return False

    class SchemaFieldSet( fieldsets.FieldSet ):

        _default_validators = validators.Same(
            position = 'password_again',
            field_names = [ 'password', 'password_again' ]
        )

        username = fields.Text( 
            label = 'Username', 
            required = True,
            validators = validators.And(
                validators.Length( 5, 18 ),
                validators.Pattern( '^[a-z0-9]+$' ),
                UserNotExists()
            )
        )

        password = fields.Password( 
            label = 'Password', 
            required = True,
            validators = validators.And(
                validators.Length( 6, 32 ),
                validators.Pattern( '.*[a-z].*', ignorecase = False ),
                validators.Pattern( '.*[A-Z].*', ignorecase = False ),
                validators.Pattern( '.*[0-9].*' )
            ) 
        )

        password_again = fields.Password( 
            label = 'Password again', 
            required = True,
            validators = validators.And(
                validators.Length( 6, 32 ),
                validators.Pattern( '.*[a-z].*', ignorecase = False ),
                validators.Pattern( '.*[A-Z].*', ignorecase = False ),
                validators.Pattern( '.*[0-9].*' )
            ) 
        )

        accept_tc = fields.SwitchCheckbox(
            option = options.Option( True, 'I Agree To The Terms & Conditions'),
            validators = validators.Equal( 
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
            validators = validators.Pattern( ur'^[A-Z]{2}$', ignorecase = False ),
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
            validators = validators.Length( max_length = 5 )
        )

        long_text = fields.Text(
            label = 'Long text',
            validators = validators.Length( min_length = 10 )
        )

        ranged_text = fields.Text(
            label = 'Ranged text',
            validators = validators.Length( 5, 10 )
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
            validators = validators.Range( 18, 100 )
        )

        date_of_graduation = fields.Date(
            label = 'Date of graduation',
            validators = validators.Range( min_value = '2000/01/01' )
        )

        birth_date = fields.Date(
            label = 'Birth date',
            validators = validators.Range( max_value = datetime.date.today() )
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

        user_id = fields.Hidden( type = types.Integer() )
        full_name = fields.Text( label = 'Full name' )
        password = fields.Password( label = 'Password' )
        number_of_children = fields.Number( label = 'Number of children' )
        birth_date = fields.Date( label = 'Birth date' )
        email = fields.Email( label = 'Email address' )
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

        # list<options.Option>
        def getMusicGenres():

            return options.generate([
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

        active = fields.Select(
            label = 'Active',
            type = types.Boolean(),
            # Hint: convert tuple/list items into list of Option
            options = options.generate([
                ( True, 'Yes' ),
                ( False, 'No' )
            ])
        )

        gender = fields.Select(
            label = 'Gender',
            options = [
                # Hint: empty element is acceptable
                options.Empty(),
                options.Option( 'M', 'Male' ),
                options.Option( 'F', 'Female' )
            ]
        )

        favourite_genre_ids = fields.Select(
            label = 'Favourite Genres',
            type = types.Integer(),
            # Hint: If you want to allow multiple selection
            multiple = True,
            # Hint: define just the function name and it will be evaluated when
            # the form is created.
            options = getMusicGenres 
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

        # list<options.Option>
        def getMusicGenres():

            # Hint: convert tuple/list items into list of Option
            return options.generate([
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
            type = types.Integer(),
            # Hint: define just the function name and it will be evaluated when
            # the form is created.
            options = getMusicGenres
        )

        accept_tc = fields.SwitchCheckbox(
            # Hint: You cant define the type attribute, its Boolean and it
            # can't be multiple or required field.
            label = 'Subscription',
            # Hint: Be aware, the paramter's name is 'option', not 'options'
            option = options.Option( True, 'Subscribe to newsletter' )
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
            options = options.generate( [ ('M','Male'), ('F','Female') ] )
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

        # list<options.Option>
        def getMusicGenres():

            # Hint: convert tuple/list items into list of Option
            return options.generate([
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
            type = types.Integer(),
            multiple = True,
            options = getMusicGenres,
            validators = validators.Selected( max_selected = 3 )
        )

        checked_genre_ids = fields.Checkbox(
            label = 'Checked Genres',
            type = types.Integer(),
            options = getMusicGenres,
            # Hint: You have to define required if you dont want to 
            # accept empty value.
            required = True,
            validators = validators.Selected( 3, 6 )
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


if __name__ == '__main__':
    app.run(
        debug = True
    )

