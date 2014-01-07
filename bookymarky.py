#!/usr/bin/python
import os
import tempfile
import time

BOOKMARKS_PATH = os.path.join( os.environ[ 'HOME' ], ".config", "google-chrome", "Default", "Bookmarks" )

if not os.path.exists( BOOKMARKS_PATH ):
    raise Exception( "Can't find the default bookmarks file at '%s'" % BOOKMARKS_PATH )

with open( BOOKMARKS_PATH ) as f:
    bookmarks = f.read()

TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Bookymarky</title>

        <script src="http://code.jquery.com/jquery-2.0.3.min.js"></script>
        <script>
            var bookmarks = %(bookmarks)s;
        </script>
    </head>

    <body>
        <div id="content">
        <div>
        <script>
            function render( root )
            {
                if ( root.type == "folder" ) {
                    var result = "<ul>" + root.name + "\n";
                    for ( var i in root.children )
                        result += "<li>" + render( root.children[ i ] ) + "</li>\n";
                    return result + "</ul>";
                } else if ( root.type == "url" ) {
                    return '<a href="' + root.url + '">' + root.name + '</a>\n';
                } else {
                    var result = "<ul>\n";
                    for ( var i in root )
                        result += "<li>" + render( root[ i ] ) + "</li>\n";
                    return result + "</ul>";
                }
            }

            $("#content").html( render( bookmarks.roots ) );
        </script>
    </body>
</html>

"""

output = tempfile.NamedTemporaryFile( suffix = ".html" )
output.write( TEMPLATE % dict( bookmarks = bookmarks ) )
output.flush()
os.system( "google-chrome file://%s" % os.path.abspath( output.name ) )
time.sleep( 3 )
