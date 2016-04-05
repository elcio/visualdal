visualdal
=========

WWW SQL Designer to web2py DAL converter.
-----------------------------------------

This script converts a XML written by [WWW SQL Designer](http://code.google.com/p/wwwsqldesigner/) to a web2py DAL code (Python). This way, you can use WWW SQL Designer, a great tool, to work on database modeling for your Python software.

The script is in a very early version, but is functional enough that we use it in our projects. Only a few datatypes are supported now: 

+ bit
+ date
+ datetime
+ decimal
+ int
+ mediumtext
+ tinyint
+ varchar

Also, column lengths are not supported and the script are completely not documented. You must use web2py conventions on your modeling work. For example, every table must have it's primary key called "id", int or tinyint, autoincrement.

You can add labels or validators by adding comments to table rows, in a strict format. For example:

    label="CEP",requires="[IS_NOT_EMPTY(),IS_CEP()]"

Will generate, in the column cep:

    Field('cep','string',label='CEP',requires=[IS_NOT_EMPTY(),IS_CEP()]),

Also you can add a value "fcol" in the row comments to fill the foreign key string formatter. Suposing you have a column called origin, foreign key of airport.id, you can add add the following comment to the origin column:

    label="Aeroporto de origem",fcol="%(name)s (%(code)s)"

This will generate:

    Field('origin',airport.id,label="Aeroporto de origem",requires=IS_IN_DB(db,'airport.id','%(name)s (%(code)s)'),

Feedback, suggestions and, of course, pull requests, are really welcome.



